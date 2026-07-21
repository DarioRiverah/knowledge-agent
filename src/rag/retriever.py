from langchain_core.documents import Document

from config import settings
from src.rag.vector_store import get_vector_store


class Retriever:
    """
    Capa encargada de recuperar información relevante
    desde la base vectorial.
    """

    def __init__(self) -> None:

        self._vector_store = get_vector_store()

    def search(
        self,
        query: str,
    ) -> list[Document]:
        """
        Busca documentos relevantes
        utilizando el score de similitud.
        """

        results = (
            self._vector_store
            .similarity_search_with_score(
                query=query,
                k=settings.top_k,
            )
        )

        documents = []

        for document, score in results:

            print(
                f"Documento: "
                f"{document.metadata.get('document_name')} "
                f"| Score: {score}"
            )

            if score <= settings.score_threshold:

                documents.append(
                    document
                )

        return documents