import datetime

def normalize_feedback(feedback: dict) -> dict:
    if not isinstance(feedback, dict):
        return {}
    
    normalized = {}
    normalized["farmer_id"] = str(feedback.get("farmer_id", "anonymous"))
    normalized["interaction_id"] = str(feedback.get("interaction_id", ""))
    normalized["intent"] = str(feedback.get("intent", "unknown"))
    normalized["agent_used"] = str(feedback.get("agent_used", "none"))
    normalized["feedback_type"] = str(feedback.get("feedback_type", ""))
    if feedback.get("feedback_reason"):
        normalized["feedback_reason"] = str(feedback["feedback_reason"])
    
    if feedback.get("timestamp"):
        normalized["timestamp"] = str(feedback["timestamp"])
    else:
        normalized["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
        
    return normalized

def validate_feedback(feedback: dict) -> bool:
    if not isinstance(feedback, dict):
        return False
    if not feedback.get("interaction_id"):
        return False
    if not feedback.get("feedback_type"):
        return False
    return True
