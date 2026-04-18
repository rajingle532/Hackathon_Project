from config import settings
from tools.consultant_parser_tool import consultant_requested, extract_consultant_type, extract_escalation_reason

def escalation_needed(intent: str, confidence: float, message: str) -> bool:
    if consultant_requested(message):
        return True
    if confidence < settings.ESCALATION_CONFIDENCE_THRESHOLD:
        return True
    return False

def get_escalation_context(intent: str, confidence: float, message: str) -> dict:
    requires_escalation = escalation_needed(intent, confidence, message)
    if not requires_escalation:
        return {"requires_escalation": False}
        
    consultant_type = extract_consultant_type(intent)
    reason = extract_escalation_reason(message, confidence, intent)
    
    return {
        "requires_escalation": True,
        "consultant_type": consultant_type,
        "escalation_reason": reason,
        "escalation_target": settings.DEFAULT_ESCALATION_TARGET
    }
