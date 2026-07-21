import shutil
from functools import lru_cache
from pathlib import Path

from langchain_core.documents import Document
from langchain_chroma import Chroma

from config import settings
from src.rag.embeddings import EmbeddingModel
from src.utils.id_generator import DocumentIdGenerator


class VectorStore:
    """
    Capa de acceso a la base vectorial.

    Responsable de:
    - Crear o abrir ChromaDB.
    - Guardar documentos.
    - Eliminar documentos.
    """

    def __init__(self) -> None:
        self._embedding_model = EmbeddingModel()

        self._db_path = Path(settings.chroma_path)

        self._db_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._vector_store = self._create_vector_store()

    def _create_vector_store(self) -> Chroma:
        """
        Crea una instancia persistente de Chroma.
        """

        return Chroma(
            collection_name=settings.collection_name,
            embedding_function=self._embedding_model.model,
            persist_directory=str(self._db_path),
            collection_metadata={"hnsw:space": "cosine"},
        )

    def add_documents(
        self,
        documents: list[Document],
        ids: list[str],
    ) -> None:
        """
        Agrega documentos a la base vectorial.
        """

        self._vector_store.add_documents(
            documents=documents,
            ids=ids,
        )

    def delete_document(
        self,
        document_name: str,
    ) -> None:
        """
        Elimina todos los chunks pertenecientes
        a un documento.
        """

        normalized_name = DocumentIdGenerator.normalize(
            document_name
        )

        self._vector_store.delete(
            where={
                "normalized_name": normalized_name
            }
        )

    def list_documents(self) -> list[str]:
        """
        Lista los documentos almacenados.
        """

        data = self._vector_store.get(
            include=["metadatas"]
        )

        documents = set()

        for metadata in data["metadatas"]:
            if metadata:
                documents.add(
                    metadata.get("document_name")
                )

        return sorted(documents)

    def similarity_search_with_score(
        self,
        query: str,
        k: int,
    ):
        """
        Busca documentos junto con su score.

        Retorna:
        [
            (Document, score)
        ]
        """

        return self._vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

    def reset(self) -> None:
        """
        Elimina completamente la base vectorial.

        Uso exclusivo durante desarrollo.
        """

        if self._db_path.exists():
            shutil.rmtree(self._db_path)

        self._db_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._vector_store = self._create_vector_store()


@lru_cache(maxsize=1)
def get_vector_store() -> VectorStore:
    """
    Devuelve una única instancia compartida de VectorStore para
    todo el proceso. Evita cargar el modelo de embeddings y abrir
    múltiples conexiones a ChromaDB por separado en cada servicio
    (UploadService, DeleteService, Retriever, sidebar, etc.).
    """
    return VectorStore()