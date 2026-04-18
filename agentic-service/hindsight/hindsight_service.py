import logging
from hindsight.hindsight_client import create_hindsight_log, get_hindsight_logs
from hindsight.hindsight_mapper import map_internal_hindsight_to_provider, map_provider_hindsight_to_internal
from hindsight.hindsight_retry import execute_with_retry
from hindsight.hindsight_config import hindsight_config

log = logging.getLogger("hindsight_external_service")

def save_hindsight(payload: dict) -> bool:
    """
    Save hindsight log to external provider.
    Returns True on success, False on failure.
    """
    if not hindsight_config.enabled:
        log.info("External hindsight logging is disabled.")
        return False
        
    try:
        mapped_payload = map_internal_hindsight_to_provider(payload)
        
        def _call_client():
            return create_hindsight_log(mapped_payload)
            
        result = execute_with_retry(_call_client)
        
        if result and result.get("status") not in ["error", "fallback"]:
            return True
        return False
    except Exception as e:
        log.error(f"Error in save_hindsight: {e}")
        return False

def fetch_hindsight(interaction_id: str) -> list[dict]:
    """
    Fetch hindsight logs from external provider and map back to internal schema.
    """
    if not hindsight_config.enabled:
        return []
        
    try:
        def _call_client():
            return get_hindsight_logs(interaction_id)
            
        external_logs = execute_with_retry(_call_client)
        
        if not external_logs:
            return []
            
        return [map_provider_hindsight_to_internal(log) for log in external_logs]
    except Exception as e:
        log.error(f"Error in fetch_hindsight: {e}")
        return []
