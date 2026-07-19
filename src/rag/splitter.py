from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


class TextSplitter:
    """
    Responsable de dividir documentos en chunks para el proceso RAG.
    """

    def __init__(self) -> None:
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def split(self, documents: list[Document]) -> list[Document]:
        """
        Divide una lista de documentos en chunks.
        """
        return self._splitter.split_documents(documents)