import re
from config import settings

def sanitize_user_input(message: str) -> str:
    if not settings.ENABLE_INPUT_SANITIZATION:
        return message
        
    # Remove null bytes
    sanitized = message.replace('\x00', '')
    
    # Trim excessive whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    # Limit length
    if len(sanitized) > settings.MAX_MESSAGE_LENGTH:
        sanitized = sanitized[:settings.MAX_MESSAGE_LENGTH]
        
    # Remove basic dangerous HTML tags
    sanitized = re.sub(r'<(script|iframe|object|embed|applet)[^>]*>.*?</\1>', '', sanitized, flags=re.IGNORECASE)
    
    return sanitized
