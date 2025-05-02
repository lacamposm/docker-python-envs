# app.py
# Aplicación Streamlit para verificar el entorno PySpark y ejecutar consultas SQL
import os 
import shutil
import pyspark.sql.functions as F
import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# --- Inicialización de la Sesión de Spark ---
@st.cache_resource # Cache la Sesión de Spark para mejorar el rendimiento
def get_spark_session():
    """Crea y devuelve una Sesión de Spark."""
    try:
        spark = SparkSession.builder \
            .appName("StreamlitPySparkApp") \
            .master("local[*]") \
            .getOrCreate()
        return spark
    except Exception as e:
        st.error(f"Error al inicializar la Sesión de Spark: {e}")
        st.stop() 

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
        messages.append(f"✅ Usando una SparkSession existente (Versión: {spark.version})")

        test_data = [("PVC_001", 150),
                     ("PVC_002", 200),
                     ("PVC_003", 75)]
        df = spark.createDataFrame(test_data, ["product_id", "demand"])
        messages.append("✅ DataFrame de prueba creado exitosamente.")

        total_demand = df.agg(F.sum("demand").alias("total_demand")).first()[0]
        messages.append(f"📊 Demanda total calculada: {total_demand} (Esperado: 425)")
        if total_demand != 425:
             messages.append("⚠️ Advertencia: ¡Desajuste en la demanda total!")

        high_demand = df.filter(col("demand") > 100).count()
        messages.append(f"🔍 Productos con demanda > 100: {high_demand} (Esperado: 2)")
        if high_demand != 2:
             messages.append("⚠️ Advertencia: ¡Desajuste en el conteo de alta demanda!")

        df = df.withColumn("demand_category",
                          F.when(col("demand") > 150, "Alta")
                           .otherwise("Media/Baja"))
        messages.append("🎛️ Columna 'demand_category' agregada.")

        temp_dir = "/tmp/streamlit_pyspark_test_output"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        df.write.mode("overwrite").parquet(temp_dir)
        messages.append(f"💾 Datos escritos temporalmente en: {temp_dir}")

        df_read = spark.read.parquet(temp_dir)
        read_count = df_read.count()
        original_count = df.count()
        if read_count == original_count:
            messages.append(f"🔄 Verificación de lectura exitosa (Conteo: {read_count}).")
        else:
            messages.append(f"❌ ¡Verificación de lectura FALLIDA! Conteo original: {original_count}, Conteo de lectura: {read_count}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return False, messages

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            messages.append(f"🧹 Directorio temporal limpiado: {temp_dir}")

        messages.append("🎉 ¡Prueba del entorno PySpark completada exitosamente!")
        return True, messages

    except Exception as e:
        messages.append(f"❌ Error durante la prueba del entorno PySpark: {str(e)}")
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
             try:
                 shutil.rmtree(temp_dir)
                 messages.append(f"🧹 Intento de limpieza de {temp_dir} después del error.")
             except Exception as cleanup_e:
                 messages.append(f"⚠️ Error durante la limpieza después de la falla de la prueba: {cleanup_e}")
        return False, messages

@st.cache_resource 
def create_sample_dataframe(_spark):
    """Crea un DataFrame de PySpark de ejemplo."""
    data = [("Alice", 1, "HR"),
            ("Bob", 2, "Engineering"),
            ("Charlie", 3, "Engineering"),
            ("David", 4, "HR"),
            ("Eve", 5, "Sales")]
    columns = ["Name", "ID", "Department"]
    try:
        df = _spark.createDataFrame(data, columns)
        df.createOrReplaceTempView("employees") 
        return df
    except Exception as e:
        st.error(f"Error al crear el DataFrame: {e}")
        st.stop()

# Título principal de la aplicación
st.title("Aplicación PySpark con Streamlit")

# Inicializar la sesión Spark
spark = get_spark_session()
sample_df = create_sample_dataframe(spark)

# Crear las dos columnas
col1, col2 = st.columns(2)

# Contenido de la columna de verificación del entorno
with col1:
    st.header("Verificación del Entorno PySpark")
    with st.spinner("Ejecutando la verificación del entorno PySpark..."):
        test_success, test_messages = test_pyspark_environment(spark)

    if test_success:
        with st.expander("Mostrar Detalles de la Verificación del Entorno", expanded=False):
            for msg in test_messages:
                st.write(msg)
        st.success("✅ ¡Verificación del entorno PySpark aprobada!")
    else:
        st.error("🔴 ¡Verificación del entorno PySpark fallida!")
        for msg in test_messages:
            st.error(msg)
        st.warning("Es posible que la aplicación no funcione correctamente.")

with col2:
    st.header("Consulta Spark SQL")
    
    st.write("### Datos de Ejemplo")
    st.write("Se ha creado una vista temporal llamada `employees` con estos datos:")
    st.dataframe(sample_df.toPandas())

    st.write("---")

    st.write("#### Consulta los Datos")
    st.write("Ingresa tu consulta Spark SQL a continuación (usando la vista `employees`):")

    default_query = "SELECT Department, count(*) as Count FROM employees GROUP BY Department"
    query = st.text_area("Consulta Spark SQL", value=default_query, height=100)

    if st.button("Ejecutar Consulta"):
        if query:
            try:
                st.write("#### Resultados de la Consulta")
                result_df = spark.sql(query)
                result_pd = result_df.toPandas()
                st.dataframe(result_pd)
                st.success("¡Consulta ejecutada exitosamente!")
            except Exception as e:
                st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.warning("Por favor, ingresa una consulta.")

st.write("---")
st.write("Nota: Esta aplicación ejecuta Spark en modo local.")
