from src.graph.graph import AgentGraph
from src.memory.conversation import ConversationMemory
from src.models.chat import ChatResponse


class AgentService:
    """
    Servicio principal del agente.

    Coordina:
    - Memoria
    - LangGraph
    - Estado
    - Respuesta final
    """

    def __init__(self) -> None:

        self.agent = AgentGraph()

        self.memory = ConversationMemory()

        self.messages = []

    def chat(
        self,
        question: str,
    ) -> ChatResponse:
        """
        Ejecuta una conversación con el agente.
        """

        self.memory.add_user_message(
            self.messages,
            question,
        )

        state = {
            "question": question,
            "route": "",
            "messages": self.messages,
            "memory": self.memory,
            "documents": [],
            "context": "",
            "context_valid": False,
            "answer": "",
            "sources": [],
        }

        result = self.agent.invoke(
            state
        )

        self.messages = result["messages"]

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
        )