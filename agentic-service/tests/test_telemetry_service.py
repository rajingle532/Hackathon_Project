import pytest
from telemetry.telemetry_service import record_telemetry_event, record_hindsight_placeholder

def test_record_telemetry_event(monkeypatch):
    class MockCol:
        def insert_one(self, doc): pass
    monkeypatch.setattr("telemetry.telemetry_service.get_telemetry_collection", lambda: MockCol())
    
    state = {"farmer_id": "123"}
    response = {}
    event = record_telemetry_event(state, response)
    
    assert "interaction_id" in event

def test_record_hindsight_placeholder(monkeypatch):
    monkeypatch.setattr("telemetry.telemetry_service.save_hindsight_log", lambda p: True)
    
    placeholder = record_hindsight_placeholder({}, {}, {"interaction_id": "123"})
    assert placeholder["interaction_id"] == "123"
