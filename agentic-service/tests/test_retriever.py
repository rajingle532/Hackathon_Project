import pytest
from rag.retriever import retrieve_relevant_context

def test_retrieve_relevant_context(monkeypatch):
    def mock_semantic_search(query, top_k=3):
        return [
            {
                "document": "Test doc",
                "metadata": {"source": "test.txt", "category": "general"},
                "score": 0.99
            }
        ]
        
    monkeypatch.setattr("rag.retriever.semantic_search", mock_semantic_search)
    
    result = retrieve_relevant_context("test query")
    assert result["retrieval_context"] == "Test doc"
    assert "test.txt" in result["sources"]
    assert "general" in result["categories"]
    assert 0.99 in result["scores"]

def test_retrieve_relevant_context_empty(monkeypatch):
    def mock_semantic_search_empty(query, top_k=3):
        return []
        
    monkeypatch.setattr("rag.retriever.semantic_search", mock_semantic_search_empty)
    
    result = retrieve_relevant_context("test query")
    assert result["retrieval_context"] == ""
    assert result["sources"] == []
