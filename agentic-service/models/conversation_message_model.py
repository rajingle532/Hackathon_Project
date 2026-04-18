import datetime

def normalize_conversation_message(message: dict) -> dict:
    if not isinstance(message, dict):
        return {}
        
    normalized = {}
    
    if message.get("farmer_id"):
        normalized["farmer_id"] = str(message.get("farmer_id"))
        
    if message.get("role"):
        normalized["role"] = str(message.get("role"))
        
    if message.get("content"):
        normalized["content"] = str(message.get("content"))
        
    if message.get("intent"):
        normalized["intent"] = str(message.get("intent"))
        
    normalized["metadata"] = message.get("metadata", {})
    
    if message.get("timestamp"):
        normalized["timestamp"] = str(message.get("timestamp"))
    else:
        normalized["timestamp"] = datetime.datetime.utcnow().isoformat()
        
    return normalized

def validate_conversation_message(message: dict) -> bool:
    if not isinstance(message, dict):
        return False
    if not message.get("farmer_id"):
        return False
    if not message.get("role"):
        return False
    return True
