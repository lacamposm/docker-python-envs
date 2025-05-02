# 🐳 Configuración del Contenedor de Desarrollo

Este directorio contiene los archivos de configuración para establecer un entorno de contenedor de desarrollo utilizando la característica Dev Containers de Visual Studio Code. Esto permite un entorno de desarrollo consistente y aislado basado en Docker.

## Resumen de Archivos

*   **[`devcontainer.json`](devcontainer.json)**: El archivo de configuración principal para VS Code Dev Containers. Define cómo se debe construir y configurar el contenedor, incluyendo:
    *   Qué archivo Docker Compose usar (`docker-compose-dev.yml`).
    *   El servicio dentro del archivo Compose al que adjuntarse (`dev-name-project`).
    *   La carpeta del espacio de trabajo dentro del contenedor (`/pyspark-project`).
    *   El usuario con el que ejecutar dentro del contenedor (`dev-user`).
    *   Comandos a ejecutar después de crear el contenedor (`postCreateCommand` para registrar el entorno Conda como un kernel de Jupyter).
    *   Configuraciones específicas de VS Code y extensiones a instalar dentro del contenedor.
    *   Puertos a reenviar desde el contenedor a la máquina anfitriona.

*   **[`docker-compose-dev.yml`](docker-compose-dev.yml)**: Define los servicios Docker para el entorno de desarrollo. En este caso, configura el servicio `dev-name-project`:
    *   Especifica el contexto de construcción y el Dockerfile (`../` y `.devcontainer/Dockerfile.dev`).
    *   Mapea puertos para varios servicios (Streamlit, Depuración, Jupyter, Spark UI).
    *   Monta el directorio del proyecto (`../`) en `/my-project-dir` dentro del contenedor.
    *   Establece variables de entorno, incluyendo `PYTHONPATH`.
    *   Usa `tail -f /dev/null` como comando para mantener el contenedor ejecutándose indefinidamente.

*   **[`Dockerfile.dev`](Dockerfile.dev)**: Describe los pasos para construir la imagen Docker utilizada para el contenedor de desarrollo.
    *   Comienza desde una imagen base (`lacamposm/docker-helpers:pyspark-conda-0.1.1-dev`).
    *   Establece el directorio de trabajo en `/pyspark-project`.
    *   Copia el archivo de entorno Conda (`environment.dev.yml`).
    *   Crea un entorno Conda llamado `pyspark-project-dev` a partir del archivo YAML.
    *   Configura un usuario no root (`dev-user`) para una mejor seguridad y gestión de la propiedad.
    *   Configura el `.bashrc` del usuario para activar automáticamente el entorno Conda.
    *   Copia el código del proyecto en el contenedor.
    *   Expone los puertos necesarios.

*   **[`environment.dev.yml`](environment.dev.yml)**: Un archivo de entorno Conda que especifica la versión de Python y las dependencias necesarias para el entorno de desarrollo. Esto incluye:
    *   Bibliotecas principales como `python`, `pip`, `streamlit`, `pyspark`.
    *   Herramientas de desarrollo instaladas a través de pip: `debugpy` (depuración), `jupyter` (notebooks), `sphinx` (documentación), `black` (formateo).

*   **[`notebook_in_devcontainer.ipynb`](notebook_in_devcontainer.ipynb)**: Un cuaderno Jupyter de ejemplo destinado a ejecutarse dentro del Dev Container para probar la configuración del entorno, particularmente la activación del entorno Conda y la disponibilidad de paquetes.

## Cómo Usar

1.  Asegúrate de tener instalados Docker y la extensión VS Code Dev Containers.
2.  Abre la carpeta raíz de este proyecto (`docker-multitask-envs`) en VS Code.
3.  VS Code debería detectar la configuración `.devcontainer` y pedirte "Reopen in Container" (Reabrir en Contenedor). Haz clic en él.
4.  Alternativamente, abre la paleta de comandos (Ctrl+Shift+P) y ejecuta "Dev Containers: Rebuild and Reopen in Container" (Contenedores de Desarrollo: Reconstruir y Reabrir en Contenedor).
5.  VS Code construirá la imagen Docker (si no está ya construida) e iniciará el contenedor definido en `docker-compose-dev.yml`.
6.  Tu instancia de VS Code se conectará entonces al contenedor en ejecución, proporcionándote una terminal y un entorno configurados según los archivos de este directorio.