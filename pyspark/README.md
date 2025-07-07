# Docker Python Spark Environment

Este directorio contiene la imagen Docker para entornos de procesamiento distribuido con Python, Conda y Apache Spark.

## Contenido
- `Dockerfile`: Imagen base con Python 3.12.8, Miniconda y Spark 3.5.5

## Características principales
- Basada en la imagen oficial `continuumio/miniconda3:24.11.1-0`
- Incluye Apache Spark 3.5.5 y OpenJDK 17
- Expone el puerto para Spark UI (4040)
- Preparada para proyectos de análisis de datos distribuidos y aplicaciones PySpark

## Ejemplo de uso

### Construir la imagen

```bash
# Desde el directorio de pyspark
docker build -t lacamposm/docker-helpers:pyspark-conda-0.1.3 .
```

### Ejecutar el contenedor

```bash
# Linux/MacOS
docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") -p 4040:4040 lacamposm/docker-helpers:pyspark-conda-0.1.3

# Windows PowerShell
docker run -it --rm -v "${PWD}:/$(Split-Path -Leaf $PWD)" -w "/$(Split-Path -Leaf $PWD)" -p 4040:4040 lacamposm/docker-helpers:pyspark-conda-0.1.3
```

### Desde DockerHub

La imagen está disponible en DockerHub y puede ser descargada directamente:

```bash
docker pull lacamposm/docker-helpers:pyspark-conda-0.1.3
```

### Verificar la instalación

Para comprobar que Spark y Python están correctamente instalados:

```bash
docker run -it --rm lacamposm/docker-helpers:pyspark-conda-0.1.3 /bin/bash -c "spark-submit --version && python -V"
```

Debería mostrar la versión de Spark 3.5.5 y Python 3.12.8.

### Recomendaciones

- Usa esta imagen como base para proyectos PySpark, ETL y análisis de datos distribuidos.
- Puedes extender este Dockerfile para agregar dependencias adicionales en tu proyecto.
- Consulta la documentación oficial de [Apache Spark](https://spark.apache.org/docs/latest/) para más detalles sobre configuración avanzada.

---

Para más imágenes y entornos, revisa el [README principal](../README.md).
