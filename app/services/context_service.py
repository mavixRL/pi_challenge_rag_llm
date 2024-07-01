"""
    In Progress
    Posiblemente se tenga que eliminar ya que se esta trabajando en cohere_service.py
"""

from langdetect import detect


def get_relevant_context(question: str) -> str:
    """# Implementa la lógica para obtener el contexto relevante"""
    return "Relevant context"


def construct_prompt(question: str, context: str) -> str:
    """
    In Progress
    """
    language = detect(question)
    instructions = {
        "es": "Responde en una sola oración, en el mismo idioma que la pregunta, incluyendo emojis que resuman el contenido de la respuesta, y siempre en tercera persona.",
        "en": "Answer in one sentence, in the same language as the question, including emojis that summarize the content of the answer, and always in third person.",
        "pt": "Responda em uma frase, no mesmo idioma da pergunta, incluindo emojis que resumam o conteúdo da resposta, e sempre na terceira pessoa.",
    }
    prompt = (
        f"Context: {context}\nQuestion: {question}\nAnswer: {instructions[language]}"
    )
    return prompt


def format_response(response_text: str) -> str:
    """
    In Progress
    """
    response_text = response_text.strip()
    # response_text += " 😊"
    return response_text
