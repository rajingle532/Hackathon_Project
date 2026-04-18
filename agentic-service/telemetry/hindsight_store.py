import logging
from models.hindsight_model import normalize_hindsight_log, validate_hindsight_log
from hindsight.hindsight_service import save_hindsight, fetch_hindsight

log = logging.getLogger("hindsight_store")

def save_hindsight_log(log_data: dict) -> bool:
    try:
        norm = normalize_hindsight_log(log_data)
        if validate_hindsight_log(norm):
            return save_hindsight(norm)
        return False
    except Exception as e:
        log.error(f"Error saving hindsight log to external service: {e}")
        return False

def get_hindsight_by_interaction(interaction_id: str) -> list[dict]:
    try:
        return fetch_hindsight(interaction_id)
    except Exception as e:
        log.error(f"Error fetching hindsight logs from external service: {e}")
        return []
