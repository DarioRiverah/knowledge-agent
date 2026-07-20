from langchain_core.documents import Document

from src.llm.llm import get_llm
from src.rag.retriever import Retriever
from src.prompts.system_prompt import SYSTEM_PROMPT


class ChatService:
    """
    Servicio encargado de responder preguntas
    utilizando RAG + LLM.
    """

    def __init__(self) -> None:
        self._llm = get_llm()
        self._retriever = Retriever()

    def ask(
        self,
        question: str,
    ) -> str:
        """
        Ejecuta una consulta RAG completa.
        """

        documents = self._retriever.search(
            question
        )

        context = self._build_context(
            documents
        )

        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question,
        )

        response = self._llm.invoke(
            prompt
        )

        return response.content

    def _build_context(
        self,
        documents: list[Document],
    ) -> str:
        """
        Convierte documentos recuperados
        en texto para el LLM.
        """

        context = []

        for document in documents:
            context.append(
                document.page_content
            )

        return "\n\n".join(context)