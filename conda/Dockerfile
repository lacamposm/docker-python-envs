FROM continuumio/miniconda3:23.10.0-1

LABEL maintainer="lacamposm <lacamposm@unal.edu.co>" \
      version="0.1.1" \
      description="Python 3.12 with conda for base image analytic projects"

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    ca-certificates \
    curl \
    libnss3 \
    make \
    sudo \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]