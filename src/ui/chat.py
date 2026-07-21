import streamlit as st
from src.services.agent_service import AgentService

service = AgentService()

def render_chat():
    """
    Interfaz principal del chat.
    """

    col1, col2 = st.columns([2, 5], vertical_alignment="center")
    with col1:
        st.image("assets/img/bimbam_boy.png", width=340)
    with col2:
        st.markdown(
            "<p class='bimbam-header-title'>BimBam Boy</p>"
            "<p class='bimbam-header-subtitle'>Tu asistente experto en BimBam Buy</p>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        ¡Hola! 👋 Soy tu asistente virtual oficial.
        Estoy aquí para resolver tus dudas sobre la documentación de BimBam Buy.

        **Puedo ayudarte con:**
        *   📦 Envíos y entregas
        *   💳 Opciones y métodos de pago
        *   💰 Políticas de reembolsos y devoluciones
        *   🤝 Detalles del programa de afiliados

        *Recuerda que mis respuestas se basan exclusivamente en la información de los documentos proporcionados.*
        """
    )
    st.divider()

    # Inicializar el estado de la sesión si es necesario
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensaje de bienvenida si no hay historial
    if not st.session_state.messages:
        st.info("👋 ¡Empecemos! Hazme tu primera pregunta sobre BimBam Buy.")

    # Mostrar historial de mensajes
    for message in st.session_state.messages:
        avatar = "assets/img/bimbam_boy.png" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Entrada del usuario
    question = st.chat_input("Escribe tu pregunta aquí...")

    if question:
        # Añadir y mostrar la pregunta del usuario
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Mostrar indicador de carga mientras el bot piensa
        with st.chat_message("assistant", avatar="assets/img/bimbam_boy.png"):
            with st.spinner("🤔 Pensando mi respuesta..."):
                try:
                    response = service.chat(question)

                    # Añadir y mostrar la respuesta del bot
                    st.session_state.messages.append({"role": "assistant", "content": response.answer})
                    st.markdown(response.answer)

                    # Mostrar las fuentes de manera más elegante
                    if response.sources:
                        with st.expander("📚 Ver fuentes consultadas", expanded=False):
                            for source in response.sources:
                                st.markdown(f"- **Documento:** {source['document']} (Página {source['page']})")
                except Exception as e:
                    # Manejo básico de errores para que la app no se rompa
                    error_msg = f"Lo siento, ocurrió un error al procesar tu pregunta. Por favor, intenta de nuevo. (Detalle: {e})"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})