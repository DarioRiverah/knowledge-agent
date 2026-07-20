from dataclasses import dataclass


@dataclass
class ChatResponse:
    """
    Modelo de respuesta generado por el agente.
    """

    answer: str
    sources: list[dict]