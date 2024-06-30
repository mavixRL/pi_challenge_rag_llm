from fastapi import FastAPI
from app.api.endpoints import ask_cohere
from app.api.endpoints import root
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="""Challenge Python LLM RAG | Pi Consulting""",
    description="""Esta API proporciona un servicio para generar respuestas aumentadas basadas 
en un modelo de lenguaje de gran escala (LLM). Utiliza FastAPI para manejar las solicitudes HTTP 
y interactuar con el LLM a través de Cohere para generar respuestas coherentes y contextualizadas 
respecto al documento entregado."""
)

app.include_router(ask_cohere.router, prefix="/api")
app.include_router(root.router, prefix="/api")


# # Configuración de CORS
# origins = [
#     "http://localhost",  # Si estás accediendo desde localhost
#     "http://localhost:8003",  # Puerto específico
#     "http://127.0.0.1:8003",  # También puedes añadir otras IPs y puertos según necesites
#     "http://tudominio.com",  # Añade aquí el dominio desde el que accedes
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )