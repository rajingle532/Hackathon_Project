from utils.escalation_keywords import ESCALATION_KEYWORDS, CONSULTANT_TYPE_MAP
from config import settings

def consultant_requested(message: str) -> bool:
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in ESCALATION_KEYWORDS)

def extract_consultant_type(intent: str) -> str:
    return CONSULTANT_TYPE_MAP.get(intent, settings.DEFAULT_CONSULTANT_TYPE)

def extract_escalation_reason(message: str, confidence: float, intent: str) -> str:
    if consultant_requested(message):
        return "Explicit consultant requested"
    if confidence < settings.ESCALATION_CONFIDENCE_THRESHOLD:
        return f"Low confidence in {intent} advice"
    return "Unknown escalation reason"
