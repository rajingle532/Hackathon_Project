from config import settings

def validate_chat_request(payload: dict) -> tuple[bool, str]:
    message = payload.get("message", "")
    if not message:
        return False, "Message is required"
        
    if len(message) > settings.MAX_MESSAGE_LENGTH:
        return False, f"Message exceeds maximum length of {settings.MAX_MESSAGE_LENGTH}"
        
    farmer_id = payload.get("farmer_id", "")
    if farmer_id and len(farmer_id) > 100:
        return False, "farmer_id is too long"
        
    lang = payload.get("language", "")
    if lang and len(lang) > 50:
        return False, "language field is too long"
        
    return True, ""
