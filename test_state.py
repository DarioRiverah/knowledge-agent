from src.graph.state import AgentState


def main():

    state: AgentState = {
        "question": "¿Cómo funcionan los reembolsos?",
        "documents": [],
        "context": "",
        "answer": "",
        "sources": [],
    }

    print(state)


if __name__ == "__main__":
    main()