from src.rag.retriever import Retriever


def main():

    retriever = Retriever()

    question = (
        "¿Cuáles son los métodos de pago disponibles?"
    )

    results = retriever.search(question)

    print(
        f"\nResultados encontrados: {len(results)}\n"
    )

    for index, document in enumerate(results):

        print("=" * 50)

        print(
            f"Resultado {index + 1}"
        )

        print(
            document.page_content[:500]
        )

        print()

        print(
            "Metadata:"
        )

        print(
            document.metadata
        )


if __name__ == "__main__":
    main()