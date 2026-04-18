import chromadb
from config import settings
from utils.logger import setup_logger

log = setup_logger("chroma_client")

_client = None

def get_chroma_client():
    """Create or return a persistent ChromaDB client."""
    global _client
    if _client is None:
        log.info(f"Initializing ChromaDB client at {settings.CHROMA_DB_DIR}")
        _client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
    return _client

def get_or_create_collection(collection_name: str = "agriculture_knowledge"):
    """Get or create a ChromaDB collection."""
    client = get_chroma_client()
    # We do not pass an embedding function here because we handle it in vectorstore
    collection = client.get_or_create_collection(name=collection_name)
    return collection
