import re
from utils.pii_patterns import PII_PATTERNS
from config import settings

def mask_pii(text: str) -> str:
    if not settings.ENABLE_PII_MASKING:
        return text
        
    masked_text = text
    for pii_type, pattern in PII_PATTERNS.items():
        masked_text = re.sub(pattern, f"[{pii_type}]", masked_text)
        
    return masked_text
