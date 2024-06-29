from fastapi import APIRouter, HTTPException
from app.models.user_request import UserRequest
# from app.services.openai_service import get_response
from app.services.cohere_service import get_response


router = APIRouter()

# @router.post("/ask_openai")
# async def ask_question(request: UserRequest):
#     try:
#         response = get_response(request)
#         return {"answer": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask_cohere")
async def get_response_cohere(request: UserRequest):
    try:

        response = get_response(request)
        # enviar respuesta y estatus 200
        return {"answer": response, "status": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))