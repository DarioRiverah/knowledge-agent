from typing import TypedDict

from src.memory.conversation import ConversationMemory


class AgentState(TypedDict):
    """
    Estado principal del agente LangGraph.

    Contiene toda la información
    que fluye entre los nodos.
    """

    question: str

    route: str

    messages: list

    memory: ConversationMemory

    documents: list

    context: str

    context_valid: bool

    answer: str

    sources: list