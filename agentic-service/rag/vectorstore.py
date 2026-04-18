from sentence_transformers import SentenceTransformer
from rag.chroma_client import get_or_create_collection
from config import settings
from utils.logger import setup_logger

log = setup_logger("vectorstore")

_embedding_model = None

def get_embedding_model():
    """Load and return the sentence-transformers model."""
    global _embedding_model
    if _embedding_model is None:
        log.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _embedding_model

def embed_text(text: str) -> list[float]:
    """Embed a single text string."""
    model = get_embedding_model()
    # model.encode returns a numpy array, convert to list of floats for ChromaDB
    return model.encode(text).tolist()

def add_documents_to_collection(documents: list[dict], collection_name: str = "agriculture_knowledge"):
    """
    Add documents to ChromaDB.
    documents format: [{"id": "...", "text": "...", "metadata": {...}}]
    """
    collection = get_or_create_collection(collection_name)
    
    ids = []
    texts = []
    metadatas = []
    embeddings = []
    
    for doc in documents:
        # Check if already exists to avoid duplication
        existing = collection.get(ids=[doc["id"]])
        if existing and existing["ids"]:
            continue
            
        ids.append(doc["id"])
        texts.append(doc["text"])
        metadatas.append(doc["metadata"])
        embeddings.append(embed_text(doc["text"]))
        
    if ids:
        collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings
        )
        log.info(f"Added {len(ids)} new documents to collection '{collection_name}'.")
    else:
        log.info("No new documents to add.")

def semantic_search(query: str, top_k: int = 3, collection_name: str = "agriculture_knowledge") -> list[dict]:
    """Search for relevant documents in ChromaDB."""
    collection = get_or_create_collection(collection_name)
    
    # If collection is empty, short circuit
    if collection.count() == 0:
        return []
        
    query_embedding = embed_text(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    formatted_results = []
    if not results or not results["documents"] or not results["documents"][0]:
        return formatted_results
        
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    
    for i in range(len(documents)):
        # Convert distance to a pseudo similarity score
        # For L2 distance, smaller is better. Let's invert it simply for score representation
        # Distance could be large, so we just use 1 / (1 + distance)
        score = round(1.0 / (1.0 + distances[i]), 4)
        
        formatted_results.append({
            "document": documents[i],
            "metadata": metadatas[i],
            "score": score
        })
        
    return formatted_results
