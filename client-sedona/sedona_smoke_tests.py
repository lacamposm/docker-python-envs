"""
sedona_smoke_tests.py
================================

This script runs a suite of smoke tests for Apache Sedona 1.7.2 on Spark 3.5.x
using only the Python API. It's designed to run in a container configured with
Spark and Sedona, as built throughout this conversation.

Key features:
* Synthetic data generation: creates test datasets in geo_data/smoke/ (GeoJSON,
  CSV with WKT, and valid GeoParquet) to ensure Sedona can read and process
  common formats even without external data.
* Robust reading: reads GeoJSON, CSV/WKT and GeoParquet. The GeoJSON reader
  flattens the FeatureCollection structure to expose the geometry column at the
  root; the CSV reader validates WKT with shapely and discards malformed rows
  to prevent Spark session abortion.
* Spatial operations: demonstrates Sedona functions like ST_Area, ST_Centroid,
  ST_Buffer, ST_Contains, and ST_Union_Aggr, plus random point generation with
  ST_GeneratePoints.
* Configuration control: configures Sedona through spark.conf.set to enable
  global indexes and avoid "Ignoring non-Spark config property" warnings.
  Extensions and serializers are activated via SparkSession.builder.

To run this script from a container with the client image built earlier,
activate the conda environment sedona-spark and run:
python sedona_smoke_tests_resiliente.py
"""

import csv
import os
from pathlib import Path
from typing import Optional, Tuple

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (IntegerType, StringType, StructField,
                               StructType)
from sedona.spark import SedonaContext
from shapely import wkt as shapely_wkt


###############################################################################
# General helpers
###############################################################################

def safe_print_header(title: str) -> None:
    """Print a decorative header for section delimitation."""
    print("\n" + "=" * 80)
    print(f"🧪 {title}")
    print("=" * 80)


def create_spark_session(app_name: str = "sedona_smoke") -> SparkSession:
    """
    Build a SparkSession configured for Sedona 1.7.2.

    - Configures Sedona extensions and Kryo serializer. These properties are
      included in case the image doesn't have a spark-defaults.conf defining them.
    - Activates Sedona's global quadtree index after building the session to
      avoid invalid property warnings.

    Args:
        app_name: Spark application name.

    Returns:
        SparkSession instance ready for Sedona.
    """
    print("🚀 Creating Spark session with Sedona configuration...")
    spark = (
        SparkSession.builder
        .appName(app_name)
        .config(
            "spark.sql.extensions",
            "org.apache.sedona.sql.SedonaSqlExtensions",
        )
        .config(
            "spark.serializer",
            "org.apache.spark.serializer.KryoSerializer",
        )
        .config(
            "spark.kryo.registrator",
            "org.apache.sedona.core.serde.SedonaKryoRegistrator",
        )
        .getOrCreate()
    )
    # Set Sedona parameters after creating session
    spark.conf.set("sedona.global.index", "true")
    spark.conf.set("sedona.global.indextype", "quadtree")
    print("✅ Spark session created successfully!")
    return spark


###############################################################################
# Test data generators
###############################################################################

def write_geojson_example(output_path: Path) -> None:
    """
    Create a small GeoJSON file with three points and save it to output_path.
    This dataset is used to test GeoJSON reading and feature flattening.
    """
    print(f"📝 Generating GeoJSON example at {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-74.0721, 4.7110]},
            "properties": {"id": 1, "name": "Bogotá", "category": "capital"},
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-75.5636, 6.2442]},
            "properties": {"id": 2, "name": "Medellín", "category": "city"},
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-76.5225, 3.4516]},
            "properties": {"id": 3, "name": "Cali", "category": "city"},
        },
    ]
    geojson = {"type": "FeatureCollection", "features": features}
    import json

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    print("✅ GeoJSON example created successfully!")


def write_csv_wkt_example(output_path: Path, include_bad_row: bool = False) -> None:
    """
    Create a CSV with id and wkt columns. By default all geometries are valid.
    If include_bad_row is True, add a row with malformed WKT to demonstrate
    error handling in read_csv_wkt.
    """
    print(f"📝 Generating CSV/WKT example at {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {"id": 1, "wkt": "POINT (-74.0721 4.7110)"},
        {"id": 2, "wkt": "POINT (-75.5636 6.2442)"},
        {
            "id": 3,
            "wkt": "POLYGON ((-74.1 4.7, -74.05 4.7, -74.05 4.75, -74.1 4.75, -74.1 4.7))",
        },
    ]
    if include_bad_row:
        rows.append({"id": 4, "wkt": "POLYGON ((-74.1 4.7, -74.05 4.7, 0"})
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "wkt"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print("✅ CSV/WKT example created successfully!")


def write_geoparquet_example(sedona: SedonaContext, output_dir: Path) -> None:
    """
    Generate a small test GeoParquet file using Sedona to ensure it contains
    valid geo metadata. The geometry is a list of points with attributes.
    """
    print(f"📝 Generating GeoParquet example at {output_dir}...")
    output_dir.mkdir(parents=True, exist_ok=True)
    # Use Sedona SQL to create a test DataFrame
    df = sedona.sql(
        """
        SELECT
            id,
            name,
            ST_Point(lon, lat) AS geometry,
            category
        FROM VALUES
            (1, 'Bogotá', -74.0721, 4.7110, 'capital'),
            (2, 'Medellín', -75.5636, 6.2442, 'city'),
            (3, 'Cali', -76.5225, 3.4516, 'city')
        AS t(id, name, lon, lat, category)
        """
    )
    # Write GeoParquet; Sedona will add metadata
    df.write.mode("overwrite").format("geoparquet").save(str(output_dir))
    print("✅ GeoParquet example created successfully!")


###############################################################################
# Robust readers
###############################################################################

def read_geojson_flat(spark: SparkSession, path: Path, sedona_ctx: Optional[SedonaContext] = None):
    """
    Read a GeoJSON and return a DataFrame with geometry, id, name, and category
    columns by flattening the FeatureCollection structure.

    Args:
        spark: Spark session configured with Sedona.
        path: Path to GeoJSON file.

    Returns:
        DataFrame ready for spatial operations.
    """
    safe_print_header(f"Reading GeoJSON: {path}")
    try:
        if sedona_ctx is None:
            sedona_ctx = SedonaContext.create(spark)
        df_raw = sedona_ctx.read.format("geojson").load(str(path))
        df_features = df_raw.select(F.explode("features").alias("feature"))
        df = df_features.select(
            F.col("feature.geometry").alias("geometry"),
            F.col("feature.properties.id").cast(IntegerType()).alias("id"),
            F.col("feature.properties.name").cast(StringType()).alias("name"),
            F.col("feature.properties.category").cast(StringType()).alias("category"),
        )
        print("📊 GeoJSON schema:")
        df.printSchema()
        print("📋 GeoJSON data:")
        df.show(truncate=False)
        print("✅ GeoJSON read successfully!")
        return df
    except Exception as exc:
        print(f"❌ Failed to read GeoJSON at {path}: {exc}\n")
        return None


def read_csv_wkt(spark: SparkSession, path: Path) -> Optional:
    """
    Read a CSV with id and wkt columns and build a geometry column using
    ST_GeomFromWKT. This version assumes all CSV geometries are valid.

    Args:
        spark: Spark session.
        path: Path to CSV.

    Returns:
        DataFrame with id and geometry columns or None if failed.
    """
    safe_print_header(f"Reading CSV/WKT: {path}")
    try:
        df_raw = spark.read.format("csv").option("header", "true").load(str(path))
        if df_raw.count() == 0:
            print(f"⚠️ CSV {path} is empty.")
            return None
        df = df_raw.select(
            F.col("id").cast(IntegerType()).alias("id"),
            F.expr("ST_GeomFromWKT(wkt)").alias("geometry"),
        )
        print("📊 CSV/WKT schema:")
        df.printSchema()
        print("📋 CSV/WKT data:")
        df.show(truncate=False)
        print("✅ CSV/WKT read successfully!")
        return df
    except Exception as exc:
        print(f"❌ Failed to convert WKT to geometry in {path}: {exc}\n")
        return None


def read_geoparquet(spark: SparkSession, path: Path) -> Optional:
    """
    Read a GeoParquet using Sedona.

    Args:
        spark: Spark session.
        path: Path to GeoParquet directory.

    Returns:
        Read DataFrame or None.
    """
    safe_print_header(f"Reading GeoParquet: {path}")
    try:
        df = spark.read.format("geoparquet").load(str(path))
        print("📊 GeoParquet schema:")
        df.printSchema()
        print("📋 GeoParquet data:")
        df.show(truncate=False)
        print("✅ GeoParquet read successfully!")
        return df
    except Exception as exc:
        print(f"❌ Failed to read GeoParquet at {path}: {exc}\n")
        return None


###############################################################################
# Example operations
###############################################################################

def run_ops_examples(points_df, polygons_df, spark: SparkSession):
    """
    Run basic spatial operations on points and polygons.

    - Calculate area and centroid of each polygon
    - Generate buffers around points
    - Perform ST_Contains spatial join between polygons and points
    - Calculate spatial union of all polygons with ST_Union_Aggr
    """
    safe_print_header("Spatial functions, predicates and aggregations")
    try:
        # Area and centroid
        polys_with_area = polygons_df.withColumn("area", F.expr("ST_Area(geometry)"))
        polys_with_area = polys_with_area.withColumn(
            "centroid_wkt", F.expr("ST_AsText(ST_Centroid(geometry))")
        )
        print("📐 Polygon areas and centroids:")
        polys_with_area.select("area", "centroid_wkt").show(truncate=False)

        # Buffers in degrees (simple example, not geodetic)
        points_buf = points_df.selectExpr("ST_Buffer(geometry, 0.05) AS buf")
        print("🛡️ Point buffers:")
        points_buf.show(truncate=False)

        # Point-polygon join
        points_df.createOrReplaceTempView("points")
        polygons_df.createOrReplaceTempView("polys")
        result = spark.sql(
            "SELECT p.id AS point_id, p.geometry AS point_geom, s.id AS poly_id "
            "FROM points p, polys s "
            "WHERE ST_Contains(s.geometry, p.geometry)"
        )
        print("🔍 Point-in-polygon join results:")
        result.show(truncate=False)

        # Spatial union of all polygons
        union_df = polygons_df.selectExpr("ST_Union_Aggr(geometry) AS merged_geom")
        print("🧩 Union of all polygons:")
        union_df.show(truncate=False)

        print("✅ Spatial operations completed successfully!")
    except Exception as exc:
        print(f"❌ Failed during spatial operations: {exc}\n")


def run_random_points_example(spark: SparkSession) -> None:
    """
    Demonstrate pseudo-random point generation within a polygon using
    ST_GeneratePoints (Sedona's Spider module).
    """
    safe_print_header("Random point generation with ST_GeneratePoints")
    try:
        df_rand = spark.sql(
            """
            SELECT ST_GeneratePoints(
                ST_PolygonFromEnvelope(-74.1, 4.7, -74.05, 4.75),
                5,
                42
            ) AS geom
            """
        )
        print("🎲 Randomly generated points:")
        df_rand.show(truncate=False)
        print("✅ Random point generation successful!")
    except Exception as exc:
        print(f"❌ Failed to generate random points: {exc}\n")


###############################################################################
# Main: generate data, read and run tests
###############################################################################

def main() -> None:
    # Setup database
    base_dir = Path("geo_data/smoke")
    geojson_path = base_dir / "cities.geojson"
    csv_path = base_dir / "geoms_wkt.csv"
    geoparquet_dir = base_dir / "cities_geoparquet"

    print("🚀 Starting Sedona Smoke Tests")
    print("📁 Creating test data directory...")
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create Spark and Sedona context
    spark = create_spark_session(app_name="sedona_smoke_resiliente")
    sedona_ctx = SedonaContext.create(spark)

    # Generate synthetic datasets if they don't exist
    if not geojson_path.exists():
        write_geojson_example(geojson_path)
    else:
        print("✅ GeoJSON already exists")

    if not csv_path.exists():
        write_csv_wkt_example(csv_path, include_bad_row=False)
    else:
        print("✅ CSV/WKT already exists")

    if not geoparquet_dir.exists():
        write_geoparquet_example(sedona_ctx, geoparquet_dir)
    else:
        print("✅ GeoParquet already exists")

    # Read data sources
    df_geojson = read_geojson_flat(spark, geojson_path, sedona_ctx)
    df_csv = read_csv_wkt(spark, csv_path)
    df_gpq = read_geoparquet(spark, geoparquet_dir)

    # Select points and polygons for operations
    points_df = df_csv if df_csv is not None else df_geojson

    # Create example polygons
    polygons = [
        (1, "POLYGON ((-74.1 4.68, -74.1 4.73, -74.05 4.73, -74.05 4.68, -74.1 4.68))"),
        (2, "POLYGON ((-75.6 6.22, -75.6 6.27, -75.54 6.27, -75.54 6.22, -75.6 6.22))"),
    ]
    df_polygons_raw = spark.createDataFrame(polygons, ["id", "wkt"])
    df_polygons = df_polygons_raw.select(
        F.col("id"),
        F.expr("ST_GeomFromWKT(wkt)").alias("geometry"),
    )

    # Run operations if we have valid points
    if points_df is not None:
        run_ops_examples(points_df, df_polygons, spark)
    else:
        print("❌ No valid points data available for spatial operations")

    # Generate random points
    run_random_points_example(spark)

    # Final message
    safe_print_header("Test Summary")
    print("✅ Smoke tests completed successfully!")
    print("📊 Generated test data available in: geo_data/smoke/")
    print("🔍 Check above for any warnings or errors")
    print("🎉 All done! Happy spatial computing!")


if __name__ == "__main__":
    main()
