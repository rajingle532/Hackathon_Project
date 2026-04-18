import logging
import requests
from hindsight.hindsight_config import hindsight_config

log = logging.getLogger("hindsight_client")

def _get_headers() -> dict:
    headers = {"Content-Type": "application/json"}
    if hindsight_config.api_key:
        headers["Authorization"] = f"Bearer {hindsight_config.api_key}"
    if hindsight_config.project_id:
        headers["X-Project-Id"] = hindsight_config.project_id
    return headers

def create_hindsight_log(payload: dict) -> dict:
    """Send a hindsight log to the external API."""
    if not hindsight_config.base_url:
        log.warning("Hindsight API Base URL is missing. Cannot create log.")
        return {"status": "fallback", "message": "unconfigured"}
        
    url = f"{hindsight_config.base_url.rstrip('/')}/logs"
    
    try:
        response = requests.post(
            url, 
            json=payload, 
            headers=_get_headers(), 
            timeout=hindsight_config.timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to create external hindsight log: {e}")
        return {"status": "error", "message": str(e)}

def get_hindsight_logs(interaction_id: str) -> list[dict]:
    """Retrieve hindsight logs for a specific interaction from external API."""
    if not hindsight_config.base_url:
        log.warning("Hindsight API Base URL is missing. Cannot fetch logs.")
        return []
        
    url = f"{hindsight_config.base_url.rstrip('/')}/logs/{interaction_id}"
    
    try:
        response = requests.get(
            url, 
            headers=_get_headers(), 
            timeout=hindsight_config.timeout
        )
        response.raise_for_status()
        data = response.json()
        
        # Depending on API response, could be a list or a dict containing a list
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("logs", [])
        return []
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to fetch external hindsight logs: {e}")
        return []

def check_hindsight_connection() -> bool:
    """Check connectivity to the external hindsight provider."""
    if not hindsight_config.base_url:
        return False
        
    url = f"{hindsight_config.base_url.rstrip('/')}/health"
    try:
        response = requests.get(
            url, 
            headers=_get_headers(), 
            timeout=hindsight_config.timeout
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
