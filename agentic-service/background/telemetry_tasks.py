import logging
import time
from models.telemetry_event_model import normalize_telemetry_event, validate_telemetry_event
from db.mongo import get_database
from telemetry.feedback_store import save_feedback
from telemetry.hindsight_store import save_hindsight_log
from config import settings

log = logging.getLogger("telemetry_tasks")

def _retry_wrapper(func, *args, **kwargs):
    retries = 0
    max_retries = settings.MAX_BACKGROUND_RETRIES
    while retries < max_retries:
        try:
            success = func(*args, **kwargs)
            if success: return True
        except Exception as e:
            log.warning(f"Telemetry task failed (attempt {retries + 1}/{max_retries}): {e}")
            
        retries += 1
        time.sleep(1)
    log.error(f"Telemetry task failed permanently after {max_retries} retries")
    return False

def _save_telemetry_event(event: dict) -> bool:
    try:
        db = get_database()
        if db is not None:
            col = db[settings.TELEMETRY_COLLECTION]
            norm = normalize_telemetry_event(event)
            if validate_telemetry_event(norm):
                col.insert_one(norm)
                return True
        return False
    except Exception as e:
        log.error(f"Error saving telemetry: {e}")
        return False

def record_telemetry_task(event: dict) -> None:
    _retry_wrapper(_save_telemetry_event, event)

def record_hindsight_task(placeholder: dict) -> None:
    # Hindsight service implements its own retry logic for external APIs
    save_hindsight_log(placeholder)

def save_feedback_task(feedback_payload: dict) -> None:
    _retry_wrapper(save_feedback, feedback_payload)

def save_hindsight_log_task(hindsight_payload: dict) -> None:
    # Hindsight service implements its own retry logic for external APIs
    save_hindsight_log(hindsight_payload)
