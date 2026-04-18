import requests
from utils.logger import setup_logger

log = setup_logger("external_api_service")

def make_get_request(url: str, params: dict = None, timeout: int = 10) -> dict:
    """Make an HTTP GET request with error handling."""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        log.error(f"Timeout while requesting {url}")
        return {"success": False, "error": "API timeout"}
    except requests.exceptions.RequestException as e:
        log.error(f"Request failed for {url}: {e}")
        return {"success": False, "error": str(e)}
    except ValueError as e:
        log.error(f"JSON parse failed for {url}: {e}")
        return {"success": False, "error": "Invalid JSON response"}
