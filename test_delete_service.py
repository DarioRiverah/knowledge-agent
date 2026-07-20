from src.services.delete_service import DeleteService
from src.rag.vector_store import VectorStore


def main():

    vector_store = VectorStore()

    print("Antes:")
    print(
        vector_store.list_documents()
    )


    service = DeleteService()

    service.delete(
        "test_document.pdf"
    )


    print("\nDespués:")

    print(
        vector_store.list_documents()
    )


if __name__ == "__main__":
    main()