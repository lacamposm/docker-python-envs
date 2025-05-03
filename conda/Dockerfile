# Fixed the base image miniconda3
FROM continuumio/miniconda3:24.11.1-0

LABEL maintainer="lacamposm <lacamposm@unal.edu.co>" \
      version="0.1.2" \
      description="Python 3.12.8 with conda for analytics development"

# Update repositories and install essential packages for development
RUN apt-get update && apt-get install -y --no-install-recommends \
    # System utilities
    bash \
    ca-certificates \
    curl \
    wget \
    sudo \
    # Build tools
    build-essential \
    make \
    # Database clients
    postgresql-client \
    # Browser dependencies
    libnss3 \
    # Version control
    git \
    && git config --system core.sshCommand "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" \
    && git config --system --add safe.directory "*" \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]