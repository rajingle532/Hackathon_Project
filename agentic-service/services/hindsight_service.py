from telemetry.hindsight_store import save_hindsight_log, get_hindsight_by_interaction
from config import settings

log = logging.getLogger("hindsight_service")

def submit_hindsight_log(hindsight_payload: dict) -> bool:
    try:
        if settings.ENABLE_ASYNC_TELEMETRY:
            return True
        return save_hindsight_log(hindsight_payload)
    except Exception as e:
        log.error(f"Failed to submit hindsight log: {e}")
        return False

def get_hindsight_summary(interaction_id: str) -> dict:
    logs = get_hindsight_by_interaction(interaction_id)
    if not logs:
        return {"total_logs": 0}
        
    return {
        "total_logs": len(logs),
        "logs": logs
    }
