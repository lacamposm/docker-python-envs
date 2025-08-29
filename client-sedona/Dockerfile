# ----------------------------------------------------------------------------
# Client Dockerfile
# Base: lacamposm/docker-helpers:sedona-1.7.2_spark-3.5.5-0.1.1
# - NO cambia ninguna versión de Spark/Sedona/JAR.
# - Crea el entorno conda 'sedona-spark' a partir de environment.yml (Python 3.10).
# - Configura PySpark para usar ese intérprete.
# ----------------------------------------------------------------------------
FROM lacamposm/docker-helpers:sedona-1.7.2_spark-3.5.5-0.1.1

# Directorio de trabajo del proyecto
WORKDIR /apache-sedona-project

# Copia el environment.yml (debe existir junto a este Dockerfile)
COPY environment.yml ./environment.yml

# Construye el entorno conda según el nombre declarado en environment.yml (sedona-spark)
RUN conda env create -f environment.yml  && conda clean -afy

# Configura PySpark para que use el Python del entorno conda
ENV CONDA_ENV=sedona-spark
ENV PYSPARK_PYTHON=/opt/conda/envs/${CONDA_ENV}/bin/python
ENV PYSPARK_DRIVER_PYTHON=/opt/conda/envs/${CONDA_ENV}/bin/python

# (Opcional) Hornear spark-defaults.conf con los mismos packages exactos (sin cambiar versiones)
# COPY spark-defaults.conf $SPARK_HOME/conf/spark-defaults.conf

# Crea un usuario no-root para ejecutar trabajos
RUN useradd -ms /bin/bash devuser && chown -R devuser:devuser /apache-sedona-project
USER devuser

# Exponer puertos útiles (Spark UI y Jupyter, por ejemplo)
EXPOSE 4040 8888

# Comando por defecto: abrir shell con el entorno activado
CMD ["/bin/bash", "-lc", "source activate sedona-spark && bash"]