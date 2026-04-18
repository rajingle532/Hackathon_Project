import time
from config import settings

# Simple in-memory rate limiting. In production, use Redis.
_rate_limits = {}

def check_rate_limit(identifier: str) -> bool:
    if not settings.ENABLE_RATE_LIMITING:
        return True
        
    current_time = time.time()
    record = _rate_limits.get(identifier)
    
    if record:
        if current_time - record["start_time"] > settings.RATE_LIMIT_WINDOW_SECONDS:
            return True # Window expired
        if record["count"] >= settings.RATE_LIMIT_REQUESTS:
            return False # Limit exceeded
            
    return True

def increment_rate_limit(identifier: str) -> None:
    if not settings.ENABLE_RATE_LIMITING:
        return
        
    current_time = time.time()
    record = _rate_limits.get(identifier)
    
    if not record or current_time - record["start_time"] > settings.RATE_LIMIT_WINDOW_SECONDS:
        _rate_limits[identifier] = {"count": 1, "start_time": current_time}
    else:
        _rate_limits[identifier]["count"] += 1
