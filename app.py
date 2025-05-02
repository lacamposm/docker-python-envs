# app.py
import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pyspark.sql.functions as F
import os # Import os for temporary path handling
import shutil # Import shutil for directory removal

# --- PySpark Environment Test Function ---
def test_pyspark_environment(spark):
    """
    Prueba básica para verificar que PySpark está funcionando correctamente
    usando una sesión existente.
    Genera datos de prueba y ejecuta operaciones básicas.
    Returns:
        tuple: (bool: success, list: messages)
    """
    messages = []
    try:
        messages.append(f"✅ Using existing SparkSession (Version: {spark.version})")

        # Crear DataFrame de prueba
        test_data = [("PVC_001", 150),
                     ("PVC_002", 200),
                     ("PVC_003", 75)]
        df = spark.createDataFrame(test_data, ["product_id", "demand"])
        messages.append("✅ Test DataFrame created successfully.")

        # Probar transformaciones básicas
        total_demand = df.agg(F.sum("demand").alias("total_demand")).first()[0]
        messages.append(f"📊 Total demand calculated: {total_demand} (Expected: 425)")
        if total_demand != 425:
             messages.append("⚠️ Warning: Total demand mismatch!")

        high_demand = df.filter(col("demand") > 100).count()
        messages.append(f"🔍 Products with demand > 100: {high_demand} (Expected: 2)")
        if high_demand != 2:
             messages.append("⚠️ Warning: High demand count mismatch!")

        df = df.withColumn("demand_category",
                          F.when(col("demand") > 150, "Alta")
                           .otherwise("Media/Baja"))
        messages.append("🎛️ Added 'demand_category' column.")

        # Probar escritura/lectura temporal
        temp_dir = "/tmp/streamlit_pyspark_test_output"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        df.write.mode("overwrite").parquet(temp_dir)
        messages.append(f"💾 Data written temporarily to: {temp_dir}")

        df_read = spark.read.parquet(temp_dir)
        read_count = df_read.count()
        original_count = df.count()
        if read_count == original_count:
            messages.append(f"🔄 Read verification successful (Count: {read_count}).")
        else:
            messages.append(f"❌ Read verification FAILED! Original count: {original_count}, Read count: {read_count}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return False, messages

        # Limpieza del directorio temporal
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            messages.append(f"🧹 Temporary directory cleaned up: {temp_dir}")

        messages.append("🎉 PySpark environment test completed successfully!")
        return True, messages

    except Exception as e:
        messages.append(f"❌ Error during PySpark environment test: {str(e)}")
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
             try:
                 shutil.rmtree(temp_dir)
                 messages.append(f"🧹 Attempted cleanup of {temp_dir} after error.")
             except Exception as cleanup_e:
                 messages.append(f"⚠️ Error during cleanup after test failure: {cleanup_e}")
        return False, messages


# --- Spark Session Initialization ---
@st.cache_resource # Cache the Spark Session for performance
def get_spark_session():
    """Creates and returns a Spark Session."""
    try:
        spark = SparkSession.builder \
            .appName("StreamlitPySparkApp") \
            .master("local[*]") \
            .getOrCreate()
        return spark
    except Exception as e:
        st.error(f"Error initializing Spark Session: {e}")
        st.stop() # Stop execution if Spark fails

spark = get_spark_session()

# --- Run PySpark Environment Test ---
st.subheader("PySpark Environment Check")
with st.spinner("Running PySpark environment check..."):
    test_success, test_messages = test_pyspark_environment(spark)

if test_success:
    with st.expander("Show Environment Check Details", expanded=False):
        for msg in test_messages:
            st.write(msg)
    st.success("✅ PySpark environment check passed!")
else:
    st.error("🔴 PySpark environment check failed!")
    for msg in test_messages:
        st.error(msg)
    st.warning("The application might not function correctly.")

st.write("---") # Separator

# --- Sample Data Creation ---
@st.cache_resource # Cache the DataFrame creation
def create_sample_dataframe(_spark):
    """Creates a sample PySpark DataFrame."""
    data = [("Alice", 1, "HR"),
            ("Bob", 2, "Engineering"),
            ("Charlie", 3, "Engineering"),
            ("David", 4, "HR"),
            ("Eve", 5, "Sales")]
    columns = ["Name", "ID", "Department"]
    try:
        df = _spark.createDataFrame(data, columns)
        df.createOrReplaceTempView("employees") # Register DataFrame as a temporary SQL table
        return df
    except Exception as e:
        st.error(f"Error creating DataFrame: {e}")
        st.stop()

sample_df = create_sample_dataframe(spark)

# --- Streamlit App UI ---
st.title("Simple PySpark Query App")

st.write("## Sample Employee Data")
st.write("A temporary view named `employees` has been created with this data:")
# Display the sample data using Pandas for better formatting in Streamlit
st.dataframe(sample_df.toPandas())

st.write("---")

st.write("## Query the Data")
st.write("Enter your Spark SQL query below (using the `employees` view):")

# Default query
default_query = "SELECT Department, count(*) as Count FROM employees GROUP BY Department"
query = st.text_area("Spark SQL Query", value=default_query, height=100)

if st.button("Run Query"):
    if query:
        try:
            st.write("### Query Results")
            result_df = spark.sql(query)
            result_pd = result_df.toPandas()
            st.dataframe(result_pd)
            st.success("Query executed successfully!")
        except Exception as e:
            st.error(f"Error executing query: {e}")
    else:
        st.warning("Please enter a query.")

st.write("---")
st.write("Note: This app runs Spark in local mode.")

# Optional: Add a button to stop the Spark session when done (useful in some contexts)
# if st.button("Stop Spark Session"):
#     spark.stop()
#     st.success("Spark Session stopped.")
#     st.rerun() # Rerun to reflect the stopped state if needed