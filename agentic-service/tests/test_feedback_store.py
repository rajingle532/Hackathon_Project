import pytest
from telemetry.feedback_store import save_feedback, get_feedback_by_interaction

def test_save_feedback(monkeypatch):
    class MockCol:
        def insert_one(self, doc): pass
    monkeypatch.setattr("telemetry.feedback_store.get_feedback_collection", lambda: MockCol())
    
    assert save_feedback({"interaction_id": "123", "feedback_type": "thumbs_up"}) == True

def test_get_feedback_by_interaction(monkeypatch):
    class MockCol:
        def find(self, q): return [{"_id": "1", "interaction_id": "123"}]
    monkeypatch.setattr("telemetry.feedback_store.get_feedback_collection", lambda: MockCol())
    
    docs = get_feedback_by_interaction("123")
    assert len(docs) == 1
    assert "_id" not in docs[0]
