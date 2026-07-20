from src.services.chat_service import ChatService


def main():

    chat = ChatService()

    question = (
        "¿Qué beneficios tiene el Programa Diamante?"
    )

    response = chat.ask(
        question
    )

    print("\nPregunta:")
    print(question)

    print("\nRespuesta:")
    print(response.answer)

    print("\nFuentes:")

    for source in response.sources:
        print(
            f"- {source['document']} "
            f"(Página {source['page']})"
        )


if __name__ == "__main__":
    main()