# Docker Python Conda Base Environment

Este directorio contiene una imagen Docker basada en Miniconda, optimizada para entornos de desarrollo científico y análisis de datos.

## Contenido
- `Dockerfile`: Imagen base con Miniconda y herramientas esenciales de desarrollo

## Características principales
- Basada en la imagen oficial `continuumio/miniconda3:24.11.1-0`
- Incluye Python 3.12.8 con sistema de gestión de paquetes Conda
- Preinstaladas herramientas de desarrollo esenciales (git, build-essential, curl)
- Configuración de seguridad para Git preestablecida
- Cliente PostgreSQL incluido para conexión a bases de datos
- Ideal para proyectos de ciencia de datos y análisis

## Ejemplo de uso

### Construir la imagen

```bash
# Desde el directorio raíz del proyecto
docker build -t python-conda-dev -f ./conda/Dockerfile .
```

### Ejecutar el contenedor

```bash
# Linux/MacOS
docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python-conda-dev:latest

# Windows PowerShell
docker run -it --rm -v "${PWD}:/$(Split-Path -Leaf $PWD)" -w "/$(Split-Path -Leaf $PWD)" python-conda-dev:latest
```

### Crear y activar un entorno Conda

```bash
# Dentro del contenedor
conda create -n mi-entorno python=3.10 pandas numpy scikit-learn
conda activate mi-entorno
python -c "import pandas; print('Pandas version:', pandas.__version__)"
```

### Recomendaciones
- Usa esta imagen para proyectos de ciencia de datos, machine learning y visualización
- Aprovecha Conda para gestionar dependencias con componentes C/C++ complejos
- Crea entornos aislados para cada proyecto usando `conda create -n nombre-entorno`
- Extiende el Dockerfile si necesitas incluir componentes adicionales específicos
- Para proyectos de ciencia de datos, considera usar un archivo `environment.yml`

---

Para más imágenes y entornos, revisa el [README principal](../README.md).