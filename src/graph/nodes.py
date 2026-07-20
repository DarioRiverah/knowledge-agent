from src.graph.state import AgentState

from src.rag.retriever import Retriever
from src.llm.llm import get_llm
from src.prompts.system_prompt import SYSTEM_PROMPT


retriever = Retriever()

llm = get_llm()



def analyze_question(
    state: AgentState,
) -> AgentState:
    """
    Analiza si la pregunta necesita
    consultar documentos.
    """

    question = state["question"].lower()


    keywords = [
        "política",
        "politica",
        "documento",
        "envío",
        "envio",
        "reembolso",
        "devolución",
        "devolucion",
        "garantía",
        "garantia",
        "pago",
        "pedido",
        "afiliado",
        "cliente",
    ]


    needs_documents = any(
        keyword in question
        for keyword in keywords
    )


    state["needs_documents"] = needs_documents


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
    Genera respuesta usando RAG.
    """

    prompt = SYSTEM_PROMPT.format(
        context=state["context"],
        question=state["question"],
    )


    response = llm.invoke(
        prompt
    )


    state["answer"] = response.content


    return state



def generate_direct_answer(
    state: AgentState,
) -> AgentState:
    """
    Genera respuestas simples
    sin consultar documentos.
    """

    response = llm.invoke(
        state["question"]
    )


    state["answer"] = response.content


    state["sources"] = []


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