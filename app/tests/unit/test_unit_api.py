"""
    Este módulo contiene las pruebas unitarias de las funciones del módulo cohere_service.

"""

# omitir print de  Traceback
# from app.core.config import settings
from app.services.cohere_service import (
    detect_language,
    generate_response,
    get_context,
    get_response,
)
from app.utils.format_logger import def_log
from app.utils.funcions_general import ConfigManager

log = def_log(path_log="./app/logs/", file="test_unit.log")

config = ConfigManager(config_paths=["./app/config/test/test_unit.yaml"])


def test_get_context():
    """
    Description:
    ------------
        Esta función realiza pruebas unitarias de la función get_context del módulo cohere_service.
        Genera un log con el resultado de las pruebas.
        Usa las variables de configuración del archivo config/test_unit.yaml

    Returns:
    --------
        - None

    """
    log.name = "test_get_context"
    query = config.get(["test_get_context", "query"])
    context = get_context(query, n_results=1)
    try:
        assert context is not None, "El contexto es None"
        assert (
            "documents" in context[0]
        ), "La clave 'documents' no está en el contexto[0]"
        assert len(context[0]["documents"]) > 0, "La lista de documentos está vacía"
        assert context[0]["documents"][0][0] == config.get(
            ["test_get_context", "context"]
        ), "El contenido del documento no coincide"
        log.info("[PASS]: Test test_get_context passed successfully")
    except AssertionError as e:
        msj = f"[ERROR]: {e}"
        log.error(msj)
        log.debug(f"query: {query}")
        log.debug(f"context: {context}")

    except Exception as e:
        msj = f"[ERROR]{e}"
        log.error(msj)
        log.debug(f"query: {query}")
        log.debug(f"context: {context}")


def test_detect_language():
    """
    Función que realiza pruebas de detección de idioma
    Description:
    ------------
    Esta función recibe un diccionario con preguntas y su respectivo idioma y devuelve un mensaje de éxito si las pruebas pasan.
    la variable test_language_data es un diccionario con preguntas y su respectivo idioma se encuentra en el config_test.yaml.
    """
    log.name = "test_detect_language"
    test_language_data = config.get(["test_detect_language", "language_data"])
    try:
        for query, language in test_language_data.items():
            # print(query)
            # print(language)
            lang = detect_language(language)
            assert language is not None, "El lenguaje detectado es None"
            assert language == lang, "El lenguaje detectado no coincide"
        log.info("[PASS]: Test test_detect_language passed successfully")
    except AssertionError as e:
        msj = f"[ERROR]: {e}"
        log.error(msj)
        # Mostrar el contenido de las variables para debug
        log.debug(f"query: {query}")
        log.debug(f"language detected: {lang}")
    except Exception as e:
        msj = f"[ERROR]{e}"
        log.error(msj)
        # Mostrar el contenido de las variables para debug
        log.debug(f"query: {query}")
        log.debug(f"language detected: {lang}")


def test_generate_response():
    """
    Description:
    ------------
        Esta función realiza pruebas unitarias de la función generate_response del módulo cohere_service.
        Genera un log con el resultado de las pruebas.
        Usa las variables de configuración del archivo config/test_unit.yaml
    """
    log.name = "test_generate_response"
    query = config.get(["test_get_context", "query"])
    context = config.get(["test_get_context", "context"])
    response = generate_response(query, context)

    # print(response)

    try:
        assert response is not None, "La respuesta es None"
        # comentado porque no se requeire que sea igual solo que genera una respuesta
        # assert response == config.get(['test_generate_response','response']), "La respuesta no coincide"
        log.info("[PASS]: Test test_generate_response passed successfully")
    except AssertionError as e:
        msj = f"[ERROR]: {e}"
        log.error(msj)
        # Mostrar el contenido de las variables para debug
        log.debug(f"query: {query}")
        log.debug(f"context: {context}")
        log.debug(f"response: {response}")
    except Exception as e:
        msj = f"[ERROR]{e}"
        log.error(msj)
        # Mostrar el contenido de las variables para debug
        log.debug(f"query: {query}")
        log.debug(f"context: {context}")
        log.debug(f"response: {response}")


def test_get_response():
    """
    Description:
    ------------
        Esta función realiza pruebas unitarias de la función get_response del módulo cohere_service.
        Genera un log con el resultado de las pruebas.
        Usa las variables de configuración del archivo config/test_unit.yaml
    """
    log.name = "test_get_response"
    request = config.get(["test_get_response"])
    # print('-------------------')
    # print(request)
    # print('-------------------')
    # class Request:
    #     def __init__(self, user_name, question):
    #         self.user_name = user_name
    #         self.question = question
    # request = Request(request['user_name'], request['question'])
    # response = get_response(request)
    from types import SimpleNamespace

    user_request = SimpleNamespace(**request)
    response = get_response(user_request)

    # print('RESPONSE:    ', response)

    try:
        assert response is not None, "La respuesta es None"
        assert response == config.get(
            ["test_get_response", "response"]
        ), "La respuesta no coincide"
        log.info("[PASS]: Test test_get_response passed successfully")
    except AssertionError as e:
        msj = f"[ERROR]: {e}"
        log.error(msj)
        # Mostrar el contenido de las variables para debug
        log.debug(f'request: {request["question"]}')
        log.debug(f"response: {response}")
    except Exception as e:

        msj = f"[ERROR]{e}"
        log.error(msj)
        # Mostrar el contenido de las variables para debug
        log.debug(f'request: {request["question"]}')
        log.debug(f"response: {response}")


if __name__ == "__main__":
    test_get_context()
    test_detect_language()
    test_generate_response()
    test_get_response()


# Para ejecutar el test se debe correr el siguiente comando:
# python -m app.tests.unit.test_unit_api
