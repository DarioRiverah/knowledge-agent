from config import settings

from src.rag.loader import DocumentLoader
from src.rag.splitter import TextSplitter
from src.rag.vector_store import VectorStore
from src.utils.id_generator import DocumentIdGenerator


def main():

    loader = DocumentLoader()
    splitter = TextSplitter()
    vector_store = VectorStore()

    documents = loader.load_directory(
        settings.documents_path
    )

    chunks = splitter.split(documents)

    ids = []

    for index, chunk in enumerate(chunks):

        DocumentIdGenerator.enrich_metadata(
            chunk,
            index,
        )

        ids.append(
            DocumentIdGenerator.generate(
                chunk,
                index,
            )
        )

    vector_store.add_documents(
        chunks,
        ids,
    )

    print("\nDocumentos almacenados:")

    for document in vector_store.list_documents():
        print("-", document)


if __name__ == "__main__":
    main()