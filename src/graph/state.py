from typing import TypedDict


class AgentState(TypedDict):
    """
    Estado principal del agente LangGraph.

    Contiene toda la información
    que fluye entre los nodos.
    """

    question: str

    route: str

    messages: list

    documents: list

    context: str

    answer: str

    sources: list