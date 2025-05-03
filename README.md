# 🐳 Docker-Python-Environments 🐳

## Repositorio de imágenes Docker para entornos Python

Este repositorio es un espacio público para compartir conocimientos sobre construcción y uso de imágenes Docker en entornos Python. Ofrecemos estructuras predefinidas, desde configuraciones minimalistas hasta entornos completos para análisis de datos, todas documentadas con ejemplos prácticos y explicaciones de diseño. 

El objetivo es facilitar la adopción de Docker en proyectos de ciencia de datos y desarrollo, reduciendo la curva de aprendizaje inicial y permitiendo a desarrolladores y científicos de datos aprovechar rápidamente los beneficios de la contenerización.

### Ejemplo de aplicación en PySpark con Streamlit

Como demostración práctica de lo que se puede lograr partiendo de las estructuras organizadas en este repositorio, se incluye una aplicación de ejemplo que utiliza Docker con Python, PySpark y Streamlit. Esta aplicación busca simplemente un caso de uso que muestra cómo aprovechar las imágenes Docker predefinidas para implementar soluciones reales.

#### Estructura del proyecto de ejemplo

```
app.py                # Aplicación Streamlit con PySpark
docker-compose.yml    # Configuración para desplegar la aplicación
Dockerfile            # Imagen Docker para la aplicación
environment.yml       # Dependencias de Conda para el proyecto
```

#### Configuración Docker

El `Dockerfile` principal se basa en `lacamposm/docker-helpers:pyspark-conda-0.1.2` (con Python, Conda, PySpark) y usa `environment.yml` para el entorno Conda. El `docker-compose.yml` gestiona la construcción de la imagen, el mapeo de puertos (8501 Streamlit, 4040 Spark UI), el montaje del código fuente y el inicio de la aplicación Streamlit.

#### Características de la aplicación

Entorno PySpark funcional con capacidad para ejecutar consultas SQL interactivas y visualizar resultados.

<div align="center">
  <img src="images/app_image.png" alt="Ejemplo de la aplicación PySpark con Streamlit" width="350" height="420" />
  <p><strong>Vista previa de la aplicación</strong></p>
</div>

# 🐳 Docker Python Environments - Guía de inicio 🐳

Para comenzar a trabajar con este proyecto, primero debes clonar el repositorio:

```bash
git clone https://github.com/lacamposm/docker-python-envs.git
cd docker-python-envs
```

#### Ejecuta la aplicación usando Docker Compose

- ****

   ```bash
   docker-compose up --build
   ```

La aplicación estará disponible en: http://localhost:8501

---

## Tabla de Contenidos
- [Introducción](#introducción)
- [Usos de Docker en Python](#usos-de-docker-en-python)
- [Conceptos Clave](#conceptos-clave)
- [Ecosistema de imágenes Docker para Python](#ecosistema-de-imágenes-docker-para-python)
- [Desarrollo integrado con VS Code DevContainers](#desarrollo-integrado-con-vs-code-devcontainers)
- [Imagenes en Docker Hub](#imagenes-en-docker-hub)
- [Recomendaciones](#recomendaciones-al-trabajar-con-docker-y-python)
- [Conclusión](#conclusión)

## Introducción

Docker es una plataforma que permite desarrollar, enviar y ejecutar aplicaciones dentro de **contenedores**. Un contenedor es un entorno ligero y aislado que incluye todo lo necesario (código, librerías, dependencias) para que una aplicación funcione de forma consistente en cualquier máquina.

Python es un lenguaje de programación interpretado, de alto nivel y propósito general, conocido por su legibilidad y versatilidad. Es ampliamente utilizado en análisis de datos, inteligencia artificial, desarrollo web, automatización, etc.

La combinación de **Python y Docker** resuelve desafíos comunes como el "funciona en mi máquina", empaquetando la aplicación Python y sus dependencias en un contenedor. Esto asegura un comportamiento uniforme y reproducible en diferentes entornos (desarrollo, pruebas, producción), lo cual es crucial en proyectos científicos y de análisis de datos.

## Usos de Docker en Python

La integración de Docker con Python transforma completamente nuestro flujo de trabajo de desarrollo. En entornos de desarrollo, nos permite crear espacios de trabajo aislados con versiones específicas de Python y las dependencias exactas que nuestro proyecto necesita, evitando conflictos con otros proyectos o con el sistema base. Durante la fase de pruebas y validación, podemos ejecutar nuestras suites de test en contenedores limpios que reproducen fielmente el entorno de producción, garantizando que nuestras pruebas sean verdaderamente representativas sin alterar nuestra configuración local. Finalmente, en la etapa de despliegue, la misma imagen que validamos en desarrollo puede trasladarse directamente a producción, eliminando el tradicional problema de inconsistencias entre entornos y reduciendo drásticamente los errores inesperados tras el despliegue.

## ¿Por qué usar Docker?

Docker ofrece un ecosistema que transforma el desarrollo y despliegue de aplicaciones. Al trabajar con contenedores, conseguimos un completo aislamiento de dependencias que elimina conflictos entre proyectos. La reproducibilidad se vuelve natural, ya que nuestro entorno funciona idénticamente en cualquier máquina, desde desarrollo hasta producción. Además, la arquitectura de Docker facilita la escalabilidad de nuestras soluciones y garantiza portabilidad entre diferentes plataformas, permitiéndonos desplegar nuestras aplicaciones Python sin preocuparnos por la infraestructura subyacente.

## Conceptos Clave

El funcionamiento de Docker se basa en varios componentes fundamentales que trabajan en conjunto. Las imágenes actúan como plantillas inmutables que contienen todo lo necesario para ejecutar nuestras aplicaciones. Cuando ejecutamos una imagen, creamos un contenedor, que es una instancia aislada con su propio sistema de archivos y red. Para construir imágenes personalizadas utilizamos Dockerfiles, archivos de texto con instrucciones específicas sobre cómo configurar el entorno. Una vez creadas, podemos compartir nuestras imágenes a través de registros como Docker Hub, facilitando la colaboración y distribución de nuestros entornos de desarrollo Python.

Más información: [Documentación oficial de Docker - Conceptos](https://docs.docker.com/get-started/overview/)

## Ecosistema de imágenes Docker para Python

Este repositorio ofrece un ecosistema completo de imágenes Docker diseñadas para diferentes necesidades de desarrollo en Python. Cada imagen está pensada para un caso de uso específico, desde entornos minimalistas hasta potentes configuraciones para análisis de datos distribuidos. Todas han sido creadas siguiendo buenas prácticas para garantizar rendimiento y facilidad de uso.

La colección incluye:

- **[Python Minimalista](./python-min/README.md)**: Entorno ligero basado en Python 3.12 para aplicaciones que priorizan la velocidad y el consumo eficiente de recursos. Ideal para microservicios, scripts de automatización y aplicaciones web simples.

- **[Entorno Conda](./conda/README.md)**: Configuración optimizada con Miniconda para ciencia de datos, machine learning y análisis estadístico. Perfecta para proyectos que requieren bibliotecas científicas como NumPy, Pandas, Scikit-learn o TensorFlow con gestión eficiente de dependencias.

- **[Procesamiento Distribuido con Spark](./spark/README.md)**: Entorno completo con Python, Conda y Apache Spark para procesamiento de big data y análisis a gran escala. Preparada para trabajar con datos masivos, transformaciones complejas y aprendizaje distribuido.

- **[Gestión con Poetry](./poetry/README.md)**: Solución moderna para desarrollo de paquetes y aplicaciones Python con Poetry, enfocada en la gestión determinista de dependencias y empaquetado. Excelente para proyectos colaborativos que requieren reproducibilidad exacta.


## Desarrollo integrado con VS Code DevContainers

Para proporcionar una experiencia de desarrollo inmersiva y sin fricciones, hemos implementado una configuración avanzada de VS Code DevContainers que elimina la barrera entre tu editor y el entorno containerizado. Esta integración permite comenzar a programar instantáneamente en un ambiente completamente configurado, con todas las extensiones y herramientas necesarias.

El DevContainer incluye:

1. **Entorno listo para usar**: Con un simple comando, crea un espacio de desarrollo virtual completo y aislado del sistema host:

   ```sh
   docker-compose up --build
   ```

2. **Configuración transparente**: La estructura está organizada de manera intuitiva para facilitar su contexto de construcción desde la raíz del proyecto, haciendo uso del `Dockerfile` principal y dependencias desde `environment.yml`

3. **Acceso fluido**: Conecta con tu entorno de desarrollo desde cualquier terminal:
   ```sh
   docker exec -it pyspark-project bash
   ```

4. **Integración perfecta con VS Code**: Desarrolla dentro del contenedor con la misma experiencia que tendrías en local:
   * Presiona Ctrl+Shift+P → Selecciona _Dev Containers: Rebuild and Reopen in Container_
   * Todas tus extensiones, configuraciones y herramientas sincronizadas automáticamente

**➡️ Descubre todos los detalles de esta potente configuración en el [README de DevContainers](./.devcontainer/README.md).**

## Imagenes en Docker Hub

Las imágenes de ejemplo de este proyecto están disponibles en:  

➡️ https://hub.docker.com/r/lacamposm/docker-helpers


Para publicar y compartir tus imágenes personalizadas, sigue la guía oficial de Docker Hub:
- [Documentación: Publicar imágenes en Docker Hub](https://docs.docker.com/docker-hub/repos/)


## Recomendaciones al Trabajar con Docker y Python

- **Gestión de dependencias:** Usa siempre archivos como `requirements.txt`, `pyproject.toml` o `environment.yml` para instalaciones reproducibles.
- **Conda:** Considera Conda para proyectos científicos con dependencias complejas. Usa imágenes base como `continuumio/miniconda3`.
- **Optimización:** Mantén las imágenes ligeras (minimiza capas, limpia cachés) para reducir tiempos y recursos.
- **Orquestación:** Utiliza [Docker Compose](https://docs.docker.com/compose/) o [Kubernetes](https://kubernetes.io/docs/concepts/overview/) para gestionar aplicaciones con múltiples contenedores (bases de datos, APIs, etc.).

## Conclusión

Docker simplifica el desarrollo, prueba y despliegue de aplicaciones al garantizar entornos consistentes y reproducibles mediante contenedores. Esto elimina el problema de "funciona en mi máquina".

**Ventajas clave:**
- **Uniformidad:** Ejecución idéntica en cualquier lugar.
- **Eficiencia:** Contenedores ligeros y rápidos.
- **CI/CD:** Fácil integración con pipelines automatizados.
- **Microservicios:** Ideal para arquitecturas modulares.

Para desarrolladores Python, Docker resuelve problemas de gestión de versiones y dependencias, estableciendo un flujo de trabajo moderno y robusto. Es una herramienta esencial en DevOps y entornos cloud-native, facilitando procesos eficientes y escalables.