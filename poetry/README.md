# Docker Python Poetry Environment

Imagen básica con Python 3.12 y Poetry para gestión de dependencias.

## Dockerfile

```dockerfile
FROM python:3.12.10

LABEL maintainer="lacamposm <lacamposm@unal.edu.co>" \
      version="0.1.1" \
      description="Python 3.12.10 + Poetry"

ENV POETRY_HOME="/opt/poetry"
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    bash build-essential ca-certificates curl git make wget \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip --root-user-action=ignore \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && rm -rf /root/.cache/pypoetry/*

CMD ["/bin/bash"]
```

## Cómo construir y ejecutar el contenedor

### Linux/MacOS

1. Construir la imagen de Docker:
    ```sh
    docker build -t python-poetry -f ./poetry/Dockerfile .
    ```
2. Ejecutar el contenedor montando la carpeta actual como volumen:
    ```sh
    docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python-poetry:latest
    ```

### Windows

1. Construir la imagen de Docker:
    ```powershell
    docker build -t python-poetry -f .\poetry\Dockerfile .
    ```
2. Ejecutar el contenedor montando la carpeta actual como volumen:
    ```powershell
    docker run -it --rm `
    -v "${PWD}:/$(Split-Path -Leaf $PWD)" `
    -w "/$(Split-Path -Leaf $PWD)" `
    python-poetry:latest
    ```

---

Para más imágenes y entornos, revisa el [README principal](../README.md).
