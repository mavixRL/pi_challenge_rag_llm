"""
    database.py:
        Este módulo contiene funciones para interactuar con la base de datos ChromaDB.

"""

import hashlib
import uuid
from typing import Any, Literal, Optional, Union

# from app.utils.utils import doc_to_paragraphs, num_tokens_from_string, split_text
import chromadb
import cohere
from chromadb.api.models.Collection import Collection

# from dotenv import load_dotenv
from app.core.config import settings

EmbeddingType = Union[Literal["float", "int8", "uint8", "binary", "ubinary"], Any]
EmbedInputType = Union[
    Literal["search_document", "search_query", "classification", "clustering"], Any
]

co = cohere.Client(settings.cohere_api_key)


def init_chromadb(name: str = "collection_name", path: str = "./app/db/ChromaDB/"):
    """
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
    >>> client = chromadb.PersistentClient(path="./app/db/ChromaDB/")
    >>> collection = init_chromadb()
    """
    client = chromadb.PersistentClient(path=path)
    collection = client.get_or_create_collection(name=name)
    return collection


def hash_document_content(content: str) -> str:
    """
    Description:
    ------------
    Esta función genera un hash SHA-256 del contenido del documento.

    Parameters:
    -----------
        - content: str
            El contenido del documento.

    Returns:
    --------
        - hash: str
            Retorna el hash del contenido del documento.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def document_exists(collection: Collection, doc_id: str) -> bool:
    """
    Description:
    ------------
    Esta función verifica si un documento con un identificador dado ya existe en la colección.

    Parameters:
    -----------
        - collection: Collection
            La colección en la que se busca el documento.
        - doc_id: str
            El identificador del documento a verificar.

    Returns:
    --------
        - exists: bool
            Retorna True si el documento existe, False en caso contrario.
    """
    try:
        result = collection.get(ids=[doc_id])
        return len(result["documents"]) > 0
    except Exception as e:
        print(f"Error checking if document exists: {e}")
        return False


def add_documents_to_collection(
    collection: Collection,
    docs: list,
    model: str = "embed-multilingual-v3.0",
    input_type: Optional[EmbedInputType] = "search_query",
    embedding_types: Optional[EmbeddingType] = None,
    metadata_options: dict = dict(),
) -> Collection:
    """
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
    >>> client = chromadb.PersistentClient(path="./app/db/ChromaDB/")
    >>> collection = client.get_or_create_collection(name="respuestas_api")
    >>> docs = split_text(['text1','text2'])
    >>> collection = add_documents_to_collection(collection,docs)


    """
    for doc in docs:
        # doc = doc.page_content
        if isinstance(doc, str):
            doc_content = doc
        else:
            doc_content = doc.page_content
        doc_id = hash_document_content(doc_content)
        if document_exists(collection, doc_id):
            print(f"Document {doc_id} already exists. Skipping. ")
            continue

        uuid_name = uuid.uuid1()
        embedding = co.embed(
            texts=[doc_content],
            model=model,
            input_type=input_type,  # search_query" or "search_document"
            embedding_types=embedding_types,
        ).embeddings[0]

        print("document for", uuid_name)

        collection.add(
            ids=[doc_id],
            embeddings=embedding,
            metadatas=metadata_options,
            documents=doc_content,
        )
    return collection
