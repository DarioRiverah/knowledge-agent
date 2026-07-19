import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # ==========================
    # LLM
    # ==========================
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    temperature: float = float(os.getenv("TEMPERATURE", 0))

    # ==========================
    # Embeddings
    # ==========================
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )

    # ==========================
    # RAG
    # ==========================
    top_k: int = int(os.getenv("TOP_K", 4))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", 1000))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", 200))

    # ==========================
    # Rutas
    # ==========================
    chroma_path: str = os.getenv("CHROMA_PATH", "data/chroma_db")
    documents_path: str = os.getenv("DOCUMENTS_PATH", "data/documents")


settings = Settings()