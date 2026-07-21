from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)


MAX_HISTORY_MESSAGES = 10


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

        Solo se incluyen los últimos MAX_HISTORY_MESSAGES mensajes,
        para evitar que el prompt crezca sin control en
        conversaciones largas.
        """

        history = []

        recent_messages = messages[-MAX_HISTORY_MESSAGES:]

        for message in recent_messages:

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