from langchain_huggingface import HuggingFaceEmbeddings

from config import settings


class EmbeddingModel:
    """
    Responsable de crear el modelo de embeddings.
    """

    def __init__(self) -> None:
        self._embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    @property
    def model(self) -> HuggingFaceEmbeddings:
        return self._embeddings