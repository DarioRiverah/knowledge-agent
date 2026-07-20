from langchain_core.documents import Document

from src.llm.llm import get_llm
from src.models.chat import ChatResponse
from src.prompts.system_prompt import SYSTEM_PROMPT
from src.rag.retriever import Retriever


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
    ) -> ChatResponse:
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

        return ChatResponse(
            answer=response.content,
            sources=self._extract_sources(
                documents
            ),
        )

    def _build_context(
        self,
        documents: list[Document],
    ) -> str:
        """
        Construye el contexto enviado al LLM.
        """

        return "\n\n".join(
            document.page_content
            for document in documents
        )

    def _extract_sources(
        self,
        documents: list[Document],
    ) -> list[dict]:
        """
        Extrae información de las fuentes utilizadas.
        """

        sources = []

        for document in documents:

            metadata = document.metadata

            sources.append(
                {
                    "document": metadata.get(
                        "document_name"
                    ),
                    "page": metadata.get(
                        "page"
                    ),
                }
            )

        return sources