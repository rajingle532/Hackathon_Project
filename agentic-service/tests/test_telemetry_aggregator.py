import pytest
from evaluation.telemetry_aggregator import collect_recent_telemetry

def test_collect_recent_telemetry(monkeypatch):
    class MockCol:
        def find(self): return self
        def sort(self, *args): return self
        def limit(self, l): return [{"_id": 1, "test": "data"}]
        
    monkeypatch.setattr("evaluation.telemetry_aggregator.get_database", lambda: {"telemetry_events": MockCol()})
    
    docs = collect_recent_telemetry(10)
    assert len(docs) == 1
    assert "test" in docs[0]
    assert "_id" not in docs[0]
