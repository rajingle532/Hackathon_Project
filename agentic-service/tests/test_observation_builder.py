import pytest
from telemetry.observation_builder import build_telemetry_event, build_hindsight_placeholder

def test_build_telemetry_event():
    state = {"farmer_id": "123", "intent": "disease", "metadata": {"agent_confidence": 0.85}}
    response = {"is_fallback": False}
    
    event = build_telemetry_event(state, response)
    
    assert "interaction_id" in event
    assert event["farmer_id"] == "123"
    assert event["confidence"] == 0.85
    assert event["response_quality"] == "high"

def test_build_hindsight_placeholder():
    telemetry_event = {"interaction_id": "uuid123", "farmer_id": "123", "intent": "disease"}
    placeholder = build_hindsight_placeholder({}, telemetry_event)
    
    assert placeholder["interaction_id"] == "uuid123"
    assert placeholder["outcome_status"] == "pending"
