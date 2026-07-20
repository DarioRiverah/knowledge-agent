from src.graph.graph import AgentGraph
from langchain_core.messages import HumanMessage


def main():

    agent = AgentGraph()


    state = {

    "question": "¿Cual me recomiendas?",

    "route": "",

    "messages": [
        HumanMessage(
            content="Hola"
        )
    ],

    "documents": [],

    "context": "",

    "answer": "",

    "sources": [],

}


    result = agent.invoke(
        state
    )


    print("\nRespuesta:")
    print(
        result["answer"]
    )


    print("\nFuentes:")

    for source in result["sources"]:
        print(
            f"- {source['document']} "
            f"(Página {source['page']})"
        )


if __name__ == "__main__":
    main()