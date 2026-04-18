import re
from utils.blocked_prompt_patterns import BLOCKED_PROMPT_PATTERNS
from config import settings

def detect_prompt_injection(message: str) -> bool:
    if not settings.ENABLE_PROMPT_GUARD:
        return False
        
    msg_lower = message.lower()
    for pattern in BLOCKED_PROMPT_PATTERNS:
        if re.search(pattern, msg_lower):
            return True
    return False

def sanitize_prompt(message: str) -> str:
    if not settings.ENABLE_PROMPT_GUARD:
        return message
        
    # Basic sanitization, but returning blocked boolean is usually safer.
    return message
