from langchain_core.documents import Document

from src.rag.vector_store import VectorStore


class Retriever:
    """
    Capa encargada de recuperar información relevante
    desde la base vectorial.
    """

    def __init__(self) -> None:
        self._vector_store = VectorStore()

        self._retriever = (
            self._vector_store.get_retriever()
        )

    def search(
        self,
        query: str,
    ) -> list[Document]:
        """
        Busca documentos relevantes para una pregunta.
        """

        return self._retriever.invoke(query)