# Use image base for development with conda and pyspark
# For more information:
#   - https://hub.docker.com/r/lacamposm/docker-helpers
#   - https://github.com/lacamposm/desarrollo-analitico-oic
FROM lacamposm/docker-helpers:pyspark-conda-0.1.1

WORKDIR /my-project

# Copy environment.yml and setup Conda environment
COPY environment.yml /tmp/environment.yml

RUN conda env create -f /tmp/environment.yml -n pyspark-env && \
    rm /tmp/environment.yml && \
    echo 'eval "$(conda shell.bash hook)"' >> ~/.bashrc && \
    echo 'conda activate pyspark-env' >> ~/.bashrc

# Example:
# Expose ports for:
# - 4040: Spark UI
# - 8501: Streamlit
EXPOSE 4040 8501

CMD ["/bin/bash"]