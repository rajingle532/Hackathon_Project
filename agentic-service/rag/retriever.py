from config import settings
from rag.vectorstore import semantic_search
from utils.logger import setup_logger

log = setup_logger("retriever")

def retrieve_relevant_context(query: str, top_k: int = None) -> dict:
    """
    Wrap semantic search logic and format output.
    Returns: {"retrieval_context": str, "sources": list, "categories": list, "scores": list}
    """
    if top_k is None:
        top_k = settings.TOP_K_RESULTS
        
    results = semantic_search(query, top_k=top_k)
    
    if not results:
        return {
            "retrieval_context": "",
            "sources": [],
            "categories": [],
            "scores": []
        }
        
    # We'll concatenate the retrieved texts for the LLM
    context_parts = []
    sources = []
    categories = []
    scores = []
    
    for res in results:
        doc_text = res["document"]
        meta = res["metadata"]
        
        context_parts.append(doc_text)
        sources.append(meta.get("source", "unknown"))
        categories.append(meta.get("category", "unknown"))
        scores.append(res["score"])
        
    return {
        "retrieval_context": "\n---\n".join(context_parts),
        "sources": sources,
        "categories": categories,
        "scores": scores
    }
