from src.graph.nodes import (
    retrieve_documents,
    build_context,
    generate_answer,
    extract_sources,
)


def main():

    state = {
        "question": "¿Cómo funciona la política de reembolso?",
        "documents": [],
        "context": "",
        "answer": "",
        "sources": [],
    }


    state = retrieve_documents(
        state
    )


    print(
        "Documentos encontrados:",
        len(state["documents"])
    )


    state = build_context(
        state
    )


    print(
        "Contexto generado:",
        len(state["context"])
    )


    state = generate_answer(
        state
    )


    print(
        "\nRespuesta:"
    )

    print(
        state["answer"]
    )


    state = extract_sources(
        state
    )


    print(
        "\nFuentes:"
    )

    print(
        state["sources"]
    )


if __name__ == "__main__":
    main()