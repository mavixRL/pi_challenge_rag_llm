from fastapi import FastAPI
from app.api.endpoints import ask_cohere
from app.api.endpoints import test_api

app = FastAPI()

app.include_router(ask_cohere.router, prefix="/api")
app.include_router(test_api.router, prefix="/api")

