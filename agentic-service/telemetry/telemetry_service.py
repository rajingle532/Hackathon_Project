import logging
from db.mongo import get_database
from models.telemetry_event_model import normalize_telemetry_event, validate_telemetry_event
from telemetry.observation_builder import build_telemetry_event, build_hindsight_placeholder
from telemetry.hindsight_store import save_hindsight_log
from config import settings

log = logging.getLogger("telemetry_service")

def get_telemetry_collection():
    db = get_database()
    if db is not None:
        return db[settings.TELEMETRY_COLLECTION]
    return None

def record_telemetry_event(state: dict, response: dict) -> dict:
    event = build_telemetry_event(state, response)
    
    if not settings.ENABLE_TELEMETRY:
        return event
        
    if settings.ENABLE_ASYNC_TELEMETRY:
        return event
        
    try:
        col = get_telemetry_collection()
        if col is not None:
            norm = normalize_telemetry_event(event)
            if validate_telemetry_event(norm):
                col.insert_one(norm)
    except Exception as e:
        log.error(f"Failed to record telemetry event: {e}")
        
    return event

def record_hindsight_placeholder(state: dict, response: dict, telemetry_event: dict) -> dict:
    placeholder = build_hindsight_placeholder(state, telemetry_event)
    
    if not settings.ENABLE_HINDSIGHT_LOGGING:
        return placeholder
        
    if settings.ENABLE_ASYNC_TELEMETRY:
        return placeholder
        
    save_hindsight_log(placeholder)
    return placeholder
