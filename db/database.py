from app.utils.utils import doc_to_paragraphs
from app.utils.utils import num_tokens_from_string
from app.utils.utils import split_text
import uuid
from chromadb.api.models.Collection import Collection
# from chromadb.api.types import EmbedInputType,EmbeddingType
from typing import Sequence, Optional, Union,Literal,Any

EmbeddingType = Union[Literal["float", "int8", "uint8", "binary", "ubinary"], Any]
EmbedInputType = Union[ Literal["search_document", "search_query", "classification", "clustering"], Any]


import chromadb
# from app.services.cohere_service import co 
from typing import Sequence, Optional, Union,Literal,Any

import os
from dotenv import load_dotenv
from app.core.config import settings
import cohere
load_dotenv()
co = cohere.Client(settings.cohere_api_key)

def init_chromadb():
    '''
    Description:
    ------------
    Esta función inicializa una colección en ChromaDB.

    Returns:
    --------
        - collection: Collection
            Retorna la colección inicializada.

    Example:
    --------
    >>> import chromadb
    >>> client = chromadb.PersistentClient(path="./../ChromaDB/")
    >>> collection = init_chromadb()
    '''
    client = chromadb.PersistentClient(path="./../ChromaDB/")
    collection = client.get_or_create_collection(name="collection_name")
    return collection



def add_documents_to_collection(
        collection:Collection,
        docs:list,
        model:str ='embed-multilingual-v3.0',
        input_type: Optional[EmbedInputType]='search_query',
        embedding_types:Optional[EmbeddingType]= None,
        metadata_options:dict = dict(),

    )->Collection:
    '''
    Description:
    ------------
    Esta función recibe una colección y una lista de documentos y los agrega a la colección.

    Parameters:
    -----------
        - collection: Collection
            Es la colección a la que se desea agregar los documentos.
        - docs: list
            Lista de documentos que se desean agregar a la colección.
        - model: str
            Es el modelo que se desea utilizar para realizar el embedding.
            Por defecto es 'embed-multilingual-v3.0'.
            Los modelos disponibles son:(verificar en la documentación de Cohere)
                - embed-english-v3.0 1024
                - embed-multilingual-v3.0 1024
                - embed-english-light-v3.0 384
                - embed-multilingual-light-v3.0 384
                - embed-english-v2.0 4096
                - embed-english-light-v2.0 1024
                - embed-multilingual-v2.0 768
        - input_type: Optional[EmbedInputType]
            Es el tipo de input que se desea utilizar.
            Por defecto es 'search_query'.
            Los tipos de input disponibles son:(verificar en la documentación de Cohere)
                - search_document
                - search_query
                - classification
                - clustering
        - embedding_types: Optional[EmbedRequestTruncate]
            Es el tipo de embedding que se desea utilizar.
            Por defecto es "float".
            Los tipos de embedding disponibles son:(verificar en la documentación de Cohere)
                - "float"
                - "int8"
                - "uint8"
                - "binary"
                - "ubinary"
        - metadata_options: dict
            Es un diccionario con los metadatos que se desean agregar a los documentos.
            Por defecto es un diccionario vacío.
    
    Returns:
    --------
        - collection: Collection
            Retorna la colección con los documentos agregados.

    Example:
    --------
    >>> import chromadb
    >>> client = chromadb.PersistentClient(path="./../ChromaDB/")
    >>> collection = client.get_or_create_collection(name="respuestas_api")
    >>> docs = split_text(['text1','text2'])
    >>> collection = add_documents_to_collection(collection,docs)


    '''
    for doc in docs:
        doc = doc.page_content
        uuid_name = uuid.uuid1()
        embedding = co.embed(texts=[doc], model=model, input_type=input_type,
            embedding_types=embedding_types).embeddings[0] # search_query" or "search_document"
        print("document for", uuid_name)
        # doc.page_content
        
        collection.add(ids=[str(uuid_name)],
                    embeddings=embedding,
                    metadatas=metadata_options,
                    documents=doc)
    return collection
