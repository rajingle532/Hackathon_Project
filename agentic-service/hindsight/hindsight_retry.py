import time
import logging
from hindsight.hindsight_config import hindsight_config

log = logging.getLogger("hindsight_retry")

def execute_with_retry(task_callable, *args, **kwargs):
    """
    Execute a callable with exponential backoff retries.
    Returns the successful result, or None if all retries fail.
    """
    max_retries = hindsight_config.max_retries
    retries = 0
    
    while retries < max_retries:
        try:
            result = task_callable(*args, **kwargs)
            # If the client returns an explicit error status, we might decide not to retry depending on logic,
            # but for now, any exception triggers retry.
            return result
        except Exception as e:
            log.warning(f"Hindsight task failed (attempt {retries + 1}/{max_retries}): {e}")
            retries += 1
            if retries < max_retries:
                # Exponential backoff
                time.sleep(2 ** retries)
                
    log.error(f"Hindsight task failed permanently after {max_retries} retries")
    return None
