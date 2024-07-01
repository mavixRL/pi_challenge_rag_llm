"""
    Este módulo contiene la ruta raíz de la API, la cual se utiliza
    para verificar que la API está funcionando correctamente.

"""

from fastapi import APIRouter, HTTPException

# from app.models.user_request import UserRequest

router = APIRouter()


# # Ruta raíz para verificar que la API está funcionando
@router.get("/")
def root():
    """
    Description:
    ------------
        Esta función se encarga de verificar que la API está funcionando correctamente.

    Returns:
    --------
        - dict
            Retorna un diccionario con un mensaje de bienvenida.
    """
    try:
        return {
            "mensaje": "Bienvenido a la  API. Desarrollado por Mavix Arias Aguila",
            "message": "Welcome to the API. Developed by Mavix Arias Aguila",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
