import pytest
from models.telemetry_event_model import normalize_telemetry_event, validate_telemetry_event

def test_normalize_telemetry_event():
    raw = {"interaction_id": "123", "confidence": "0.9", "is_fallback": 1}
    norm = normalize_telemetry_event(raw)
    assert norm["interaction_id"] == "123"
    assert norm["confidence"] == 0.9
    assert norm["is_fallback"] == True

def test_validate_telemetry_event():
    assert validate_telemetry_event({"interaction_id": "123"}) == True
    assert validate_telemetry_event({"confidence": 0.9}) == False
