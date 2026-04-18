import datetime

def normalize_agent_interaction(interaction: dict) -> dict:
    if not isinstance(interaction, dict):
        return {}
        
    normalized = {}
    
    if interaction.get("farmer_id"):
        normalized["farmer_id"] = str(interaction.get("farmer_id"))
        
    if interaction.get("intent"):
        normalized["intent"] = str(interaction.get("intent"))
        
    if interaction.get("agent_used"):
        normalized["agent_used"] = str(interaction.get("agent_used"))
        
    if interaction.get("reply"):
        normalized["reply"] = str(interaction.get("reply"))
        
    normalized["metadata"] = interaction.get("metadata", {})
    
    if interaction.get("timestamp"):
        normalized["timestamp"] = str(interaction.get("timestamp"))
    else:
        normalized["timestamp"] = datetime.datetime.utcnow().isoformat()
        
    return normalized

def validate_agent_interaction(interaction: dict) -> bool:
    if not isinstance(interaction, dict):
        return False
    if not interaction.get("farmer_id"):
        return False
    return True
