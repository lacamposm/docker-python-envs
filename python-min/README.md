# Python 3.12 Minimal Docker Image

Imagen mínima de Python 3.12 para entornos ligeros sin paquetes adicionales. Ideal para ejecutar scripts o aplicaciones simples de manera eficiente sin sobrecargar el contenedor.

## Dockerfile

```dockerfile
FROM python:3.12-slim

#  Set working directory for better layer caching
WORKDIR /workspace

#  Copy only requirements to cache dependencies layer
COPY requirements.txt .

#  Create venv, install dependencies, register kernel, 
# configure bashrc, and clean up in one layer
RUN set -eux; \
    python -m venv /opt/venv; \
    # ensure the virtualenv is activated in interactive shells
    echo 'source /opt/venv/bin/activate' >> /root/.bashrc; \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip; \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt; \
    rm requirements.txt; \
    # register this environment as a Jupyter kernel
    /opt/venv/bin/python -m ipykernel install --sys-prefix --name venv --display-name "Python3.12 (venv)"

#  Prepend venv to PATH and ensure bash sources bashrc in non-interactive mode
ENV PATH="/opt/venv/bin:$PATH" \
    BASH_ENV="/root/.bashrc"

#  Expose Jupyter Notebook port
EXPOSE 8888

#  Launch bash (venv will be active via bashrc)
CMD ["bash"]
```

El archivo `requirements.txt` incluye:

```
jupyter
ipykernel
```

## Cómo construir y ejecutar el contenedor

### Linux/MacOS

1. Construir la imagen de Docker:

    ```bash
    docker build -t python3.12-slim -f ./python-min/Dockerfile .
    ```

2. Ejecutar el contenedor montando la carpeta actual como volumen:
    ```sh
    docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python3.12-slim:latest
    ```

3. Para iniciar un servidor Jupyter Notebook y explorar el entorno:
    ```sh
    docker run -it --rm -p 8888:8888 -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python3.12-slim:latest jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
    ```

### Windows

1. Construir la imagen de Docker:
    ```sh
    docker build -t python3.12-slim -f .\python-min\Dockerfile .
    ```
2. Ejecutar el contenedor montando la carpeta actual como volumen:
    ```powershell
    docker run -it --rm -v "${PWD}:/$(Split-Path -Leaf $PWD)" -w "/$(Split-Path -Leaf $PWD)" python3.12-slim:latest
    ```
    O en una línea más legible usando el caracter de continuación ` :
    ```powershell
    docker run -it --rm `
         -v "${PWD}:/$(Split-Path -Leaf $PWD)" `
         -w "/$(Split-Path -Leaf $PWD)" `
         python3.12-slim:latest
    ```

---

Para más imágenes y entornos, revisa el [README principal](../README.md).
