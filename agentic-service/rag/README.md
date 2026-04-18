# RAG Layer for Krishi Sakhi

This folder contains the scaffolding and implementation for the ChromaDB-powered RAG (Retrieval-Augmented Generation) system.

## Components

- **chroma_client.py**: Manages the persistent ChromaDB connection.
- **vectorstore.py**: Wraps `sentence-transformers` for embedding text and handles the storage/querying of those embeddings in ChromaDB.
- **ingest.py**: Reads `.txt` files from the `knowledge_base` directory, chunks them, embeds them, and inserts them into ChromaDB.
- **retriever.py**: Performs semantic search and formats the raw ChromaDB output into an easy-to-use dictionary for the Agentic workflow.
- **knowledge_base/**: A folder containing `.txt` documents.

## How to use

1. **Add Documents**: Place your agricultural knowledge `.txt` files inside `rag/knowledge_base/`.
2. **Ingest Documents**: Run the ingestion script from the `agentic-service` root:
   ```bash
   python rag/ingest.py
   ```
   This will create a `data/chroma` directory containing the database.

## Future Improvements
- Upgrade `ingest.py` to support PDF ingestion via LangChain document loaders.
- Implement advanced chunking strategies (e.g. RecursiveCharacterTextSplitter).
- Add Hybrid Search (BM25 + Dense Vectors).
- Implement Cross-Encoder reranking for better relevance scoring.
