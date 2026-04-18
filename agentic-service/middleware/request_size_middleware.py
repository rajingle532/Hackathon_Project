from fastapi import Request, HTTPException
from config import settings

async def request_size_middleware(request: Request, call_next):
    # If the content length header exists, check it
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.MAX_REQUEST_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="Payload Too Large")
        
    return await call_next(request)
