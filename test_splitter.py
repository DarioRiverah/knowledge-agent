from config import settings
from src.rag.loader import DocumentLoader
from src.rag.splitter import TextSplitter


def main():
    loader = DocumentLoader()
    splitter = TextSplitter()

    documents = loader.load_directory(settings.documents_path)

    chunks = splitter.split(documents)

    print(f"Documentos originales: {len(documents)}")
    print(f"Chunks generados: {len(chunks)}")

    print("\nPrimer chunk:\n")
    print(chunks[0].page_content)


if __name__ == "__main__":
    main()