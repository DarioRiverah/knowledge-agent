from src.rag.embeddings import EmbeddingModel


def main():
    embedding_model = EmbeddingModel()

    vector = embedding_model.model.embed_query(
        "¿Cuál es la política de devoluciones?"
    )

    print(f"Dimensión del embedding: {len(vector)}")
    print(f"Primeros valores: {vector[:10]}")


if __name__ == "__main__":
    main()