import pytest
from memory.mongo_conversation_store import get_recent_history_from_mongo, save_message_to_mongo

def test_get_recent_history_from_mongo(monkeypatch):
    class MockCursor:
        def sort(self, key, direction): return self
        def limit(self, l): return [{"_id": "a", "role": "user"}]
    class MockCol:
        def find(self, q): return MockCursor()
        
    monkeypatch.setattr("memory.mongo_conversation_store.get_conversation_collection", lambda: MockCol())
    
    docs = get_recent_history_from_mongo("1")
    assert len(docs) == 1
    assert "_id" not in docs[0]

def test_save_message_to_mongo(monkeypatch):
    class MockCol:
        def insert_one(self, doc): pass
    monkeypatch.setattr("memory.mongo_conversation_store.get_conversation_collection", lambda: MockCol())
    
    success = save_message_to_mongo({"farmer_id": "1", "role": "user"})
    assert success == True
