import openai
from app.core.config import settings
from app.models.user_request import UserRequest
from app.utils.utils import format_response
# from app.services.context_service import get_relevant_context, construct_prompt, format_response

# openai.api_key = settings.openai_api_key

# def get_response(request: UserRequest) -> str:
#     context = get_relevant_context(request.question)
#     prompt = construct_prompt(request.question, context)
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=prompt,
#         max_tokens=50,
#         temperature=0
#     )
#     return format_response(response.choices[0].text)


#################################################################################
import time
from ratelimit import limits, sleep_and_retry
import os
from dotenv import load_dotenv
from app.core.config import settings
import cohere
from chromadb.api.models.Collection import Collection
import langid
from db.database import init_chromadb
# from app.main import collection
load_dotenv()

# # COHERE_api_key: str = os.getenv("COHERE_API_KEY")
# COHERE_api_key = settings.cohere_api_key

# Limites del API de Cohere
EMBED_LIMIT = settings.EMBED_LIMIT  # llamadas por minuto
RERANK_CHAT_LIMIT = settings.RERANK_CHAT_LIMIT  # llamadas por minuto
OTHER_LIMIT = settings.OTHER_LIMIT  # llamadas por minuto

co = cohere.Client(settings.cohere_api_key)

collection = init_chromadb()

# def get_context(collection:Collection,query:str,n_results:int=1):
def get_context(query:str,n_results:int=1):
    '''
    Description:
    ------------
    Esta función recibe un query y devuelve el contexto de la respuesta.
    
    Parameters:
    -----------
        - collection: Collection
            Es la colección con la que se desea realizar la consulta.
        - query: str
            Es la pregunta que se desea realizar.
        - n_results: int
            Es el número de resultados que se desean obtener.
            por defecto es 1.
    
    Returns:
    --------
        - results: dict
            Retorna un diccionario con los resultados de la consulta.
        - contexto: str
            Retorna el contexto de la respuesta.
    
    Example:
    --------
    >>>query = "Quien es Zara?"
    >>> results,contexto = get_context(query)
    '''

    # query_embedding = co.embed(texts=[query]).embeddings[0]
    query_embedding = co.embed(texts=[query],model='embed-multilingual-v3.0',input_type ='search_query').embeddings[0] # search_query" or "search_document"
    results = collection.query(query_embeddings=query_embedding, n_results=n_results,include=['documents']) #include=['embeddings','documents']
    contexto = ' '.join([result for result in results['documents'][0]])
    # contexto  = results['documents'][0][0]
    contexto
    return results,contexto

@sleep_and_retry
@limits(calls=EMBED_LIMIT, period=60)
def detect_language(query:str):
    '''
    Description:
    ------------
        Esta función recibe un query y devuelve el idioma del query.
        Si el idioma no es español, inglés o portugués, se solicita al LLM que interprete el idioma.

    Parameters:
    -----------
        - query: str
            es el texto que se desea detectar el idioma.
    
    Returns:
    --------
        - language: str
        retorno el idioma del texto en formato de dos letras.

    Example:
    --------
    >>> query = "Quien es Zara?"
    >>> language = detect_language(query)
    es
    >>>
    '''
    
    language = langid.classify(query)[0]
    if not language in ['es','en','pt']:
        response = co.chat(
        chat_history=[
            {"role": "SYSTEM", "message": f"""Eres  un detector muy preciso de idiomas,dime el idioma en una sola palabra (es, en, pt) de la siguiente pregunta : """},
        ],
        message=f"""{query}""",
        # connectors=[{"id": "translation"}],
        seed=44,
        temperature=0,
        )
        language = response.text
    return language

@sleep_and_retry
@limits(calls=EMBED_LIMIT, period=60)
def generate_response(query:str, contexto:str):
    '''
    Description:
    ------------
        Esta función recibe un query y un contexto y devuelve una respuesta en el mismo idioma que el query.
    
    Parameters:
    -----------
        - query: str
            Es la pregunta que se desea realizar.
        - contexto: str
            Es el contexto de la respuesta.

    Returns:
    --------
        - respuesta: str
            Retorna la respuesta en el mismo idioma que el query.

    Example:
    --------
    >>> query = "Quien es Zara?"
    >>> contexto = "Zara es una empresa de moda"
    >>> respuesta = generate_response(query, contexto)
    >>>
    '''
    language = detect_language(query)

    dict_important1 =  {
            "es":"Debes ser lo más conciso y preciso posible en la entrega de información (20 palabras o menos) y traducir tu respuesta si es necesario a partir del siguiente contexto:",
            "en":"You must be as concise and precise as possible in delivering information (20 words or less) and translate your response if necessary from the following context:",
            "pt":"Você deve ser o mais conciso e preciso possível na entrega de informações (20 palavras ou menos) e traduzir sua resposta, se necessário, a partir do seguinte contexto:",
            }

    dict_important2 = {
            "es": "Responde en una sola oración, en el mismo idioma que la pregunta, incluyendo emojis que resuman el contenido de la respuesta, y siempre en tercera persona.",
            "en": "Answer in one sentence, in the same language as the question, including emojis that summarize the content of the answer, and always in third person.",
            "pt": "Responda em uma frase, no mesmo idioma da pergunta, incluindo emojis que resumam o conteúdo da resposta, e sempre na terceira pessoa.",
        }
    dict_important3  = {
            "es": "Responde en español, si el texto esta en español traduce la respuesta al español.",
            "en": "Answer in English, if the text is in español, translate the answer to English.",
            "pt": "Responda em português, se o texto estiver em español, traduza a resposta para o português.",
        }

    response = co.chat(
        chat_history=[
            {"role": "SYSTEM", "message": f"""{dict_important1[language]}
            {contexto}
            NOTA IMPORTANTE:
            {dict_important2[language]}

            """},
            
            # {
            #     "role": "CHATBOT",
            #     "message": f"ya identifique el idioma del siguiente mensaje :{query} procedere a responder en el mismo idioma.",
            # },
        ],
        message=f"""{query} {dict_important3[language]}""",
        #"realizar búsqueda web antes de responder a la pregunta. También puedes usar tu propio conector personalizado."
        # · contenedores de traducion y busqueda en contexto
        # connectors=[{"id": "translation"}],
        seed=44,
        temperature=0,
        # conversation_id='user_defined_id_1',
        # model = 'command-r-plus',
        # model = 'command-r',
    )
    respuesta =response.text

    return respuesta

def get_response(request: UserRequest) -> str:
    contexto =get_context(query=request.question,n_results=1)
    respuesta = generate_response(request.question, contexto)
    
    return format_response(respuesta)



####################################################################################################


# @sleep_and_retry
# @limits(calls=EMBED_LIMIT, period=60)
# def generate_response(query:str, contexto:str):
#     '''
#     Description:
#     ------------
#         Esta función recibe un query y un contexto y devuelve una respuesta en el mismo idioma que el query.
    
#     Parameters:
#     -----------
#         - query: str
#             Es la pregunta que se desea realizar.
#         - contexto: str
#             Es el contexto de la respuesta.

#     Returns:
#     --------
#         - respuesta: str
#             Retorna la respuesta en el mismo idioma que el query.

#     Example:
#     --------
#     >>> query = "Quien es Zara?"
#     >>> contexto = "Zara es una empresa de moda"
#     >>> respuesta = generate_response(query, contexto)
#     >>>
#     '''
#     language = detect_language(query)

#     dict_important1 =  {
#             "es":"Debes ser lo más conciso y preciso posible en la entrega de información (20 palabras o menos) y traducir tu respuesta si es necesario a partir del siguiente contexto:",
#             "en":"You must be as concise and precise as possible in delivering information (20 words or less) and translate your response if necessary from the following context:",
#             "pt":"Você deve ser o mais conciso e preciso possível na entrega de informações (20 palavras ou menos) e traduzir sua resposta, se necessário, a partir do seguinte contexto:",
#             }

#     dict_important2 = {
#             "es": "Responde en una sola oración, en el mismo idioma que la pregunta, incluyendo emojis que resuman el contenido de la respuesta, y siempre en tercera persona.",
#             "en": "Answer in one sentence, in the same language as the question, including emojis that summarize the content of the answer, and always in third person.",
#             "pt": "Responda em uma frase, no mesmo idioma da pergunta, incluindo emojis que resumam o conteúdo da resposta, e sempre na terceira pessoa.",
#         }
#     dict_important3  = {
#             "es": "Responde en español, si el texto esta en español traduce la respuesta al español.",
#             "en": "Answer in English, if the text is in español, translate the answer to English.",
#             "pt": "Responda em português, se o texto estiver em español, traduza a resposta para o português.",
#         }

#     response = co.chat(
#         chat_history=[
#             {"role": "SYSTEM", "message": f"""{dict_important1[language]}
#             {contexto}
#             NOTA IMPORTANTE:
#             {dict_important2[language]}

#             """},
            
#             # {
#             #     "role": "CHATBOT",
#             #     "message": f"ya identifique el idioma del siguiente mensaje :{query} procedere a responder en el mismo idioma.",
#             # },
#         ],
#         message=f"""{query} {dict_important3[language]}""",
#         #"realizar búsqueda web antes de responder a la pregunta. También puedes usar tu propio conector personalizado."
#         # · contenedores de traducion y busqueda en contexto
#         # connectors=[{"id": "translation"}],
#         seed=44,
#         temperature=0,
#         # conversation_id='user_defined_id_1',
#         # model = 'command-r-plus',
#         # model = 'command-r',
#     )
#     respuesta =response.text

#     return respuesta
