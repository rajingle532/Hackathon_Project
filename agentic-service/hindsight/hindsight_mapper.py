def map_internal_hindsight_to_provider(payload: dict) -> dict:
    """
    Map the internal Krishi Sakhi hindsight schema to the external Hindsight API schema.
    This acts as an abstraction layer so external schema changes don't affect internal models.
    """
    if not payload:
        return {}
        
    return {
        "event_id": payload.get("interaction_id"),
        "user_id": payload.get("farmer_id"),
        "agent_name": payload.get("agent_used"),
        "intent": payload.get("intent"),
        "prediction": payload.get("original_prediction"),
        "status": payload.get("outcome_status"),
        "reason": payload.get("outcome_reason"),
        "created_at": payload.get("timestamp")
    }

def map_provider_hindsight_to_internal(payload: dict) -> dict:
    """
    Map the external Hindsight API response schema back to the internal schema.
    """
    if not payload:
        return {}
        
    return {
        "interaction_id": payload.get("event_id"),
        "farmer_id": payload.get("user_id"),
        "agent_used": payload.get("agent_name"),
        "intent": payload.get("intent"),
        "original_prediction": payload.get("prediction"),
        "outcome_status": payload.get("status"),
        "outcome_reason": payload.get("reason"),
        "timestamp": payload.get("created_at")
    }
