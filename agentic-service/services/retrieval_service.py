from rag.retriever import retrieve_relevant_context
from utils.logger import setup_logger

log = setup_logger("retrieval_service")

def get_retrieval_context(message: str) -> str:
    """Retrieve agricultural knowledge context using semantic search."""
    try:
        results = retrieve_relevant_context(message)
        return results.get("retrieval_context", "")
    except Exception as e:
        log.error(f"Semantic retrieval failed: {e}")
        return ""

def get_retrieval_metadata(message: str) -> dict:
    """Retrieve the full metadata package from semantic search."""
    try:
        return retrieve_relevant_context(message)
    except Exception as e:
        log.error(f"Semantic retrieval metadata failed: {e}")
        return {
            "retrieval_context": "",
            "sources": [],
            "categories": [],
            "scores": []
        }
