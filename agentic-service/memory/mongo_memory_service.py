import logging
import datetime
from memory.mongo_farmer_profile_store import get_farmer_profile_from_mongo, update_farmer_profile_in_mongo
from memory.mongo_conversation_store import get_recent_history_from_mongo, save_message_to_mongo, save_agent_interaction_to_mongo
from memory.memory_service import enrich_profile_from_message

log = logging.getLogger("mongo_memory_service")

def load_mongo_memory_context(farmer_id: str) -> dict:
    if not farmer_id:
        return {"profile": {}, "history": [], "mongo_connected": False}
        
    profile = get_farmer_profile_from_mongo(farmer_id)
    history = get_recent_history_from_mongo(farmer_id)
    
    if profile is None and history is None:
        # Mongo failed
        return None
        
    return {
        "profile": profile or {"farmer_id": farmer_id},
        "history": history or [],
        "mongo_connected": True
    }

def persist_mongo_memory_context(farmer_id: str, state: dict, response: dict) -> bool:
    if not farmer_id:
        return False
        
    if settings.ENABLE_ASYNC_PERSISTENCE:
        return True
        
    success = True
    messages = state.get("messages", [])
    if messages:
        last_msg = messages[-1]
        content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
        
        # Save user msg
        msg_success = save_message_to_mongo({
            "farmer_id": farmer_id,
            "role": "user",
            "content": content
        })
        if not msg_success: success = False
        
        # Enrich profile
        profile = get_farmer_profile_from_mongo(farmer_id) or {"farmer_id": farmer_id}
        updates = enrich_profile_from_message(content, profile)
        
        metadata = response.get("metadata", {})
        if metadata.get("soil_type"): updates["soil_type"] = metadata["soil_type"]
        if metadata.get("location"): updates["location"] = metadata["location"]
        if metadata.get("recommended_crops"): updates["crops_grown"] = metadata["recommended_crops"]
        
        if updates:
            update_farmer_profile_in_mongo(farmer_id, updates)
            
    interaction = {
        "farmer_id": farmer_id,
        "intent": response.get("intent", "unknown"),
        "agent_used": response.get("agent_used", "none"),
        "reply": response.get("reply", ""),
        "metadata": response.get("metadata", {}),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    int_success = save_agent_interaction_to_mongo(interaction)
    if not int_success: success = False
    
    return success
