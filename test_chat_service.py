from src.services.chat_service import ChatService


def main():

    chat = ChatService()

    question = (
        "¿Como funciona la politica de reembolso?"
    )

    answer = chat.ask(
        question
    )

    print("\nPregunta:")
    print(question)

    print("\nRespuesta:")
    print(answer)


if __name__ == "__main__":
    main()