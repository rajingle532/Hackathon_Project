import logging
import time
from memory.mongo_memory_service import persist_mongo_memory_context
from memory.mongo_conversation_store import save_message_to_mongo, save_agent_interaction_to_mongo
from config import settings

log = logging.getLogger("persistence_tasks")

def _retry_wrapper(func, *args, **kwargs):
    retries = 0
    max_retries = settings.MAX_BACKGROUND_RETRIES
    while retries < max_retries:
        try:
            success = func(*args, **kwargs)
            if success: return True
        except Exception as e:
            log.warning(f"Task failed (attempt {retries + 1}/{max_retries}): {e}")
        
        retries += 1
        time.sleep(1) # simple backoff
    log.error(f"Task failed permanently after {max_retries} retries")
    return False

def persist_memory_context_task(farmer_id: str, state: dict, response: dict) -> None:
    _retry_wrapper(persist_mongo_memory_context, farmer_id, state, response)

def save_conversation_task(message_payload: dict) -> None:
    _retry_wrapper(save_message_to_mongo, message_payload)

def save_agent_interaction_task(interaction_payload: dict) -> None:
    _retry_wrapper(save_agent_interaction_to_mongo, interaction_payload)
