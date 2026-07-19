from pathlib import Path

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document

from src.exceptions import UnsupportedDocumentError


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
}


class DocumentLoader:
    """
    Responsable de cargar documentos soportados y convertirlos
    en objetos Document de LangChain.
    """

    _LOADERS = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
        ".md": TextLoader,
    }

    def load(self, file_path: str) -> list[Document]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"El archivo '{path}' no existe.")

        loader = self._get_loader(path)

        return loader.load()

    def load_directory(self, directory: str) -> list[Document]:
        path = Path(directory)

        if not path.exists():
            raise FileNotFoundError(f"La carpeta '{path}' no existe.")

        documents = []

        for file in path.iterdir():
            if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
                documents.extend(self.load(str(file)))

        return documents

    def _get_loader(self, file_path: Path):
        extension = file_path.suffix.lower()

        loader_class = self._LOADERS.get(extension)

        if loader_class is None:
            raise UnsupportedDocumentError(
                f"El formato '{extension}' no está soportado."
            )

        return loader_class(str(file_path))