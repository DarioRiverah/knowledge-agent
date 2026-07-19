import re
import unicodedata
from pathlib import Path

from langchain_core.documents import Document


class DocumentIdGenerator:
    """
    Responsable de generar identificadores únicos y enriquecer la metadata
    de los documentos almacenados en la base vectorial.
    """

    @staticmethod
    def generate(document: Document, chunk_index: int) -> str:
        """
        Genera un identificador único para un chunk.

        Formato:
        nombre_documento_normalizado_pagina_chunk

        Ejemplo:
        guia_de_envios_pdf_3_7
        """

        source = document.metadata.get("source", "unknown")
        page = document.metadata.get("page", 0)

        document_name = Path(source).name
        normalized_name = DocumentIdGenerator.normalize(document_name)

        return f"{normalized_name}_{page}_{chunk_index}"

    @staticmethod
    def enrich_metadata(document: Document, chunk_index: int) -> Document:
        """
        Agrega información adicional a la metadata del documento.
        """

        source = document.metadata.get("source", "unknown")
        page = document.metadata.get("page", 0)

        document.metadata["document_name"] = Path(source).name
        document.metadata["normalized_name"] = DocumentIdGenerator.normalize(
            Path(source).name
        )
        document.metadata["page"] = page
        document.metadata["chunk"] = chunk_index

        return document

    @staticmethod
    def normalize(text: str) -> str:
        """
        Convierte un texto en un identificador seguro.

        Ejemplo:
        'Guía de Envíos.pdf'

        ↓

        guia_de_envios_pdf
        """

        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")

        text = text.lower()

        text = re.sub(r"[^a-z0-9]+", "_", text)

        text = re.sub(r"_+", "_", text)

        return text.strip("_")