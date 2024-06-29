from fastapi import APIRouter, HTTPException
from app.models.user_request import UserRequest
# from app.services.openai_service import get_response

router = APIRouter()

@router.post("/")
async def test_api(request: UserRequest):
    try:
        mensaje= 'Hola Pi Consulting'
        return {"answer": mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
