from security.jwt_service import verify_access_token
from security.api_key_service import validate_api_key
from config import settings

def authenticate_request(auth_header: str = None, api_key: str = None) -> dict:
    if not settings.ENABLE_AUTH:
        return {"authenticated": True, "auth_type": "none"}
        
    if api_key and validate_api_key(api_key):
        return {"authenticated": True, "auth_type": "api_key"}
        
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = verify_access_token(token)
        if payload:
            return {"authenticated": True, "auth_type": "jwt", "payload": payload}
            
    return {"authenticated": False, "auth_type": "none"}
