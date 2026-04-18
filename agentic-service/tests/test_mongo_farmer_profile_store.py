import pytest
from memory.mongo_farmer_profile_store import get_farmer_profile_from_mongo, upsert_farmer_profile

def test_get_farmer_profile_from_mongo(monkeypatch):
    class MockCol:
        def find_one(self, q): return {"farmer_id": "1", "_id": "mongo_id"}
    monkeypatch.setattr("memory.mongo_farmer_profile_store.get_farmer_profile_collection", lambda: MockCol())
    
    doc = get_farmer_profile_from_mongo("1")
    assert doc["farmer_id"] == "1"
    assert "_id" not in doc

def test_upsert_farmer_profile(monkeypatch):
    called = []
    class MockCol:
        def update_one(self, q, u, upsert): called.append(True)
    monkeypatch.setattr("memory.mongo_farmer_profile_store.get_farmer_profile_collection", lambda: MockCol())
    
    upsert_farmer_profile("1", {"farmer_id": "1", "location": "Delhi"})
    assert called == [True]
