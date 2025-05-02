# Prueba de funcionamiento básico de PySpark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pyspark.sql.functions as F


def test_pyspark_environment():
    """
    Prueba básica para verificar que PySpark está funcionando correctamente.
    Crea una sesión, genera datos de prueba y ejecuta operaciones básicas.
    """    
    # 1. Inicializar sesión de Spark
    try:
        spark = SparkSession.builder \
            .appName("PySparkTest") \
            .getOrCreate()
        
        print("✅ SparkSession creada exitosamente")
        print(f"Versión de PySpark: {spark.version}")
    except Exception as e:
        print(f"❌ Error al crear SparkSession: {str(e)}")
        return False

    # 2. Crear DataFrame de prueba
    test_data = [("PVC_001", 150), 
                 ("PVC_002", 200),
                 ("PVC_003", 75)]
    
    try:
        df = spark.createDataFrame(test_data, ["product_id", "demand"])
        print("\n✅ DataFrame creado exitosamente:")
        df.show()
    except Exception as e:
        print(f"❌ Error al crear DataFrame: {str(e)}")
        spark.stop()
        return False

    # 3. Probar transformaciones básicas
    try:
        # Calcular demanda total
        total_demand = df.agg(F.sum("demand").alias("total_demand")).first()[0]
        print(f"\n📊 Demanda total calculada: {total_demand} (Valor esperado: 425)")
        
        # Filtrar productos con demanda > 100
        high_demand = df.filter(col("demand") > 100).count()
        print(f"🔍 Productos con demanda >100: {high_demand} (Valor esperado: 2)")
        
        # Agregar columna calculada
        df = df.withColumn("demand_category", 
                          F.when(col("demand") > 150, "Alta")
                           .otherwise("Media/Baja"))
        print("\n🎛️ DataFrame con categorías de demanda:")
        df.show()
    except Exception as e:
        print(f"❌ Error en transformaciones: {str(e)}")
        spark.stop()
        return False

    # 4. Probar escritura temporal (modo seguro)
    try:
        temp_path = "/tmp/pyspark_test_output"
        df.write.mode("overwrite").parquet(temp_path)
        print(f"\n💾 Datos escritos temporalmente en: {temp_path}")
        
        # Leer datos guardados para verificación
        df_read = spark.read.parquet(temp_path)
        if df_read.count() == df.count():
            print("🔄 Lectura de datos verificada exitosamente")
        else:
            raise ValueError("Conteo de registros no coincide")
    except Exception as e:
        print(f"❌ Error en escritura/lectura: {str(e)}")
        spark.stop()
        return False

    # 5. Limpieza
    spark.stop()
    print("\n🧹 Sesión de Spark cerrada correctamente")
    return True

# Ejecutar prueba
if __name__ == "__main__":
    success = test_pyspark_environment()
    if success:
        print("\n🎉 ¡Todas las pruebas de PySpark se completaron exitosamente!")
    else:
        print("\n🔴 Se encontraron problemas en la configuración de PySpark")