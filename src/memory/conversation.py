from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)


class ConversationMemory:
    """
    Administra el historial de conversación.
    """


    def add_user_message(
        self,
        messages: list,
        content: str,
    ) -> list:

        messages.append(
            HumanMessage(
                content=content
            )
        )

        return messages



    def add_ai_message(
        self,
        messages: list,
        content: str,
    ) -> list:

        messages.append(
            AIMessage(
                content=content
            )
        )

        return messages



    def format_history(
        self,
        messages: list,
    ) -> str:
        """
        Convierte mensajes en texto.
        """

        history = []


        for message in messages:

            role = (
                "Usuario"
                if isinstance(
                    message,
                    HumanMessage,
                )
                else "Asistente"
            )


            history.append(
                f"{role}: {message.content}"
            )


        return "\n".join(history)