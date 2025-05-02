# Use the same base image as the main Dockerfile
# For more information:
#   - https://hub.docker.com/r/lacamposm/docker-helpers
#   - https://github.com/lacamposm/desarrollo-analitico-oic
FROM lacamposm/docker-helpers:python-conda-base-0.1.1

LABEL maintainer="lacamposm <lacamposm@unal.edu.co>" \
      version="0.1.1" \
      description="Python 3.12.10 + Spark 3.5.5"

# Install dependencies, configure system, and setup directories in a single layer
# to reduce image size and number of layers  
RUN mkdir -p /my-project-dir /data/_tmp && \
    chmod -R 777 /data/_tmp && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        bash-completion \
        locales \
        openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/* && \
    wget -q https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz && \
    tar -xzf spark-3.5.5-bin-hadoop3.tgz && \
    mv spark-3.5.5-bin-hadoop3 /opt/spark && \
    rm spark-3.5.5-bin-hadoop3.tgz && \
    rm -rf /tmp/* /root/.cache /root/.wget-hsts

# Configure environment variables.
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Expose ports for Spark UI, FastAPI, Streamlit, Jupyter
EXPOSE 4040 8000 8501 8888