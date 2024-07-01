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
git clone https://github.com/mavixRL/pi_challenge_rag_llm.git
cd pi_challenge_rag_llm
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
pip install -r requirements/base.txt
```

### Inicializar aplicación

```bash
uvicorn app.main:app --host localhost --port 8003 --reload
```
La aplicación debería estar corriendo en http://127.0.0.1:8003.

Al iniciar la aplicación, se crearán dos archivos en la raíz del proyecto: `logger.log`, que contendrá los registros del proyecto, y `pi.db`, que será la base de datos de la aplicación.

## Documentación de la API

Esta sección te redirige a Swagger UI, donde puedes interactuar dinámicamente con tu API y explorar sus endpoints y parámetros.

- Accede a Swagger UI en `/docs`

La URL para Swagger UI es: http://127.0.0.1:8003/docs (solo de los endpoints de la API)

La documentacion general de todos los modulos se encuentra en la carperta **docs/app/index.html**


##  Mensaje de Bienvenida en la API

  http://localhost:8003/api/

  ```bash
 {
    "mensaje": "Bienvenido a la  API. Desarrollado por Mavix Arias Aguila",
    "message": "Welcome to the API. Developed by Mavix Arias Aguila"
}
  ```
----------
## Implementación con Docker(Opcional)

### Construir imagen de Docker

```bash
docker build -t pi_challenge .
```

### Inicializar contenedor Docker

```bash
docker run -p 8003:8003 pi_challenge
```

## El Prompt de Cohere

El prompt de Cohere es el siguiente:
El prompt utilizado consiste en ingresar un chat_history con los requerimientos de la respuesta  y el contexto.

El contexto es obtenido a partir del calculo de la similitud de coseno entre los embedding de la pregunta y el contexto.
Luego se obtiene el idioma del query por medio del siguente prompt:
```bash
 chat_history=[
        {
            "role": "SYSTEM",
            "message": f"""Eres un detector muy preciso de idiomas,dime el idioma en una sola palabra (es, en, pt) de la siguiente pregunta : """,  # noqa
        },
    ],
    message=f"""Cual es el idioma del texto?:
{query}""",
...
```
Da como respuesta 
```bash
en es o pt
```
Se omitio el uso de librerias de deteccion de idiomas por las limitaciones de las mismas.

Adicionalmente se tiene un verificador de consulta que es basicamente si la similaridad tiene un valor por debajo de **0.43** se considera que la pregunta no es sobre el documento y se da una respuesta generica (**no_data_msg**).

```bash
no_data_msg:
  es: La pregunta no está relacionada con el documento.
  en: The question is not related to the document.
  pt: A pergunta não está relacionada com o documento.

```

con el query, idioma, y contexto se genera el prompt para obtener la respuesta.

```bash
    dict_important1 = {
        "es": "Debes ser lo más conciso y preciso posible en la entrega de información (20 palabras o menos) y traducir tu respuesta si es necesario a partir del siguiente contexto:",
        "en": "You must be as concise and precise as possible in delivering information (20 words or less) and translate your response if necessary from the following context:",
        "pt": "Você deve ser o mais conciso e preciso possível na entrega de informações (20 palavras ou menos) e traduzir sua resposta, se necessário, a partir do seguinte contexto:",
    }

    dict_important2 = {
        "es": "Responde en una sola oración, en el mismo idioma que la pregunta, incluyendo emojis que resuman el contenido de la respuesta, y siempre en tercera persona.",
        "en": "Answer in one sentence, in the same language as the question, including emojis that summarize the content of the answer, and always in third person.",
        "pt": "Responda em uma frase, no mesmo idioma da pergunta, incluindo emojis que resumam o conteúdo da resposta, e sempre na terceira pessoa.",
    }
    dict_important3 = {
        "es": "Responde en español, si el texto esta en español traduce la respuesta al español.",
        "en": "Answer in English, if the text is in español, translate the answer to English.",
        "pt": "Responda em português, se o texto estiver em español, traduza a resposta para o português.",
    }

    response = co.chat(
        chat_history=[
            {
                "role": "SYSTEM",
                "message": f"""{dict_important1[language]}
            {contexto}
            NOTA IMPORTANTE:
            {dict_important2[language]}

            """,
            },
        ],
        message=f"""{query} {dict_important3[language]}""",

  ```
  por ejemplo si el query es:
  ```bash
  query = "Quien es Zara?"
  ```
  EL prompt seria:
  ```bash
  history_chat:
  """ You must be as concise and precise as possible in delivering information (20 words or less) and translate your response if necessary from the following context:
  Ficción Espacial: En la lejana galaxia de Zenthoria, dos civilizaciones alienígenas, los Dracorians y los Lumis, se encuentran al borde de la guerra intergaláctica. Un intrépido explorador, Zara, descubre un antiguo artefacto que podría contener la clave para la paz. Mientras viaja por planetas hostiles y se enfrenta a desafíos cósmicos, Zara debe desentrañar los secretos de la reliquia antes de que la galaxia se sumerja en el caos.
  NOTA IMPORTANTE:
  Answer in one sentence, in the same language as the question, including emojis that summarize the content of the answer, and always in third person."""
  mensaje:

  """Quien es Zara? Answer in English, if the text is in español, translate the answer to English."""

  ```

Y la respuesta seria:

Zara is an intrepid explorer on a mission to unravel the mysteries of an ancient artifact that holds the key to intergalactic peace. 🚀",


y por ultmimo se almacena la respuesta, el nombre del usuario y el query en la base de datos para en caso se solicite la misma pregunta buscar en la base de datos y no hacer la consulta al modelo. Evitando en cierta medida el problema de reproducibilidad de los modelos de lenguaje que a pesar de poner temperatura 0 dan respuestas diferentes por su naturaleza probabilistica.


## Pruebas Unitarias

Para ejecutar las pruebas unitarias, ejecute el siguiente comando:

```bash
python -m app.tests.unit.test_unit_api
```
Tener en cuenta que en caso se encuntre algun error hay que revisar el archivo **test_unit_api.py** y el archivo 
**app\config\test\test_unit.yaml**
Donde se define las respuestas que deberian dar los modelos de lenguaje