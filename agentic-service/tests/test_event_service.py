import pytest
from services.event_service import build_event_payload

def test_build_event_payload():
    payload = build_event_payload("test", "f1", "i1", {"k": "v"})
    assert payload["event_type"] == "test"
    assert payload["farmer_id"] == "f1"
    assert payload["interaction_id"] == "i1"
    assert payload["metadata"] == {"k": "v"}
    assert "timestamp" in payload
