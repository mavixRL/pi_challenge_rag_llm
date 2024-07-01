"""
    In Progress
        Este modulo se encarga de interactuar con la API de OpenAI
        para obtener respuestas a las preguntas de los usuarios.

"""

import openai
from app.core.config import settings
from app.models.user_request import UserRequest
from app.services.context_service import (
    construct_prompt,
    format_response,
    get_relevant_context,
)

openai.api_key = settings.openai_api_key


def get_response_op(request: UserRequest) -> str:
    """
    In Progress
        Esta función recibe una solicitud del usuario y devuelve una respuesta
        utilizando la API de OpenAI.
    """
    context = get_relevant_context(request.question)
    prompt = construct_prompt(request.question, context)
    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt, max_tokens=500, temperature=0
    )
    return format_response(response.choices[0].text)



