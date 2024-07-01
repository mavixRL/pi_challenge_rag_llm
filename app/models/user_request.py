"""
Este archivo define el modelo de datos para las solicitudes de usuario en la API.
Utiliza Pydantic para la validación de datos y garantiza que las solicitudes de usuario contengan
los campos necesarios y estén en el formato correcto.
"""

from pydantic import BaseModel


class UserRequest(BaseModel):
    """
    Modelo de datos para las solicitudes de usuario en la API
    """

    user_name: str
    question: str
