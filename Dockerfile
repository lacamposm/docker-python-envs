# Use image base for spark/Dockerfile
# For more information:
#   - https://hub.docker.com/r/lacamposm/docker-helpers
#   - https://github.com/lacamposm/desarrollo-analitico-oic
FROM lacamposm/docker-helpers:pyspark-conda-0.1.2

WORKDIR /pyspark-project

# Copy environment.yml and setup Conda environment
COPY environment.yml /tmp/environment.yml

# Define user and group IDs as build arguments
ARG USER_UID=1000
ARG USER_GID=1000

# Combine all RUN commands to reduce image layers
RUN conda env create -f /tmp/environment.yml -n pyspark-env  \
    && conda clean --all --yes \
    && rm /tmp/environment.yml \
    && printf "source /opt/conda/etc/profile.d/conda.sh\nconda activate pyspark-env \n" \
       > /etc/profile.d/conda-env.sh \
    && groupadd --gid $USER_GID dev-user \
    && useradd --uid $USER_UID --gid $USER_GID -m dev-user \
    && chown -R dev-user:dev-user /pyspark-project \
    && { \
         echo "source /opt/conda/etc/profile.d/conda.sh"; \
         echo "conda activate pyspark-env "; \
       } >> /home/dev-user/.bashrc \
    && chown dev-user:dev-user /home/dev-user/.bashrc

# Switch to the non-root user
USER dev-user

# - 4040-Spark UI and 8501-Streamlit
EXPOSE 4040 8501

CMD ["/bin/bash"]
