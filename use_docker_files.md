# ***Construyendo y corriendo imagenes Docker en local.***


## Dockerfile.PythonMin

Imagen mínima de Python 3.12 para entornos ligeros sin paquetes adicionales.
Esta imagen se utiliza cuando se requiere un entorno base de Python sin dependencias extras, ideal para ejecutar scripts o aplicaciones simples de manera eficiente sin sobrecargar el contenedor.

```dockerfile
FROM python:3.12-slim

CMD ["/bin/bash"]
```

### Ejecutar y Crear el Contenedor

Estando en la carpeta padre del proyecto:

#### Linux/MacOS


1. Construir la imagen de Docker:

     ```bash
     docker build -t python3.12-slim -f ./python-min/Dockerfile .
     ```

3. Ejecutar el contenedor montando la carpeta actual como volumen:
     ```sh
     docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python3.12-slim:latest
     ```

#### Windows

1. Construir la imagen de Docker:
     ```sh
     docker build -t python3.12-slim -f .\python-min\Dockerfile .
     ```
3. Ejecutar el contenedor montando la carpeta actual como volumen:

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

## Dockerfile.PythonConda

Imagen basada en Miniconda para entornos de desarrollo científico.

```dockerfile
FROM continuumio/miniconda3:23.10.0-1

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
```

### Ejecutar y Crear el Contenedor

Estando en la carpeta padre del proyecto:

#### Linux/MacOS

1. Construir la imagen de Docker:
     ```sh
     docker build -t python-conda -f ./conda/Dockerfile .
     ```

2. Ejecutar el contenedor montando la carpeta actual como volumen:
     ```sh
     docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python-conda:latest
     ```

#### Windows

1. Construir la imagen de Docker:
     ```powershell
     docker build -t python-conda -f .\conda\Dockerfile .
     ```

2. Ejecutar el contenedor montando la carpeta actual como volumen:
     ```powershell
     docker run -it --rm `
     -v "${PWD}:/$(Split-Path -Leaf $PWD)" `
     -w "/$(Split-Path -Leaf $PWD)" `
     python-conda:latest
     ```

## Dockerfile.PythonCondaDev

Versión extendida para desarrollo con Node.js y otras herramientas adicionales.

```dockerfile
# Imagen base misma que en latest de PythonConda
FROM continuumio/miniconda3:23.10.0-1

# Actualizar repositorios e instalar utilidades esenciales para desarrollo
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    ca-certificates \
    curl \
    git \
    libnss3 \
    make \
    sudo \
    wget \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update && apt-get install -y --no-install-recommends nodejs \
    && node -v && npm -v \
    && git config --system core.sshCommand "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" \
    && git config --system --add safe.directory "*" \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
```

### Ejecutar y Crear el Contenedor

#### Linux/MacOS

1. Construir la imagen de Docker:
     ```sh
     docker build -t python-conda-dev -f ./conda/Dockerfile.dev .
     ```

2. Ejecutar el contenedor montando la carpeta actual como volumen:
     ```sh
     docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python-conda-dev:latest
     ```

#### Windows

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

## Dockerfile.PythonPoetry

Imagen básica con Python 3.12-slim y Poetry para gestión de dependencias.

```dockerfile
# Imagen base de Python 3.12
FROM python:3.12-slim

# Instalar utilidades necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    git \
    wget \
    make \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

# Configuración de git
RUN git config --system core.sshCommand "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" \
    && git config --system --add safe.directory "*"

# Directorio de trabajo
WORKDIR /developer

# CMD por defecto
CMD ["/bin/bash"]
```

### Ejecutar y Crear el Contenedor

Estando en la carpeta padre del proyecto:

#### Linux/MacOS

1. Construir la imagen de Docker:
     ```sh
     docker build -t python-poetry -f ./poetry/Dockerfile .
     ```

2. Ejecutar el contenedor montando la carpeta actual como volumen:
     ```sh
     docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python-poetry:latest
     ```

#### Windows

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

## Dockerfile.PoetryDev

Versión de desarrollo con herramientas adicionales y Node.js.

```dockerfile
# Imagen base de Python 3.12
FROM python:3.12

# Instalar utilidades necesarias, Node.js, y todas las dependencias en un solo paso
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    curl \
    git \
    wget \
    sudo \
    ca-certificates \
    make \
    libnss3 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && node -v && npm -v \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry \
    && git config --system core.sshCommand "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" \
    && git config --system --add safe.directory "*"

CMD ["/bin/bash"]
```

### Ejecutar y Crear el Contenedor

#### Linux/MacOS

1. Construir la imagen de Docker:
     ```sh
     docker build -t python-poetry-dev -f ./poetry/Dockerfile.dev .
     ```

2. Ejecutar el contenedor montando la carpeta actual como volumen:
     ```sh
     docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python-poetry-dev
     ```

#### Windows

1. Construir la imagen de Docker:
     ```powershell
     docker build -t python-poetry-dev -f .\poetry\Dockerfile.dev .
     ```

2. Ejecutar el contenedor montando la carpeta actual como volumen:
     ```powershell
     docker run -it --rm `
     -v "${PWD}:/$(Split-Path -Leaf $PWD)" `
     -w "/$(Split-Path -Leaf $PWD)" `
     python-poetry-dev
     ```

## Publicar la Imagen en Docker Hub

Para publicar las imágenes en Docker Hub, sigue estos pasos:

1. Inicia sesión en Docker Hub:
     ```sh
     docker login
     ```
     Ingresa tu nombre de usuario y contraseña cuando se solicite.

2. Etiquetar las imágenes
   Para subir una imagen a tu repositorio en Docker Hub, primero debes etiquetarla con tu nombre de usuario:

     Para PythonMin:
     ```sh
     docker tag python3.12-slim tu-usuario-dockerhub/nombre-asignado:python3.12-slim
     ```
     Para PythonConda:
     ```sh
     docker tag python-conda tu-usuario-dockerhub/nombre-asignado:python-conda
     ```
     Para PythonCondaDev:
     ```sh
     docker tag python-conda-dev tu-usuario-dockerhub/nombre-asignado:python-conda-dev
     ```
     Para PythonPoetry:
     ```sh
     docker tag python-poetry tu-usuario-dockerhub/nombre-asignado:python-poetry
     ```
     Para PoetryDev:
     ```sh
     docker tag python-poetry-dev tu-usuario-dockerhub/nombre-asignado:python-poetry-dev
     ```

3. Subir las imágenes a Docker Hub
   Una vez etiquetadas, puedes subirlas a Docker Hub:

     Para PythonMin:
     ```sh
     docker push tu-usuario-dockerhub/nombre-asignado:python3.12-slim
     ```
     Para PythonConda:
     ```sh
     docker push tu-usuario-dockerhub/nombre-asignado:python-conda
     ```
     Para PythonCondaDev:
     ```sh
     docker push tu-usuario-dockerhub/nombre-asignado:python-conda-dev
     ```
     Para PythonPoetry:
     ```sh
     docker push tu-usuario-dockerhub/nombre-asignado:python-poetry
     ```
     Para PoetryDev:
     ```sh
     docker push tu-usuario-dockerhub/nombre-asignado:python-poetry-dev
     ```

4. Descargar y utilizar imágenes desde Docker Hub
   Para descargar y usar una imagen publicada:

     ```sh
     docker pull tu-usuario-dockerhub/nombre-asignado:python-conda-dev
     ```

     Para Linux:
     ```sh
     docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") tu-usuario-dockerhub/nombre-asignado:python-conda-dev
     ```

     Para Windows:
     ```powershell
     docker run -it --rm -v "${PWD}:/$(Split-Path -Leaf $PWD)" -w "/$(Split-Path -Leaf $PWD)" tu-usuario-dockerhub/nombre-asignado:python-conda-dev
     ```

     Asegúrate de reemplazar `tu-usuario-dockerhub` con tu nombre de usuario en Docker Hub si estás subiendo tus propias imágenes.

5. Explicación de los parámetros
     - `-it`: Permite la interacción con el contenedor.
     - `--rm`: Elimina el contenedor al detenerse.
     - `-v "$(pwd):/$(basename "$(pwd)")"`: Monta el directorio actual en el contenedor.
     - `-w /$(basename "$(pwd)")"`: Define el directorio de trabajo.