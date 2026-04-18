import pytest
from background.telemetry_tasks import _retry_wrapper, _save_telemetry_event

def test_retry_wrapper_telemetry_success():
    calls = []
    def mock_func():
        calls.append(1)
        return True
        
    res = _retry_wrapper(mock_func)
    assert res == True
    assert len(calls) == 1

def test_save_telemetry_event(monkeypatch):
    class MockCol:
        def insert_one(self, doc): pass
    monkeypatch.setattr("background.telemetry_tasks.get_database", lambda: {"telemetry_events": MockCol()})
    
    res = _save_telemetry_event({"interaction_id": "123"})
    assert res == True
