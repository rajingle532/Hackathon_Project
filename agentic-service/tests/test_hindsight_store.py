import pytest
from telemetry.hindsight_store import save_hindsight_log, get_hindsight_by_interaction

def test_save_hindsight_log(monkeypatch):
    class MockCol:
        def insert_one(self, doc): pass
    monkeypatch.setattr("telemetry.hindsight_store.get_hindsight_collection", lambda: MockCol())
    
    assert save_hindsight_log({"interaction_id": "123"}) == True

def test_get_hindsight_by_interaction(monkeypatch):
    class MockCol:
        def find(self, q): return [{"_id": "1", "interaction_id": "123"}]
    monkeypatch.setattr("telemetry.hindsight_store.get_hindsight_collection", lambda: MockCol())
    
    docs = get_hindsight_by_interaction("123")
    assert len(docs) == 1
    assert "_id" not in docs[0]
