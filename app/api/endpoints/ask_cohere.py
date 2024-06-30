"""
    Modulo ask_cohere.py:
        Este módulo contiene la definición de la ruta para el endpoint /ask_cohere
        que se encarga de interactuar con la API de Cohere para obtener respuestas
        a las preguntas de los usuarios.

"""
from fastapi import APIRouter, HTTPException
from app.models.user_request import UserRequest
# from app.services.openai_service import get_response
from app.services.cohere_service import get_response

router = APIRouter()

@router.post("/ask_cohere")
async def get_response_cohere(request: UserRequest):
    '''
    Description:
    ------------
        Esta función recibe una solicitud del usuario y devuelve una respuesta
        utilizando la API de Cohere.
    
    Parameters:
    -----------
        - request: UserRequest
            Es la solicitud del usuario que contiene la pregunta y el contexto.
    
    Returns:
    --------
        - dict
            Retorna un diccionario con la respuesta y el estatus 200.
    '''
    try:

        response = get_response(request)
        # enviar respuesta y estatus 200
        return {"answer": response, "status": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))