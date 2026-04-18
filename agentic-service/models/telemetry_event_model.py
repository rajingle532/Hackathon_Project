import datetime

def normalize_telemetry_event(event: dict) -> dict:
    if not isinstance(event, dict):
        return {}
        
    normalized = {}
    normalized["interaction_id"] = str(event.get("interaction_id", ""))
    normalized["farmer_id"] = str(event.get("farmer_id", "anonymous"))
    normalized["intent"] = str(event.get("intent", "unknown"))
    normalized["agent_used"] = str(event.get("agent_used", "none"))
    
    normalized["confidence"] = float(event.get("confidence", 0.0))
    normalized["is_fallback"] = bool(event.get("is_fallback", False))
    normalized["response_score"] = float(event.get("response_score", 0.0))
    normalized["response_quality"] = str(event.get("response_quality", "unknown"))
    
    if event.get("timestamp"):
        normalized["timestamp"] = str(event["timestamp"])
    else:
        normalized["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
        
    return normalized

def validate_telemetry_event(event: dict) -> bool:
    if not isinstance(event, dict):
        return False
    if not event.get("interaction_id"):
        return False
    return True
