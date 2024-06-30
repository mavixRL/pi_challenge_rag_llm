import tiktoken
from typing import Sequence, Optional, Union,Literal,Any, List
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter



def print_collections(collections:list) -> None:
    """
    Descripción:
    ------------
    Prints the collections in the database de forma legible para las ultimas versiones de Chromadb.
    En las ultimas versiones no se ve el objeto collection, por lo que se debe de cambiar el print
    
    Parameters:
    -----------
        - collections: list
            Es una lista de objetos de tipo collection
    
    Returns:
    --------
        - None
            imprime en pantalla el nombre de las colecciones
            
    
    Example:
    --------
    >>> import chromadb
    >>> client = chromadb.PersistentClient(path="./../ChromaDB/")
    >>> client.create_collection(name="respuestas_api")
    >>> print_collections(collections)
    """
    for collection in collections:
        print(f"Collection(name={collection.name})")

def print_verbose(msg: str,verbose:bool) -> None:
    '''
    Description:
    ------------
    Esta función imprime un mensaje en pantalla si verbose es True
    
    Parameters:
    -----------
        - msg: str
            Es el mensaje que se desea imprimir en pantalla
        - verbose: bool
            Es un booleano que indica si se imprime o no el mensaje en pantalla
            
    Returns:
    --------
        - None
            No retorna ningún valor solo imprime en pantalla el mensaje
            
    Example:
    --------
    >>> print_verbose("Hola Mundo", True)
    '''
    print(msg) if verbose else None



def num_tokens_from_string(string: str, encoding_name: str="cl100k_base") -> int:
    """
    Description:
    ------------
        Esta función recibe un string y devuelve el número de tokens que contiene.

    Parameters:
    -----------
        - string: str
            Es el string que se desea tokenizar.
        - encoding_name: str
            Es el nombre del encoding que se desea utilizar para tokenizar el string.
    
    Returns:
    --------
        - num_tokens:int
            Retorna el número de tokens que contiene el string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def doc_to_paragraphs(file:str='./docs/documento.docx'):
    '''
    Description:
    ------------
        Esta función recibe un archivo .docx y devuelve una lista con los párrafos del documento
        y una lista con el número de tokens de cada párrafo.

    Parameters:
    -----------
        - file: str
            Es la ruta del archivo .docx que se desea tokenizar.
    
    Returns:
    --------
        - ntoken_list: list
            Retorna una lista con el número de tokens de cada párrafo.
        - list_parrafo: list
            Retorna una lista con los párrafos del documento.
    
    Example:
    --------
    >>> ntoken_list, list_parrafo = doc_to_paragraphs(file)

    '''
    # Abre el archivo .docx
    doc = Document(file)

    list_parrafo = [parrafo.text for parrafo in doc.paragraphs if (parrafo.text != "")and(parrafo.text != " ")]
    ntoken_list = [num_tokens_from_string(parrafo) for parrafo in list_parrafo]

    return ntoken_list, list_parrafo

    
def split_text(
        input: Union[str,List[str]],
        unir_list:bool=False, 
        chunk_size: int=300,
        chunk_overlap: int=0,
        separators:list=["\n\n", "\n",],
        verbose=False
)->list:
    '''
    Description:
    ------------
        Esta función recibe un texto o lista  y lo divide en chunks de un tamaño especificado.
        Por defecto si es una lista no se unirá, si se desea unir se debe de especificar en el
        parámetro unir_list=True
        Nota: si se especifica unir_list=False  y se pasa separators ["\n\n", "\n"] los chunks
        se dividirán por los saltos de linea para cada elemento de la lista de strings.
        Si se especifica unir_list=False y separators = ["\n\n", "\n"] los chunks no tomaran en cuanta chunk_size y chunk_overlap

    Parameters:
    -----------
        - input: str or list
            Es el texto que se desea dividir en chunks.
        - chunk_size: int
            Es el tamaño de cada chunk.
        - chunk_overlap: int
            Es el solapamiento entre chunks.
        - separators: list
            Es una lista con los separadores que se desean utilizar para dividir el texto.
            ejemplo: ["\n\n", "\n", ",", ";", "."]
        - verbose: bool
            Es un booleano que indica si se imprime o no el mensaje en pantalla
        - unir_list: bool   
            Es un booleano que indica si se desea unir la lista de strings en un solo string.

    
    Returns:
    --------
        - chunks: list
            Retorna una lista con los chunks del texto.
    
    Example:
    --------
    >>> chunks = split_text(text)

    >>> docs = split_text(input=list_parrafo,chunk_size=500, chunk_overlap=20,
                            unir_list=False,separators=None,verbose=False)

    >>> docs = split_text(input=list_parrafo, chunk_size=500, chunk_overlap=20,
                            unir_list=False,separators=["\n\n", "\n"],verbose=False)
    
    '''
    if isinstance(input, str):
        input = [input]
    elif isinstance(input, list):
        if unir_list:
            input = [" ".join(input)]
    print_verbose(input,verbose)

    # Configuración del splitter
    text_splitter = RecursiveCharacterTextSplitter(
        separators=separators,          # Separadores a utilizar
        chunk_size=chunk_size,          # Tamaño de cada chunk
        chunk_overlap=chunk_overlap,    # Solapamiento entre chunks
    )

    # Crear documentos divididos
    docs = text_splitter.create_documents(input)

    # Mostrar resultado
    for doc in docs:
        print_verbose(msg=f'Chunk: {doc.page_content}', verbose=verbose)

    return docs

def format_response(response_text: str) -> str:
    '''
    Description:
    ------------
        Esta función recibe un texto y le agrega un emoji al final.

    Parameters:
    -----------
        - response_text: str
            Es el texto al que se le desea agregar un emoji.
    
    Returns:
    --------
        - response_text: str
            Retorna el texto 
    '''

    response_text = response_text.strip()
    # response_text += " 😊"
    return response_text