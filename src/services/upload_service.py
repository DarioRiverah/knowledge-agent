from pathlib import Path
import shutil

from config import settings

from src.exceptions.document_exceptions import (
    DocumentAlreadyExistsError,
)

from src.rag.loader import DocumentLoader
from src.rag.splitter import TextSplitter
from src.rag.vector_store import get_vector_store
from src.utils.id_generator import DocumentIdGenerator


class UploadService:
    """
    Servicio encargado de subir documentos
    y agregarlos al sistema RAG.
    """

    def __init__(self) -> None:

        self._loader = DocumentLoader()
        self._splitter = TextSplitter()
        self._vector_store = get_vector_store()

        self._documents_path = Path(
            settings.documents_path
        )

        self._documents_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def upload(
        self,
        file_path: str,
    ) -> int:
        """
        Procesa un documento nuevo.

        Retorna la cantidad de chunks creados.
        """

        source = Path(file_path)

        existing_documents = (
            self._vector_store.list_documents()
        )

        if source.name in existing_documents:

            raise DocumentAlreadyExistsError(
                f"El documento '{source.name}' ya existe."
            )

        destination = (
            self._documents_path /
            source.name
        )

        shutil.copy(
            source,
            destination,
        )

        documents = self._loader.load(
            str(destination)
        )

        chunks = self._splitter.split(
            documents
        )

        ids = []

        for index, chunk in enumerate(chunks):

            DocumentIdGenerator.enrich_metadata(
                chunk,
                index,
            )

            ids.append(
                DocumentIdGenerator.generate(
                    chunk,
                    index,
                )
            )

        self._vector_store.add_documents(
            chunks,
            ids,
        )

        return len(chunks)