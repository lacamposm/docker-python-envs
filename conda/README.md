# Docker Python Conda Base Environment

Imagen basada en Miniconda para entornos de desarrollo científico y análisis de datos.

## Dockerfile: conda/Dockerfile

Versión extendida para desarrollo con Node.js y otras herramientas adicionales.

```dockerfile
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
```

### Linux/MacOS

1. Construir la imagen de Docker:
    ```sh
    docker build -t python-conda-dev -f ./conda/Dockerfile.dev .
    ```
2. Ejecutar el contenedor montando la carpeta actual como volumen:
    ```sh
    docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python-conda-dev:latest
    ```

### Windows

1. Construir la imagen de Docker:
    ```powershell
    docker build -t python-conda-dev -f .\conda\Dockerfile.dev .
    ```
2. Ejecutar el contenedor montando la carpeta actual como volumen:
    ```powershell
    docker run -it --rm `
    -v "${PWD}:/$(Split-Path -Leaf $PWD)" `
    -w "/$(Split-Path -Leaf $PWD)" `
    python-conda-dev:latest
    ```

---

Para más imágenes y entornos, revisa el [README principal](../README.md).