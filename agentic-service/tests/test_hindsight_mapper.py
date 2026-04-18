from hindsight.hindsight_mapper import map_internal_hindsight_to_provider, map_provider_hindsight_to_internal

def test_map_internal_to_provider():
    internal_payload = {
        "interaction_id": "int_123",
        "farmer_id": "farm_456",
        "agent_used": "weather_agent",
        "intent": "check_weather",
        "original_prediction": "rain",
        "outcome_status": "success",
        "outcome_reason": "user_liked",
        "timestamp": "2023-10-10T10:00:00Z"
    }
    
    provider_payload = map_internal_hindsight_to_provider(internal_payload)
    
    assert provider_payload["event_id"] == "int_123"
    assert provider_payload["user_id"] == "farm_456"
    assert provider_payload["agent_name"] == "weather_agent"
    assert provider_payload["intent"] == "check_weather"
    assert provider_payload["prediction"] == "rain"
    assert provider_payload["status"] == "success"
    assert provider_payload["reason"] == "user_liked"
    assert provider_payload["created_at"] == "2023-10-10T10:00:00Z"

def test_map_provider_to_internal():
    provider_payload = {
        "event_id": "int_123",
        "user_id": "farm_456",
        "agent_name": "weather_agent",
        "intent": "check_weather",
        "prediction": "rain",
        "status": "success",
        "reason": "user_liked",
        "created_at": "2023-10-10T10:00:00Z"
    }
    
    internal_payload = map_provider_hindsight_to_internal(provider_payload)
    
    assert internal_payload["interaction_id"] == "int_123"
    assert internal_payload["farmer_id"] == "farm_456"
    assert internal_payload["agent_used"] == "weather_agent"
    assert internal_payload["intent"] == "check_weather"
    assert internal_payload["original_prediction"] == "rain"
    assert internal_payload["outcome_status"] == "success"
    assert internal_payload["outcome_reason"] == "user_liked"
    assert internal_payload["timestamp"] == "2023-10-10T10:00:00Z"
