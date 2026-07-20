from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from src.graph.state import AgentState

from src.graph.nodes import (
    analyze_question,
    retrieve_documents,
    build_context,
    generate_answer,
    generate_direct_answer,
    extract_sources,
)



class AgentGraph:
    """
    Construye y administra
    el grafo del agente.
    """


    def __init__(self):

        self.graph = self._build_graph()



    def _build_graph(self):

        workflow = StateGraph(
            AgentState
        )


        workflow.add_node(
            "analyze_question",
            analyze_question,
        )


        workflow.add_node(
            "retrieve_documents",
            retrieve_documents,
        )


        workflow.add_node(
            "build_context",
            build_context,
        )


        workflow.add_node(
            "generate_answer",
            generate_answer,
        )


        workflow.add_node(
            "generate_direct_answer",
            generate_direct_answer,
        )


        workflow.add_node(
            "extract_sources",
            extract_sources,
        )



        workflow.add_edge(
            START,
            "analyze_question",
        )



        workflow.add_conditional_edges(
            "analyze_question",

            lambda state: state["route"],

            {
                "rag": "retrieve_documents",

                "direct": "generate_direct_answer",
            },
        )



        workflow.add_edge(
            "retrieve_documents",
            "build_context",
        )


        workflow.add_edge(
            "build_context",
            "generate_answer",
        )


        workflow.add_edge(
            "generate_answer",
            "extract_sources",
        )


        workflow.add_edge(
            "extract_sources",
            END,
        )


        workflow.add_edge(
            "generate_direct_answer",
            END,
        )


        return workflow.compile()



    def invoke(
        self,
        state: AgentState,
    ) -> AgentState:

        return self.graph.invoke(
            state
        )