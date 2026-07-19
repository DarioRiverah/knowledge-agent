# knowledge-agent
```
knowledge-agent
├─ app.py
├─ config.py
├─ data
│  └─ documents
├─ README.md
├─ requirements.txt
├─ src
│  ├─ exceptions
│  │  ├─ document_exceptions.py
│  │  └─ __init__.py
│  ├─ graph
│  │  ├─ graph.py
│  │  ├─ nodes.py
│  │  └─ state.py
│  ├─ llm
│  │  └─ llm.py
│  ├─ models
│  │  └─ document.py
│  ├─ prompts
│  │  └─ system_prompt.py
│  ├─ rag
│  │  ├─ embeddings.py
│  │  ├─ loader.py
│  │  ├─ retriever.py
│  │  ├─ splitter.py
│  │  └─ vector_store.py
│  ├─ services
│  │  ├─ chat_service.py
│  │  ├─ delete_service.py
│  │  ├─ document_service.py
│  │  └─ upload_service.py
│  ├─ ui
│  │  ├─ chat.py
│  │  ├─ components.py
│  │  └─ sidebar.py
│  └─ utils
│     └─ logger.py
└─ test_llm.py

```