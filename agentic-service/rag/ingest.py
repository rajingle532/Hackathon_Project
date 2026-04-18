import os
from config import settings
from rag.vectorstore import add_documents_to_collection
from utils.logger import setup_logger

log = setup_logger("ingest")

def load_knowledge_base_documents() -> list[dict]:
    """Load text files from the knowledge base directory."""
    kb_dir = settings.KNOWLEDGE_BASE_DIR
    documents = []
    
    if not os.path.exists(kb_dir):
        log.warning(f"Knowledge base directory '{kb_dir}' does not exist.")
        return documents
        
    for filename in os.listdir(kb_dir):
        if not filename.endswith(".txt"):
            continue
            
        filepath = os.path.join(kb_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().strip()
            
        if not text:
            continue
            
        # Infer category from filename (e.g., yellow_leaves.txt -> crop_health)
        category = "general"
        if "disease" in filename or "pest" in filename or "yellow" in filename:
            category = "crop_health"
        elif "irrigation" in filename or "water" in filename:
            category = "irrigation"
        elif "fertilizer" in filename or "soil" in filename:
            category = "soil_health"
            
        # Create chunk
        doc_id = f"{filename}_chunk_0"
        
        documents.append({
            "id": doc_id,
            "text": text,
            "metadata": {
                "source": filename,
                "category": category
            }
        })
        
    return documents

def ingest_documents():
    """Main ingestion script."""
    log.info("Starting document ingestion...")
    documents = load_knowledge_base_documents()
    
    if not documents:
        log.info("No documents found to ingest.")
        return
        
    add_documents_to_collection(documents)
    log.info(f"Successfully processed {len(documents)} document(s).")

if __name__ == "__main__":
    ingest_documents()
