from pydantic import BaseModel

class UserRequest(BaseModel):
    user_name: str
    question: str