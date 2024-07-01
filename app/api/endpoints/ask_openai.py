"""
    In Progress
        Módulo ask_openai.py
            Este módulo contiene la definición de la ruta para el endpoint /ask_openai.

"""

from fastapi import APIRouter, HTTPException

from app.models.user_request import UserRequest

# from app.services.cohere_service import get_response_cohere
from app.services.openai_service import get_response_op

router = APIRouter()


@router.post("/ask_openai")
async def ask_question(request: UserRequest):
    """
    In Progress
        No usar, está en desarrollo.
    """
    try:
        response = get_response_op(request)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
