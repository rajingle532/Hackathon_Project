from security.prompt_guard import detect_prompt_injection, sanitize_prompt
from security.pii_masking_service import mask_pii
from security.input_sanitizer import sanitize_user_input

def secure_message(message: str) -> dict:
    sanitized = sanitize_user_input(message)
    pii_detected = False
    
    # Check if masking changes text
    masked = mask_pii(sanitized)
    if masked != sanitized:
        pii_detected = True
        sanitized = masked
        
    injection_detected = detect_prompt_injection(sanitized)
    blocked = injection_detected
    
    return {
        "sanitized_message": sanitized,
        "pii_detected": pii_detected,
        "prompt_injection_detected": injection_detected,
        "blocked": blocked
    }
