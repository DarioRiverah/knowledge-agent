import streamlit as st

from config import settings
from src.rag.vector_store import get_vector_store
from src.rag.loader import DocumentLoader
from src.rag.splitter import TextSplitter
from src.utils.id_generator import DocumentIdGenerator

from src.ui.chat import render_chat
from src.ui.sidebar import render_sidebar
from src.ui.styles import load_styles


def ensure_documents_indexed() -> None:
    """
    Verifica que la base vectorial tenga documentos indexados y,
    si está vacía, indexa automáticamente todo lo disponible en
    data/documents/.

    Necesario porque en Streamlit Community Cloud el sistema de
    archivos es efímero: cada reinicio de la app (por inactividad,
    actualización de código, etc.) borra data/chroma_db/. Sin esto,
    el bot arrancaría sin ningún documento cargado.
    """

    vector_store = get_vector_store()

    if vector_store.list_documents():
        return

    loader = DocumentLoader()
    splitter = TextSplitter()

    documents = loader.load_directory(settings.documents_path)

    if not documents:
        return

    chunks = splitter.split(documents)

    ids = []

    for index, chunk in enumerate(chunks):
        DocumentIdGenerator.enrich_metadata(chunk, index)
        ids.append(DocumentIdGenerator.generate(chunk, index))

    vector_store.add_documents(chunks, ids)


st.set_page_config(
    page_title="BimBam Boy",
    page_icon="🤖",
    layout="wide",
)

ensure_documents_indexed()

load_styles()

render_sidebar()

render_chat()