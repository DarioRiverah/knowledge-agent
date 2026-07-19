from config import settings
from src.rag.loader import DocumentLoader
from src.rag.splitter import TextSplitter
from src.utils.id_generator import DocumentIdGenerator


def main():
    loader = DocumentLoader()
    splitter = TextSplitter()

    documents = loader.load_directory(settings.documents_path)
    chunks = splitter.split(documents)

    chunk = chunks[0]

    chunk = DocumentIdGenerator.enrich_metadata(chunk, 0)

    chunk_id = DocumentIdGenerator.generate(chunk, 0)

    print("ID generado:")
    print(chunk_id)

    print("\nMetadata:")
    print(chunk.metadata)


if __name__ == "__main__":
    main()