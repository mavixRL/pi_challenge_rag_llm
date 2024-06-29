import openai
from app.core.config import settings
from app.models.user_request import UserRequest
from app.services.context_service import get_relevant_context, construct_prompt, format_response

openai.api_key = settings.openai_api_key

def get_response_op(request: UserRequest) -> str:
    context = get_relevant_context(request.question)
    prompt = construct_prompt(request.question, context)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0
    )
    return format_response(response.choices[0].text)




#################################################################################