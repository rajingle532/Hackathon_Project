import pytest
import os
from rag.ingest import load_knowledge_base_documents

def test_load_knowledge_base_documents(tmpdir, monkeypatch):
    # Mock settings.KNOWLEDGE_BASE_DIR
    import config
    monkeypatch.setattr(config.settings, "KNOWLEDGE_BASE_DIR", str(tmpdir))
    
    # Create mock text file
    f = tmpdir.join("test_crop.txt")
    f.write("This is a test document about crops.")
    
    docs = load_knowledge_base_documents()
    assert len(docs) == 1
    assert docs[0]["metadata"]["source"] == "test_crop.txt"
    assert docs[0]["metadata"]["category"] == "general" # Default category
    assert docs[0]["text"] == "This is a test document about crops."

def test_load_knowledge_base_documents_empty_dir(tmpdir, monkeypatch):
    import config
    monkeypatch.setattr(config.settings, "KNOWLEDGE_BASE_DIR", str(tmpdir))
    
    docs = load_knowledge_base_documents()
    assert len(docs) == 0
