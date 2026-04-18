from fastapi import Request, HTTPException
from security.rate_limit_service import check_rate_limit, increment_rate_limit
from background.event_dispatcher import dispatch_event
from background.event_types import EVENT_TYPES

async def rate_limit_middleware(request: Request, call_next):
    # Handled in route in main.py for simpler dependency injection
    return await call_next(request)
