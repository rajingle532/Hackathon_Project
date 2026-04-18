import datetime

def normalize_hindsight_log(log: dict) -> dict:
    if not isinstance(log, dict):
        return {}
        
    normalized = {}
    normalized["farmer_id"] = str(log.get("farmer_id", "anonymous"))
    normalized["interaction_id"] = str(log.get("interaction_id", ""))
    normalized["intent"] = str(log.get("intent", "unknown"))
    normalized["agent_used"] = str(log.get("agent_used", "none"))
    
    if log.get("original_prediction"):
        normalized["original_prediction"] = str(log["original_prediction"])
        
    normalized["outcome_status"] = str(log.get("outcome_status", "pending"))
    
    if log.get("outcome_reason"):
        normalized["outcome_reason"] = str(log["outcome_reason"])
        
    if log.get("timestamp"):
        normalized["timestamp"] = str(log["timestamp"])
    else:
        normalized["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
        
    return normalized

def validate_hindsight_log(log: dict) -> bool:
    if not isinstance(log, dict):
        return False
    if not log.get("interaction_id"):
        return False
    return True
