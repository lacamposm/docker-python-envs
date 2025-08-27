##
## Dockerfile for running Apache Sedona 1.7.2 on top of Spark 3.5.5
##
## According to Sedona’s platform support matrix, only
## Python 3.7–3.10 are tested with Spark 3.5 and Sedona 1.7.2.

# Use a minimal conda-enabled base image.  Mambaforge gives us mamba for
# faster environment resolution and defaults to the conda‑forge channel.
FROM condaforge/mambaforge:24.7.1-0

ARG SPARK_VERSION=3.5.5
ARG HADOOP_PROFILE=hadoop3
ARG SEDONA_VERSION=1.7.2
ARG SCALA_BIN=2.12

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Bogota

SHELL ["/bin/bash","-o","pipefail","-lc"]

RUN apt-get update && apt-get install -y --no-install-recommends \
        wget curl ca-certificates bash tini openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=${JAVA_HOME}/bin:$PATH

# Spark 3.5.5 (Hadoop 3)
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-${HADOOP_PROFILE}.tgz \
 && tar -xzf spark-${SPARK_VERSION}-bin-${HADOOP_PROFILE}.tgz \
 && mv spark-${SPARK_VERSION}-bin-${HADOOP_PROFILE} /opt/spark \
 && rm spark-${SPARK_VERSION}-bin-${HADOOP_PROFILE}.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# spark-defaults.conf con Sedona + GeoTools + repos + extensiones
RUN mkdir -p ${SPARK_HOME}/conf && \
    printf '%s\n' \
      "spark.sql.extensions=org.apache.sedona.sql.SedonaSqlExtensions" \
      "spark.serializer=org.apache.spark.serializer.KryoSerializer" \
      "spark.kryo.registrator=org.apache.sedona.core.serde.SedonaKryoRegistrator" \
      "spark.jars.packages=org.apache.sedona:sedona-spark-shaded-3.5_${SCALA_BIN}:${SEDONA_VERSION},org.datasyslab:geotools-wrapper:1.7.2-28.5" \
      "spark.jars.repositories=https://repo1.maven.org/maven2,https://artifacts.unidata.ucar.edu/repository/unidata-all" \
      > ${SPARK_HOME}/conf/spark-defaults.conf

# Puertos útiles (UI local / Jupyter)
EXPOSE 4040 8888

ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["/bin/bash","-lc","bash"]
