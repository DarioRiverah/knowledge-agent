from pathlib import Path

from config import settings
from src.rag.vector_store import get_vector_store


class DeleteService:
    """
    Servicio encargado de eliminar documentos
    del sistema RAG.
    """

    def __init__(self) -> None:

        self._vector_store = get_vector_store()

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

        # delete_document() ya normaliza internamente el nombre,
        # así que le pasamos el nombre original tal cual (evitamos
        # normalizar dos veces).
        self._vector_store.delete_document(
            document_name
        )


        file_path = (
            self._documents_path /
            document_name
        )


        if file_path.exists():

            file_path.unlink()