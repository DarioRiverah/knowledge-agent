from langchain_groq import ChatGroq

from config import settings


def get_llm() -> ChatGroq:
    """
    Crea y devuelve una instancia del modelo de lenguaje.
    """

    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.model_name,
        temperature=settings.temperature,
    )