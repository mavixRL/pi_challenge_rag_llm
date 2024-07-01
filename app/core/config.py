'''
    Este archivo contiene la configuración de la aplicación.
'''
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    """
    Clase para almacenar las configuraciones de la aplicación.
    """
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    cohere_api_key: str = os.getenv("COHERE_API_KEY")

    # Limites del API de Cohere
    EMBED_LIMIT = 5  # llamadas por minuto
    RERANK_CHAT_LIMIT = 10  # llamadas por minuto
    OTHER_LIMIT = 100  # llamadas por minuto

settings = Settings()
