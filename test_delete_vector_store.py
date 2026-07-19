from src.rag.vector_store import VectorStore


def main():

    vector_store = VectorStore()

    print("Antes:")
    print(vector_store.list_documents())

    vector_store.delete_document(
        "Guía de Tiempos y Costos de Envío de BimBam Buy.pdf"
    )

    print("\nDespués:")
    print(vector_store.list_documents())


if __name__ == "__main__":
    main()