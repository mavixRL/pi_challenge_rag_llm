# Proyecto Challenge RAG con LLM

Introduction
------------
Este proyecto consiste en desarrollar una solución basada en la generación de respuestas aumentadas (RAG) mediante el uso de modelos de lenguaje de gran escala (LLMs). El enfoque principal es proporcionar una interacción eficiente y precisa entre el usuario y el modelo, permitiendo obtener respuestas contextuales y relevantes a partir de documentos específicos. La solución implicará la creación de una API que servirá de puente entre el usuario y el LLM.

Desarrollado por Mavix Arias Aguila [https://www.linkedin.com/in/mavix-arias-aguila/]

## Contenido
1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Tecnologias](#tecnologias)
3. [Configuración del Entorno Local](#configuración-del-entorno-local)
    1. [Clonar el repositorio](#clonar-el-repositorio)
    2. [Crear entorno virtual](#crear-entorno-virtual)
    3. [Instalar Dependencias](#instalar-dependencias)
    4. [Inicializar Aplicación](#inicializar-aplicación)
4. [Documentación de la API](#documentación-de-la-api)
5. [Implementación con Docker(Opcional)](#implementación-con-docker(opcional))

## Estructura del Proyecto

```
challenge_rag_llm/
│          
├── app/
│   ├── api/                 # Contiene controladores/routers/schemas/logging
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── ask_cohere.py
│   │   │   ├── ask_openai.py
│   │   │   └── root.py
│   ├── config/
│   │   ├── services/
│   │   │   └── cohere_services.yaml
│   │   ├── test/
│   │   │   └── test_unit.yaml
│   ├── core/
│   │   ├── init.py
│   │   └── config.py
│   ├── db/
│   ├── ChromaDB/
│   │   │   ├── 9c989208-a74c-4934-9e41-5999ad224932/
│   │   │   │   ├── data_level0.bin
│   │   │   │   ├── header.bin
│   │   │   │   ├── length.bin
│   │   │   │   └── link_list.bin
│   │   │   ├── a83eaa7f-fd5b-4339-a258-3254f1a016e4/
│   │   │   │   ├── data_level0.bin
│   │   │   │   ├── header.bin
│   │   │   │   ├── length.bin
│   │   │   │   └── link_list.bin
│   │   │   └── chroma.sqlite3
│   │   └── database.py
│   ├── logs/
│   │   └── test_unit.log
│   ├──models/                    # Contiene los schemas de la aplicación
│   │   ├── __init__.py
│   │   └── user_request.py
│   ├── Notebooks/
│   │   ├── Analisis_token.ipynb
│   │   ├── ChromaDB.ipynb
│   │   ├── crear_db_con_ChromaDB.ipynb
│   │   └── crear_db_con_ChromaDB.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cohere_service.py
│   │   ├── context_service.py
│   │   └── openai_service.py.py
│   ├── test/
│   │   ├── e2e/
│   │   │   └── test_end_to_end.py.py
│   │   ├── integration/
│   │   │   └── test_integration.py
│   │   └── unit/
│   │       ├── test_unit_api.py
│   │       └── test_unit_db.py
│   ├── utils/
│   │   ├── format_logger.py
│   │   ├── funcions_general.py
│   │   └── utils.py
│   ├── __init__.py
│   └── main.py
├── docs/                    # Documentación del proyecto
│   ├── challenge_ ai_engineer.pdf
│   ├── documento.docx
│   └── tutorial_chroma.ipynb
├── requirements/            # Archivos de requerimientos
│   ├── base.txt             # basic requisite dependencies for running the API service.
│   ├── dev.txt              # dependencies for the local development.
│   └── doc.txt              # dependencies for creating sphinx documentation.
├──.env
├── .gitignore
├── Dockerfile
├── Pi_Challenge_RAG_LLM Collection.postman_collection.json
└── README.md
```
## Tecnologias

- **Python version**: 3.9 o superior
- **Framework**: FastAPI
- **Database**: ChromaDB
- **LLM**: Cohere y OpenAI
## Configuración del Entorno Local

### Clonar el repositorio

```bash
git clone <repository_url>
cd pi_challenge
```

### Crear entorno virtual

```bash
# Crear un entorno virtual
python -m venv nombre_entorno_virtual

# Activar entorno virtual (Windows)
.\nombre_entorno_virtual\Scripts\activate

# Activar entorno virtual (macOS/Linux)
source nombre_entorno_virtual/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Inicializar aplicación

```bash
uvicorn app.main:app --reload
```
La aplicación debería estar corriendo en http://127.0.0.1:8000.

Al iniciar la aplicación, se crearán dos archivos en la raíz del proyecto: `logger.log`, que contendrá los registros del proyecto, y `pi.db`, que será la base de datos de la aplicación.

## Documentación de la API

Esta sección te redirige a Swagger UI, donde puedes interactuar dinámicamente con tu API y explorar sus endpoints y parámetros.

- Accede a Swagger UI en `/docs`

La URL para Swagger UI es: http://127.0.0.1:8000/docs
----------
## Implementación con Docker(Opcional)

### Construir imagen de Docker

```bash
docker build -t pi_challenge .
```

### Inicializar contenedor Docker 

```bash
docker run -p 80:80 pi_challenge
```
Configuration
+++++++++++++

GitHub Actions
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Stage
     - Description
     - TODOs
     - Enabled
   * - linting
     - Linting check with `flake8`_, `mypy`_, `bandit`_.
     -
     - Yes
   * - test
     - Run tests with `pytest`_ and generate coverage report.
     -
     - Yes
   * - build
     - Build docker images and push them to docker registry.
     - Docker login credentials.
     - Yes

CI/CD Variables
~~~~~~~~~~~~~~~
To make sure that the CI/CD pipeline runs successfully, there are some CI/CD variables need to be set in repository settings.

.. list-table::
   :header-rows: 1

   * - Environment Variable
     - Description
   * - MODE
     - Run the API service in which MODE ("DEV", "TEST", "PROD").
   * - DB_CONNECTION
     - Postgres DB URI for building docker image.
   * - DOCKER_REGISTRY_USERNAME
     - Username of docker registry to login.
   * - DOCKER_REGISTRY_TOKEN
     - Token of docker registry to login.
   

Makefile
~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Command
     - Description
   * - clean
     - Remove autogenerated folders and artifacts.
   * - clean-pyc
     - Remove python artifacts.
   * - clean-build
     - Remove build artifacts.
   * - bandit
     - Install and run `bandit`_ security analysis.
   * - mypy
     - Install and run `mypy`_ type checking.
   * - flake8
     - Install and run `flake8`_ linting.
   * - test
     - Run tests and generate coverage report.

How to Use
++++++++++

Dependencies
~~~~~~~~~~~~

THh dependencies are listed in files from folder `requirements`:

+ `base.txt`: basic requisite dependencies for running the API service.
+ `dev.txt`: dependencies for the local development, linting checks, unit tests.
+ `doc.txt`: dependencies for creating sphinx documentation.


You can install them via::

    $ pip install -r requirements/<file name>

Run API Service
~~~~~~~~~~~~~~~

Please check the section `Running the API Service locally <./docs/source/02_usage.rst>`_ for detailed information.

Run Tests
~~~~~~~~~

Please check the section `Running Tests locally <./docs/source/02_usage.rst>`_ for detailed information.

Build Sphinx Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Please check the section `Building Sphinx Documentation locally <./docs/source/02_usage.rst>`_ for detailed information.

API Endpoints
+++++++++++++

.. list-table::
   :header-rows: 1

   * - Endpoints
     - Description
   * - **/api/v1/version**
     - API Service version information
   * - **/docs**
     - Open API documentation
   * - **/api/v1/openapi.json**
     - Open API information in json format

Maintainers
-----------

..
    TODO: List here the people responsible for the development and maintaining of this project.
    Format: **Name** - *Role/Responsibility* - Email

* **Mvx** - *Maintainer* - `mavixarias@gmail.com <mailto:mavixarias@gmail.com?subject=[GitHub]Challenge%20RAG%20con%20LLM>`_

.. _bandit: https://bandit.readthedocs.io/en/latest/
.. _mypy: https://github.com/python/mypy
.. _flake8: https://gitlab.com/pycqa/flake8
.. _pytest: https://docs.pytest.org/en/stable/
