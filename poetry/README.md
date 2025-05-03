# Docker Python Poetry Environment

Este directorio contiene una imagen Docker con Python 3.12 y Poetry para gestión profesional de dependencias en proyectos Python.

## Contenido
- `Dockerfile`: Imagen base con Python 3.12 y Poetry instalado y configurado

## Características principales
- Basada en la imagen oficial `python:3.12.10`
- Incluye Poetry para gestión determinista de dependencias
- Configurado para usar el entorno global (sin virtualenvs)
- Incluye herramientas de desarrollo esenciales (git, curl, build-essential)
- Ideal para desarrollo de paquetes y aplicaciones con dependencias complejas

## Ejemplo de uso

### Construir la imagen

```bash
# Desde el directorio raíz del proyecto
docker build -t python-poetry -f ./poetry/Dockerfile .
```

### Ejecutar el contenedor

```bash
# Linux/MacOS
docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python-poetry:latest

# Windows PowerShell
docker run -it --rm -v "${PWD}:/$(Split-Path -Leaf $PWD)" -w "/$(Split-Path -Leaf $PWD)" python-poetry:latest
```

### Iniciar un nuevo proyecto con Poetry

```bash
# Dentro del contenedor
poetry new mi-proyecto
cd mi-proyecto
poetry add pandas matplotlib
poetry run python -c "import pandas; print(pandas.__version__)"
```

### Recomendaciones
- Usa esta imagen para proyectos que necesiten gestión robusta de dependencias
- Ideal para desarrollo de bibliotecas Python que serán publicadas
- Aprovecha Poetry para bloquear versiones exactas y garantizar reproducibilidad
- Utiliza `pyproject.toml` para configurar tu proyecto con estándares modernos

---

Para más imágenes y entornos, revisa el [README principal](../README.md).
