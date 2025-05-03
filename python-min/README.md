# Python 3.12 Minimal Docker Image

Este directorio contiene una imagen Docker minimalista basada en Python 3.12, diseñada para entornos ligeros y eficientes.

## Contenido
- `Dockerfile`: Imagen base con Python 3.12 y entorno virtual
- `requirements.txt`: Dependencias mínimas (jupyter, ipykernel)

## Características principales
- Basada en la imagen oficial `python:3.12-slim`
- Configuración de entorno virtual para aislamiento de dependencias
- Soporte para Jupyter Notebook con kernel personalizado
- Mínima huella de almacenamiento para despliegues eficientes
- Ideal para scripts, microservicios y aplicaciones web ligeras

## Ejemplo de uso

### Construir la imagen

```bash
# Desde el directorio raíz del proyecto
docker build -t python3.12-slim -f ./python-min/Dockerfile .
```

### Ejecutar el contenedor

```bash
# Linux/MacOS
docker run -it --rm -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python3.12-slim:latest

# Windows PowerShell
docker run -it --rm -v "${PWD}:/$(Split-Path -Leaf $PWD)" -w "/$(Split-Path -Leaf $PWD)" python3.12-slim:latest
```

### Iniciar Jupyter Notebook

```bash
# Linux/MacOS
docker run -it --rm -p 8888:8888 -v "$(pwd)":/$(basename "$(pwd)") -w /$(basename "$(pwd)") python3.12-slim:latest jupyter notebook --ip 0.0.0.0 --no-browser --allow-root

# Windows PowerShell
docker run -it --rm -p 8888:8888 -v "${PWD}:/$(Split-Path -Leaf $PWD)" -w "/$(Split-Path -Leaf $PWD)" python3.12-slim:latest jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

### Recomendaciones
- Usa esta imagen para proyectos que requieran un entorno Python limpio y ligero
- Personaliza el archivo `requirements.txt` para incluir solo las dependencias necesarias
- Ideal para CI/CD, microservicios y entornos donde el rendimiento y el tamaño importan
- Extiende el Dockerfile si necesitas agregar herramientas específicas para tu proyecto

---

Para más imágenes y entornos, revisa el [README principal](../README.md).
