from pathlib import Path
import streamlit as st

from src.exceptions.document_exceptions import DocumentAlreadyExistsError
from src.rag.vector_store import get_vector_store
from src.services.delete_service import DeleteService
from src.services.upload_service import UploadService

vector_store = get_vector_store()
delete_service = DeleteService()
upload_service = UploadService()

def render_sidebar() -> None:
    """
    Renderiza la barra lateral de la aplicación.
    """
    with st.sidebar:
        col1, col2 = st.columns([1, 3], vertical_alignment="center")
        with col1:
            st.image("assets/img/bimbam_boy.png", width=80)
        with col2:
            st.markdown(
                "<p style='font-weight:700; font-size:1.3rem; margin-bottom:0;'>BimBam Boy</p>"
                "<p style='color:#9FB3D9; font-size:0.85rem; margin-top:0;'>Asistente virtual</p>",
                unsafe_allow_html=True,
            )
        
        st.divider()
        
        st.subheader("📤 Gestión de Documentos") # Título más general
        
        uploaded_file = st.file_uploader(
            "Selecciona un PDF o TXT para subir", # Texto más descriptivo
            type=["pdf", "txt"],
            help="Sube documentos para que BimBam Boy pueda aprender de ellos." # Añadida ayuda
        )

        if uploaded_file is not None:
            upload_path = Path("data/uploads") / uploaded_file.name
            upload_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(upload_path, "wb") as file:
                file.write(uploaded_file.getbuffer())
                
            try:
                with st.spinner("Procesando documento... esto puede tardar un momento. ⏳"): # Mensaje de carga más amigable
                    chunks = upload_service.upload(str(upload_path))
                st.success(f"¡Éxito! Documento '{uploaded_file.name}' agregado ({chunks} chunks). 🎉") # Mensaje de éxito mejorado
                st.rerun()
            except DocumentAlreadyExistsError:
                st.warning(f"⚠️ El documento '{uploaded_file.name}' ya se encuentra cargado.") # Mensaje de advertencia mejorado
            finally:
                # data/uploads/ es solo un buffer temporal de recepción;
                # el archivo real ya vive en data/documents/ (copiado por
                # upload_service). Lo limpiamos aquí sin importar si la
                # subida fue exitosa o si el documento ya existía, para
                # no dejar copias huérfanas acumulándose.
                if upload_path.exists():
                    upload_path.unlink()

        st.divider()

        documents = vector_store.list_documents()
        st.subheader(f"📄 Documentos Cargados ({len(documents)})")

        if documents:
            # Usar un contenedor con scroll si hay muchos documentos
            with st.container(height=300): 
                for document in documents:
                    col1, col2 = st.columns([4, 1]) # Ajustado el ancho de las columnas
                    
                    with col1:
                        st.markdown(f"**{document}**") # Negrita para el nombre del documento
                        
                    with col2:
                        if st.button("🗑️", key=document, help=f"Eliminar {document}", use_container_width=True):
                            delete_service.delete(document)
                            st.success(f"Documento '{document}' eliminado.")
                            st.rerun()
        else:
            st.info("No hay documentos cargados actualmente. ¡Sube uno para empezar! ⬆️") # Mensaje más animado

        st.divider()

        if st.button("🗑️ Limpiar Historial de Chat", use_container_width=True, type="primary"): # Añadido icono, texto más claro, tipo primary
            st.session_state.messages = []
            st.rerun()