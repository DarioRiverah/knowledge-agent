import streamlit as st

from src.ui.chat import render_chat
from src.ui.sidebar import render_sidebar
from src.ui.styles import load_styles


st.set_page_config(
    page_title="BimBam Boy",
    page_icon="🤖",
    layout="wide",
)

load_styles()

render_sidebar()

render_chat()