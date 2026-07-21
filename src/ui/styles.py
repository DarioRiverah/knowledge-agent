import streamlit as st


BRAND_BLUE = "#2E5AAC"
BRAND_BLUE_DARK = "#1D3F7A"
BRAND_ORANGE = "#F5821F"
BRAND_ORANGE_LIGHT = "#FCEEDD"
BG_DARK = "#0B1220"
BG_CARD = "#111C33"
BORDER_SUBTLE = "rgba(245, 130, 31, 0.18)"


def load_styles() -> None:
    """
    Carga los estilos CSS de la aplicación, con la paleta de marca
    de BimBam Buy (azul royal + naranja, tomada del personaje
    BimBam Boy).
    """
    st.markdown(
        f"""
        <style>

        .main {{
            padding-top: 1rem;
        }}

        .block-container {{
            padding-top: 3.5rem;
            padding-bottom: 3rem;
            max-width: 820px;
            margin: 0 auto;
        }}

        /* ===== Burbujas de chat ===== */
        .stChatMessage {{
            border-radius: 16px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.9rem;
            border: 1px solid {BORDER_SUBTLE};
            box-shadow: 0 2px 10px rgba(0,0,0,0.18);
        }}

        /* Mensajes del usuario: acento naranja */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
            background: linear-gradient(180deg, rgba(245,130,31,0.14), rgba(245,130,31,0.06));
            border: 1px solid rgba(245,130,31,0.35);
        }}

        /* Mensajes del asistente: acento azul */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
            background: linear-gradient(180deg, rgba(46,90,172,0.16), rgba(46,90,172,0.06));
            border: 1px solid rgba(46,90,172,0.35);
        }}

        /* ===== Botones ===== */
        .stButton>button {{
            border-radius: 10px;
            font-weight: 600;
            border: 1px solid {BORDER_SUBTLE};
            transition: all 0.2s ease;
        }}

        .stButton>button:hover {{
            transform: translateY(-1px);
            border-color: {BRAND_ORANGE};
            box-shadow: 0 4px 10px rgba(245,130,31,0.25);
        }}

        /* ===== Sidebar ===== */
        [data-testid="stSidebar"] {{
            border-right: 1px solid {BORDER_SUBTLE};
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: {BRAND_ORANGE};
        }}

        [data-testid="stFileUploader"] {{
            border: 1px dashed rgba(245,130,31,0.4);
            border-radius: 10px;
            padding: 0.6rem;
        }}

        /* Tarjetas de documentos cargados */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {{
            background: {BG_CARD};
            border-radius: 10px;
            padding: 0.4rem 0.6rem;
            margin-bottom: 0.4rem;
            border: 1px solid {BORDER_SUBTLE};
        }}

        /* ===== Encabezado principal ===== */
        .bimbam-header-title {{
            font-size: 3.2rem;
            font-weight: 700;
            color: {BRAND_ORANGE};
            margin: 0;
            line-height: 1.15;
        }}

        .bimbam-header-subtitle {{
            color: #9FB3D9;
            margin: 0.3rem 0 0 0;
            font-size: 1.4rem;
        }}

        /* ===== Ocultar elementos por defecto de Streamlit ===== */
        footer {{
            visibility: hidden;
        }}

        #MainMenu {{
            visibility: hidden;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )