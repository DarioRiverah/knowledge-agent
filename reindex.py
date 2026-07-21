"""
Script de reindexación completa para el agente BimBam Boy.

Uso:
    python reindex.py

Qué hace:
1. Borra por completo la base vectorial actual (Chroma).
2. Vuelve a crearla (ya con la métrica coseno, si ya
   actualizaste vector_store.py).
3. Recorre todos los documentos soportados en data/documents/
   y los vuelve a cargar, trocear, embeber e indexar.

Corre esto UNA sola vez después de cambiar la métrica de
Chroma a coseno. Si lo corres varias veces no pasa nada raro:
el reset() borra todo antes de volver a indexar, así que no
vas a terminar con documentos duplicados.
"""

import gc
from pathlib import Path

from config import settings
from src.rag.loader import DocumentLoader
from src.rag.splitter import TextSplitter
from src.rag.vector_store import VectorStore
from src.utils.id_generator import DocumentIdGenerator


def _force_reset(vector_store: VectorStore) -> VectorStore:
    """
    Borra la base vectorial SIN tocar el archivo .sqlite3 desde
    afuera. En Windows, shutil.rmtree puede fallar por locks de
    archivo (antivirus, Windows Search, handles zombies) incluso
    después de liberar la referencia en Python. Para evitarlo, le
    pedimos a la propia librería de Chroma que borre la colección
    usando su cliente interno -- ella sabe manejar su conexión a
    SQLite mejor que nosotros borrando el archivo por fuera.
    """

    client = vector_store._vector_store._client

    try:
        client.delete_collection(name=settings.collection_name)
        print("   🗑️  Colección eliminada vía API de Chroma.")
    except Exception as error:
        print(
            f"   ⚠️  No se pudo borrar la colección (puede que no "
            f"existiera aún): {error}"
        )

    # Soltar la referencia vieja y forzar limpieza antes de recrear.
    del vector_store._vector_store
    gc.collect()

    # Recrear una instancia nueva; Chroma vuelve a crear la
    # colección vacía automáticamente al inicializarse.
    return VectorStore()


def reindex() -> None:
    documents_path = Path(settings.documents_path)

    if not documents_path.exists():
        print(f"❌ La carpeta '{documents_path}' no existe.")
        return

    print(f"📂 Buscando documentos en: {documents_path}")

    loader = DocumentLoader()
    splitter = TextSplitter()
    vector_store = VectorStore()

    print("🗑️  Borrando base vectorial actual...")
    vector_store = _force_reset(vector_store)

    print("📄 Cargando documentos...")
    documents = loader.load_directory(str(documents_path))

    if not documents:
        print("⚠️  No se encontró ningún documento soportado. Nada que indexar.")
        return

    print(f"✂️  Troceando {len(documents)} páginas/documentos...")
    chunks = splitter.split(documents)

    print(f"🧩 Se generaron {len(chunks)} chunks. Enriqueciendo metadata...")

    ids = []
    seen_names = set()

    for index, chunk in enumerate(chunks):
        DocumentIdGenerator.enrich_metadata(chunk, index)
        ids.append(DocumentIdGenerator.generate(chunk, index))
        seen_names.add(chunk.metadata.get("document_name"))

    print("💾 Guardando en ChromaDB (esto puede tardar un poco)...")
    vector_store.add_documents(chunks, ids)

    print("\n✅ Reindexación completa.")
    print(f"   Documentos procesados: {sorted(seen_names)}")
    print(f"   Total de chunks indexados: {len(chunks)}")


if __name__ == "__main__":
    reindex()