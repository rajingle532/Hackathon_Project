import pytest
from rag.vectorstore import semantic_search

def test_semantic_search_empty_short_circuit(monkeypatch):
    # If the collection is empty, semantic_search should return an empty list
    class MockCollection:
        def count(self):
            return 0
            
    def mock_get_or_create(*args, **kwargs):
        return MockCollection()
        
    monkeypatch.setattr("rag.vectorstore.get_or_create_collection", mock_get_or_create)
    
    results = semantic_search("query")
    assert results == []

def test_semantic_search_with_results(monkeypatch):
    class MockCollection:
        def count(self):
            return 1
            
        def query(self, *args, **kwargs):
            return {
                "documents": [["Test doc"]],
                "metadatas": [[{"source": "test.txt", "category": "general"}]],
                "distances": [[0.1]]
            }
            
    def mock_get_or_create(*args, **kwargs):
        return MockCollection()
        
    def mock_embed(*args, **kwargs):
        return [0.1, 0.2, 0.3]
        
    monkeypatch.setattr("rag.vectorstore.get_or_create_collection", mock_get_or_create)
    monkeypatch.setattr("rag.vectorstore.embed_text", mock_embed)
    
    results = semantic_search("query")
    assert len(results) == 1
    assert results[0]["document"] == "Test doc"
    assert "score" in results[0]
