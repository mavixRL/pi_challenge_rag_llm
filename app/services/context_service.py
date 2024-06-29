from langdetect import detect

def get_relevant_context(question: str) -> str:
    # Implementa la lógica para obtener el contexto relevante
    return "Relevant context"

def construct_prompt(question: str, context: str) -> str:
    language = detect(question)
    instructions = {
        "es": "Responde en una sola oración, en el mismo idioma que la pregunta, incluyendo emojis que resuman el contenido de la respuesta, y siempre en tercera persona.",
        "en": "Answer in one sentence, in the same language as the question, including emojis that summarize the content of the answer, and always in third person.",
        "pt": "Responda em uma frase, no mesmo idioma da pergunta, incluindo emojis que resumam o conteúdo da resposta, e sempre na terceira pessoa."
    }
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer: {instructions[language]}"
    return prompt

def format_response(response_text: str) -> str:
    response_text = response_text.strip()
    response_text += " 😊"
    return response_text


# #################################################################################



# ####################################################################################################
# import cohere
# import chromadb
# from app.core.config import settings
# from app.models.user_request import UserRequest
# from chromadb.api.models.Collection import Collection


# client = chromadb.PersistentClient(path="./../ChromaDB/")
# collection = client.get_or_create_collection(name="document_chunks")

# co = cohere.Client(settings.cohere_api_key)

# def get_context(collection:Collection,query:str,n_results:int=1):
#     '''
#     Description:
#     ------------
#     Esta función recibe un query y devuelve el contexto de la respuesta.
    
#     Parameters:
#     -----------
#         - collection: Collection
#             Es la colección con la que se desea realizar la consulta.
#         - query: str
#             Es la pregunta que se desea realizar.
#         - n_results: int
#             Es el número de resultados que se desean obtener.
#             por defecto es 1.
    
#     Returns:
#     --------
#         - results: dict
#             Retorna un diccionario con los resultados de la consulta.
#         - contexto: str
#             Retorna el contexto de la respuesta.
    
#     Example:
#     --------
#     >>>query = "Quien es Zara?"
#     >>> results,contexto = get_context(query)
#     '''

#     # query_embedding = co.embed(texts=[query]).embeddings[0]
#     query_embedding = co.embed(texts=[query],model='embed-multilingual-v3.0',input_type ='search_query').embeddings[0] # search_query" or "search_document"
#     results = collection.query(query_embeddings=query_embedding, n_results=n_results,include=['documents']) #include=['embeddings','documents']
#     contexto = ' '.join([result for result in results['documents'][0]])
#     # contexto  = results['documents'][0][0]
#     contexto
#     return results,contexto

