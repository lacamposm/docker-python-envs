# For more information:
#   - https://hub.docker.com/r/lacamposm/docker-helpers
FROM continuumio/miniconda3:24.11.1-0

LABEL maintainer="lacamposm <lacamposm@unal.edu.co>" \
      version="0.1.3" \
      description="Python 3.12.8 + Spark 3.5.5 with conda for analytics development"

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    bash-completion \
    ca-certificates \
    curl \
    wget \
    sudo \
    locales \
    build-essential \
    make \
    postgresql-client \
    libnss3 \
    git \
    openjdk-17-jre-headless \
    && git config --system core.sshCommand "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" \
    && git config --system --add safe.directory "*" \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and install Spark
RUN mkdir -p /data/_tmp && \
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

# Expose ports for Spark UI
EXPOSE 4040

CMD ["/bin/bash"]