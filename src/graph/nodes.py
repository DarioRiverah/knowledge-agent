from src.graph.state import AgentState

from src.rag.retriever import Retriever
from src.llm.llm import get_llm
from src.prompts.system_prompt import SYSTEM_PROMPT
from src.prompts.router_prompt import ROUTER_PROMPT
from src.memory.conversation import ConversationMemory


retriever = Retriever()

llm = get_llm()

memory = ConversationMemory()

def analyze_question(
    state: AgentState,
) -> AgentState:
    """
    Clasifica la pregunta usando el LLM.
    """

    prompt = ROUTER_PROMPT.format(
        question=state["question"]
    )


    response = llm.invoke(
        prompt
    )


    route = response.content.strip().lower()


    if route not in ["rag", "direct"]:
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
    Convierte documentos recuperados
    en contexto para el LLM.
    """

    context = "\n\n".join(
        document.page_content
        for document in state["documents"]
    )


    state["context"] = context


    return state



def generate_answer(
    state: AgentState,
) -> AgentState:
    """
    Genera respuesta usando RAG
    y memoria conversacional.
    """


    history = memory.format_history(
        state["messages"]
    )


    prompt = f"""
{SYSTEM_PROMPT}


Historial de conversación:

{history}


Contexto documental:

{state["context"]}


Pregunta actual:

{state["question"]}


Responde utilizando únicamente el contexto documental
cuando la información esté disponible.
"""


    response = llm.invoke(
        prompt
    )


    state["answer"] = response.content


    memory.add_ai_message(
        state["messages"],
        response.content,
    )


    return state


def generate_direct_answer(
    state: AgentState,
) -> AgentState:
    """
    Respuesta directa usando memoria.
    """


    history = memory.format_history(
        state["messages"]
    )


    prompt = f"""
Historial:

{history}


Nueva pregunta:

{state["question"]}
"""


    response = llm.invoke(
        prompt
    )


    state["answer"] = response.content


    state["sources"] = []


    memory.add_ai_message(
        state["messages"],
        response.content,
    )


    return state



def extract_sources(
    state: AgentState,
) -> AgentState:
    """
    Extrae las fuentes utilizadas.
    """

    sources = []


    for document in state["documents"]:

        metadata = document.metadata


        sources.append(
            {
                "document": metadata.get(
                    "document_name"
                ),
                "page": metadata.get(
                    "page"
                ),
            }
        )


    state["sources"] = sources


    return state