from pathlib import Path

from config import settings
from src.rag.vector_store import VectorStore
from src.utils.id_generator import DocumentIdGenerator


class DeleteService:
    """
    Servicio encargado de eliminar documentos
    del sistema RAG.
    """

    def __init__(self) -> None:

        self._vector_store = VectorStore()

        self._documents_path = Path(
            settings.documents_path
        )


    def delete(
        self,
        document_name: str,
    ) -> None:
        """
        Elimina un documento del sistema.

        Elimina:
        - Archivo físico
        - Embeddings asociados
        """

        normalized_name = (
            DocumentIdGenerator.normalize(
                document_name
            )
        )


        self._vector_store.delete_document(
            normalized_name
        )


        file_path = (
            self._documents_path /
            document_name
        )


        if file_path.exists():

            file_path.unlink()