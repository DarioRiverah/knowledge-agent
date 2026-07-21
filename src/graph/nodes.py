import groq

from src.graph.state import AgentState

from src.rag.retriever import Retriever
from src.llm.llm import get_llm
from src.prompts.system_prompt import SYSTEM_PROMPT
from src.prompts.router_prompt import ROUTER_PROMPT


retriever = Retriever()

llm = get_llm()


MENSAJE_ERROR_LLM = (
    "Estoy teniendo problemas técnicos para procesar tu pregunta "
    "en este momento. Por favor, intenta de nuevo en unos segundos."
)

MENSAJE_SIN_INFORMACION = (
    "No encontré información relacionada "
    "en los documentos disponibles."
)


def _invoke_llm(prompt: str) -> str | None:
    """
    Invoca al LLM capturando errores específicos del proveedor
    (Groq), para no dejar que detalles técnicos internos (códigos
    de error, rate limits, etc.) lleguen crudos hasta el usuario.

    Retorna el contenido de la respuesta, o None si ocurrió un
    error controlado (en cuyo caso ya se imprimió el detalle en
    consola para debugging).
    """

    try:
        response = llm.invoke(prompt)
        return response.content

    except groq.RateLimitError as error:
        print(f"[LLM] Rate limit excedido: {error}")
        return None

    except groq.AuthenticationError as error:
        print(f"[LLM] Error de autenticación (revisa GROQ_API_KEY): {error}")
        return None

    except groq.APIConnectionError as error:
        print(f"[LLM] Error de conexión con Groq: {error}")
        return None

    except groq.APIStatusError as error:
        print(f"[LLM] Error de la API de Groq (status {error.status_code}): {error}")
        return None

    except Exception as error:
        print(f"[LLM] Error inesperado invocando al modelo: {error}")
        return None


def analyze_question(
    state: AgentState,
) -> AgentState:
    """
    Clasifica la pregunta usando el LLM.
    """

    prompt = ROUTER_PROMPT.format(
        question=state["question"]
    )

    content = _invoke_llm(prompt)

    if content is None:
        # Si el clasificador falla, optamos por el camino más
        # seguro: intentar responder con RAG en vez de romper
        # el flujo completo del agente.
        state["route"] = "rag"
        return state

    route = content.strip().lower()

    if route not in ["rag", "direct", "off_topic"]:
        route = "rag"

    state["route"] = route

    return state


def retrieve_documents(
    state: AgentState,
) -> AgentState:
    """
    Busca documentos relevantes
    en ChromaDB.
    """

    documents = retriever.search(
        state["question"]
    )

    state["documents"] = documents

    return state


def build_context(
    state: AgentState,
) -> AgentState:
    """
    Convierte los documentos recuperados
    en un contexto estructurado para el LLM.
    """

    if not state["documents"]:
        state["context"] = ""
        return state

    sections = []

    for document in state["documents"]:

        metadata = document.metadata

        sections.append(
            f"""
Documento: {metadata.get("document_name")}
Página: {metadata.get("page")}

Contenido:
{document.page_content}
"""
        )

    state["context"] = "\n\n------------------------------\n\n".join(
        sections
    )

    return state


def validate_context(
    state: AgentState,
) -> AgentState:
    """
    Valida si existe información documental
    suficiente para responder.
    """

    if state["context"].strip():

        state["context_valid"] = True

    else:

        state["context_valid"] = False

        state["answer"] = MENSAJE_SIN_INFORMACION

        state["sources"] = []

    return state


def generate_answer(
    state: AgentState,
) -> AgentState:
    """
    Genera una respuesta utilizando
    RAG y memoria conversacional.
    """

    if not state["context_valid"]:
        return state

    history = state["memory"].format_history(
        state["messages"]
    )

    prompt = f"""
{SYSTEM_PROMPT}

Historial de conversación:

{history}

Contexto documental:

{state["context"]}

Pregunta del usuario:

{state["question"]}

Respuesta:
"""

    content = _invoke_llm(prompt)

    if content is None:
        state["answer"] = MENSAJE_ERROR_LLM
        state["sources"] = []
        return state

    state["answer"] = content

    state["memory"].add_ai_message(
        state["messages"],
        content,
    )

    return state


def generate_direct_answer(
    state: AgentState,
) -> AgentState:
    """
    Respuesta directa usando memoria.
    """

    history = state["memory"].format_history(
        state["messages"]
    )

    prompt = f"""
Eres BimBam Boy, el asistente virtual oficial de BimBam Buy.

Mantén una conversación amable y profesional.

Historial:

{history}

Nueva pregunta:

{state["question"]}

Respuesta:
"""

    content = _invoke_llm(prompt)

    if content is None:
        state["answer"] = MENSAJE_ERROR_LLM
        state["sources"] = []
        return state

    state["answer"] = content

    state["sources"] = []

    state["memory"].add_ai_message(
        state["messages"],
        content,
    )

    return state


def generate_off_topic_answer(
    state: AgentState,
) -> AgentState:
    """
    Responde con un mensaje fijo cuando la pregunta es claramente
    ajena a BimBam Buy, sin gastar una llamada al LLM ni consultar
    la base vectorial.
    """

    state["answer"] = (
        "Soy el asistente virtual de BimBam Buy, así que solo puedo "
        "ayudarte con temas relacionados a la empresa: envíos, pagos, "
        "reembolsos, devoluciones y el programa de afiliados. "
        "¿Hay algo de eso en lo que te pueda ayudar?"
    )

    state["sources"] = []

    return state


def extract_sources(
    state: AgentState,
) -> AgentState:
    """
    Extrae las fuentes utilizadas
    eliminando duplicados.

    Si la respuesta final del LLM terminó siendo el mensaje de
    "no encontré información" (aunque sí se hayan recuperado
    documentos que pasaron el threshold), no tiene sentido mostrar
    fuentes -- sería contradictorio para el usuario ver "Ver fuentes
    consultadas" junto a un mensaje que dice que no se encontró nada.
    """

    if state["answer"].strip() == MENSAJE_SIN_INFORMACION:
        state["sources"] = []
        return state

    sources = []

    seen = set()

    for document in state["documents"]:

        metadata = document.metadata

        document_name = metadata.get(
            "document_name"
        )

        page = metadata.get(
            "page"
        )

        source_key = (
            document_name,
            page,
        )

        if source_key not in seen:

            sources.append(
                {
                    "document": document_name,
                    "page": page,
                }
            )

            seen.add(
                source_key
            )

    state["sources"] = sources

    return state