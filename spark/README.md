# Docker Python Spark Environment

Este directorio contiene la imagen Docker para entornos de procesamiento distribuido con Python, Conda y Apache Spark.

## Contenido
- `Dockerfile`: Imagen base con Python, Conda y Spark 3.5.5

## Características principales
- Basada en la imagen `lacamposm/docker-helpers:python-conda-base-0.1.2`
- Incluye Apache Spark 3.5.5 y OpenJDK 17
- Expone puertos para Spark UI (4040), FastAPI (8000), Streamlit (8501) y Jupyter (8888)
- Preparada para proyectos de análisis de datos distribuidos y aplicaciones PySpark

## Ejemplo de uso

### Construir la imagen

```bash
# Desde el directorio raíz del proyecto
docker build -t python-spark -f ./spark/Dockerfile .
```

### Ejecutar el contenedor

```bash
# Linux/MacOS
docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") -p 4040:4040 -p 8501:8501 -p 8888:8888 python-spark:latest

# Windows PowerShell
docker run -it --rm -v "${PWD}:/$(Split-Path -Leaf $PWD)" -w "/$(Split-Path -Leaf $PWD)" -p 4040:4040 -p 8501:8501 -p 8888:8888 python-spark:latest
```

### Recomendaciones
- Usa esta imagen como base para proyectos PySpark, ETL y análisis de datos distribuidos.
- Puedes extender este Dockerfile para agregar dependencias adicionales en tu proyecto.
- Consulta la documentación oficial de [Apache Spark](https://spark.apache.org/docs/latest/) para más detalles sobre configuración avanzada.

---

Para más imágenes y entornos, revisa el [README principal](../README.md).
