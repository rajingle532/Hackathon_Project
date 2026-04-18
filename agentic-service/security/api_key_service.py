from config import settings

def validate_api_key(api_key: str) -> bool:
    if not settings.ENABLE_API_KEYS:
        return True
    valid_keys = settings.VALID_API_KEYS.split(",")
    return api_key in valid_keys
