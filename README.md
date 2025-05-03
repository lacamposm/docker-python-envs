# 🐳 Docker-Python-Environments 🐳

## Ejemplo de aplicación en PySpark con Streamlit

Este repositorio incluye una aplicación de ejemplo que demuestra el uso práctico de Docker con Python, PySpark y Streamlit. La aplicación está configurada para ejecutarse fácilmente usando Docker Compose y basada en una imagen con `spark` ya configurada.

### Cómo clonar este repositorio

Para comenzar a trabajar con este proyecto, primero debes clonar el repositorio:

```bash
# Clonar el repositorio
git clone https://github.com/lacamposm/docker-python-envs.git

# Ingresar al directorio del proyecto
cd docker-python-envs
```

Si deseas trabajar con una rama específica:

```bash
# Listar todas las ramas disponibles
git branch -a

# Cambiar a la rama ejemplo (con la aplicación Streamlit)
git checkout feature/example-use
```

### Estructura del proyecto de ejemplo

```
app.py                # Aplicación Streamlit con PySpark
docker-compose.yml    # Configuración para desplegar la aplicación
Dockerfile            # Imagen Docker para la aplicación
environment.yml       # Dependencias de Conda para el proyecto
```

### Características de la aplicación

- **Verificación del entorno PySpark**: Comprueba que PySpark funciona correctamente
- **Consultas SQL interactivas**: Permite ejecutar consultas Spark SQL desde la interfaz web
- **Visualización de datos**: Muestra resultados en tablas interactivas

### Vista previa de la aplicación

![Ejemplo de la aplicación PySpark con Streamlit](images/app_image.png)

### Cómo ejecutar la aplicación

1. **Usando Docker Compose** (recomendado):

   ```bash
   docker-compose up --build
   ```

   La aplicación estará disponible en: http://localhost:8501

2. **Construyendo manualmente**:

   ```bash
   # Construir la imagen
   docker build -t my-project-sol .
   
   # Ejecutar el contenedor
   docker run -it --rm -p 8501:8501 -p 4040:4040 -v "$(pwd)":/my-project-dir -w /my-project-dir my-project-sol bash -lc "streamlit run app.py"
   ```

### Detalles del Dockerfile

El Dockerfile principal utiliza la imagen base `lacamposm/docker-helpers:pyspark-conda-0.1.1` que incluye Python, Conda y PySpark preconfigurados. La aplicación se ejecuta en un entorno Conda definido en `environment.yml`.

### Estructura de docker-compose.yml

El archivo docker-compose.yml configura:
- Construcción automática de la imagen
- Mapeo de puertos (8501 para Streamlit, 4040 para la UI de Spark)
- Montaje de volúmenes para el código fuente
- Variables de entorno necesarias
- Comando para iniciar la aplicación Streamlit

---

# 🐳 Docker Python Environments - Guía Completa 🐳

## Tabla de Contenidos
- [Introducción](#introducción)
  - [¿Qué es Docker?](#qué-es-docker)
  - [¿Qué es Python?](#qué-es-python)
  - [Python y Docker](#python-y-docker)
- [¿Por qué usar Docker?](#por-qué-usar-docker)
- [Conceptos Clave](#conceptos-clave)
- [Principales Comandos de Docker](#principales-comandos-de-docker)
  - [Comandos Detallados](#comandos-detallados)
- [Imágenes disponibles y uso](#imágenes-disponibles-y-uso)
- [Usos de Docker en Python](#usos-de-docker-en-python)
- [Desarrollo con VS Code DevContainer](#desarrollo-con-vs-code-devcontainer)
- [Publicación de imágenes en Docker Hub](#publicar-la-imagen-en-docker-hub)
- [Recomendaciones](#recomendaciones-al-trabajar-con-docker-y-python)
- [Conclusión](#conclusión)


### ¿Qué es Docker?

Docker es una plataforma que permite desarrollar, enviar y ejecutar aplicaciones dentro de contenedores. Un contenedor es un entorno ligero y aislado que contiene todo lo necesario para que una aplicación funcione de forma consistente en cualquier lugar.

### ¿Qué es Python?

Python es un lenguaje de programación interpretado, de alto nivel y propósito general conocido por su legibilidad y versatilidad. Su filosofía de diseño enfatiza la simplicidad y la legibilidad del código, lo que permite a los desarrolladores expresar conceptos en menos líneas que en otros lenguajes. Python es ampliamente utilizado en análisis de datos, inteligencia artificial, desarrollo web, automatización, y prácticamente en cualquier campo de la programación.

### Python y Docker

La combinación de Python y Docker resuelve muchos desafíos comunes en el desarrollo de software. Python, con su diversidad de versiones y dependencias, a menudo enfrenta el problema de "funciona en mi máquina". Docker soluciona esto al empaquetar la aplicación Python junto con todas sus dependencias en un contenedor, asegurando un comportamiento uniforme en diferentes entornos. Esta combinación es particularmente valiosa para equipos que trabajan en proyectos científicos o soluciones de analitica de datos, donde la consistencia del entorno es crucial para obtener resultados reproducibles.

## ¿Por qué usar Docker?

- **Aislamiento**: Cada contenedor cuenta con sus propias dependencias y librerías, evitando conflictos con otras aplicaciones.  
- **Reproducibilidad**: Las aplicaciones se ejecutan de la misma manera indistintamente del sistema operativo anfitrión.  
- **Escalabilidad**: Es sencillo replicar un contenedor y desplegarlo en distintos entornos sin configuraciones extra.  
- **Portabilidad**: Se puede exportar e importar contenedores sin importar la infraestructura subyacente.

## Conceptos Clave

- **Imagen**: Conjunto de capas que incluyen el sistema de archivos y la configuración necesarios para ejecutar un contenedor.
- **Contenedor**: Instancia de una imagen que se ejecuta de forma aislada y que puede crearse, iniciarse o detenerse fácilmente.
- **Dockerfile**: Archivo que describe cómo se construye una imagen (instalación de paquetes y configuraciones).
- **Registro de imágenes**: Repositorio donde se almacenan y comparten imágenes de Docker (ej. Docker Hub).

> Más información: [Documentación oficial de Docker - Conceptos](https://docs.docker.com/get-started/overview/)

## Principales Comandos de Docker

Comandos básicos para trabajar con Docker:

- `docker pull <imagen>`: Descarga una imagen desde un registro.
- `docker run <imagen>`: Crea y ejecuta un contenedor basado en la imagen.
- `docker ps`: Lista los contenedores en ejecución.
- `docker stop <contenedor>`: Detiene un contenedor en ejecución.
- `docker rm <contenedor>`: Elimina un contenedor detenido.
- `docker build -t <nombre_imagen> .`: Construye una imagen desde un Dockerfile.

### Comandos Detallados

1. `docker pull <imagen>`: Descarga una imagen desde un registro.  
   - `--all-tags, -a`: Descarga todas las etiquetas disponibles de la imagen.
2. `docker run <imagen>`: Crea y ejecuta un contenedor basado en la imagen indicada.  
   - `--detach, -d`: Ejecuta el contenedor en segundo plano.  
   - `-it`: Permite una terminal interactiva.  
   - `--volume, -v`: Monta un volumen.  
   - `--name`: Asigna un nombre personalizado al contenedor.  
   - `--rm`: Elimina automáticamente el contenedor cuando se detiene.
3. `docker ps`: Lista los contenedores en ejecución.  
   - `--all, -a`: Muestra todos los contenedores (no solo los activos).
4. `docker stop <contenedor>`: Detiene un contenedor en ejecución.  
   - `--time, -t`: Segundos a esperar antes de forzar la detención.
5. `docker rm <contenedor>`: Elimina un contenedor que ya se ha detenido.  
   - `--force, -f`: Fuerza la eliminación de un contenedor en ejecución.
6. `docker build -t <nombre_imagen> .`: Construye una imagen usando un Dockerfile presente en el directorio actual.  
   - `--no-cache`: No usa la caché durante la construcción.  
   - `--file, -f`: Nombre del Dockerfile (por defecto es 'Dockerfile').

> Consulta la [documentación oficial de Docker - Referencia de comandos](https://docs.docker.com/engine/reference/commandline/docker/) para más detalles y ejemplos.

## Imágenes disponibles y uso

Para instrucciones detalladas sobre cada imagen Docker, consulta el README correspondiente en cada carpeta:

- [python-min/README.md](./python-min/README.md): Imagen mínima de Python 3.12 para entornos ligeros.
- [conda/README.md](./conda/README.md): Imagen basada en Miniconda para entornos científicos y de análisis de datos.
- [poetry/README.md](./poetry/README.md): Imagen con Python y Poetry para gestión de dependencias.
- [spark/README.md](./spark/README.md): Imagen con Python, Conda y Apache Spark para procesamiento distribuido de datos.

## Usos de Docker en Python

- **Entornos de desarrollo**: Facilita la creación de entornos personalizados que incluyan la versión de Python y las dependencias necesarias para cada proyecto.  
- **Pruebas y validación**: Se pueden ejecutar tests en contenedores limpios, reproduciendo condiciones idénticas sin afectar la configuración del sistema local.  
- **Despliegue en producción**: Una vez validada la aplicación, se despliega el mismo contenedor en el entorno de producción, lo que reduce los errores por diferencias de configuración.  

## Desarrollo con VS Code DevContainer

Para facilitar el desarrollo aislado con VS Code, se provee un DevContainer configurado en la carpeta `.devcontainer`:

1.  **Construir y levantar** el contenedor con Docker Compose:

    ```sh
    docker compose -f .devcontainer/docker-compose-dev.yml up --build
    ```

2.  **Contexto y Dockerfile** usados:
    *   Contexto: `.` (directorio raíz del proyecto)
    *   Dockerfile: `.devcontainer/Dockerfile.dev`
    *   Archivo de entorno: `.devcontainer/environment.dev.yml`

3.  **Acceder** al contenedor:
    ```sh
    docker exec -it dev-name-project bash
    ```

4.  **Reabrir en contenedor** desde VS Code (guía rápida):
    *   Ctrl+Shift+P → _Dev Containers: Rebuild and Reopen in Container_

**➡️ Para más detalles sobre la configuración del Dev Container, consulta el [README específico de .devcontainer](./.devcontainer/README.md).**

## Publicar la Imagen en Docker Hub

Para publicar y compartir tus imágenes personalizadas, sigue la guía oficial de Docker Hub:
- [Documentación: Publicar imágenes en Docker Hub](https://docs.docker.com/docker-hub/repos/)

Imágenes de ejemplo de este proyecto están disponibles en:  
➡️ https://hub.docker.com/r/lacamposm/docker-helpers

Los pasos generales son:
1. Inicia sesión con `docker login`.
2. Etiqueta tu imagen con tu usuario de Docker Hub.
3. Sube la imagen con `docker push`.
4. Descárgala en cualquier máquina con `docker pull`.

Consulta la documentación oficial para detalles y mejores prácticas.

## Recomendaciones al Trabajar con Docker y Python

- Incluir siempre un archivo con las dependencias (por ejemplo, `requirements.txt`, `pyproject.toml` o `environment.yml` para Conda) para que la instalación sea clara y reproducible.
- Considerar Conda como alternativa para gestionar entornos Python dentro de contenedores, especialmente para proyectos científicos o con dependencias complejas.
- Al usar Conda con Docker, preferir imágenes base como `continuumio/miniconda3` que ya incluyen el sistema de gestión de paquetes preinstalado.  
- Mantener las imágenes lo más ligeras posible para disminuir tiempos de descarga y consumo de recursos.  
- Usar herramientas de orquestación como Docker Compose o Kubernetes para coordinar varios contenedores (ej. bases de datos, servidores web, etc.).  

## Comentario

Docker ha transformado radicalmente la forma en que desarrollamos, probamos y desplegamos aplicaciones, tanto en Python como en otros lenguajes. Al encapsular cada entorno en contenedores, se garantiza una ejecución uniforme y predecible en cualquier plataforma, eliminando de raíz el clásico problema de "en mi máquina funciona". 

### Ventajas Destacadas

- **Uniformidad**: Garantiza ejecución idéntica en cualquier plataforma, simplificando la depuración.
- **Eficiencia**: Contenedores más ligeros y rápidos que máquinas virtuales, optimizando recursos.
- **CI/CD**: Integración fluida con pipelines de desarrollo automatizado.
- **Microservicios**: Facilita arquitecturas modulares con componentes independientes.
- **Persistencia**: Mediante volúmenes, separa código inmutable de datos persistentes.

Para los desarrolladores de Python, Docker no solo resuelve problemas históricos relacionados con la gestión de versiones y conflictos de dependencias, sino que establece un flujo de trabajo moderno y robusto. En un mundo cada vez más orientado hacia infraestructuras cloud-native y metodologías ágiles, Docker se consolida como una herramienta esencial en el ecosistema DevOps, facilitando procesos de desarrollo más eficientes, colaborativos y escalables.