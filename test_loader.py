from config import settings
from src.rag.loader import DocumentLoader


def main():
    loader = DocumentLoader()

    documents = loader.load_directory(settings.documents_path)

    print(f"\nDocumentos cargados: {len(documents)}\n")

    for i, document in enumerate(documents, start=1):
        print(f"========== Documento {i} ==========")
        print(f"Origen: {document.metadata.get('source', 'Desconocido')}")
        print(document.page_content[:300])
        print("-" * 80)


if __name__ == "__main__":
    main()