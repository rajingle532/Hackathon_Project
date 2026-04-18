from services.retrieval_service import get_retrieval_context, get_retrieval_metadata

def retrieve_context(message: str) -> str:
    """Retrieve agricultural knowledge snippet using the retrieval service."""
    return get_retrieval_context(message)

def retrieve_context_with_metadata(message: str) -> dict:
    """Retrieve agricultural knowledge along with metadata."""
    return get_retrieval_metadata(message)
