from memory.farmer_profile_store import get_farmer_profile, update_farmer_profile
from memory.conversation_store import get_recent_conversation_history, save_conversation_message, save_agent_interaction
from memory.mongo_memory_service import load_mongo_memory_context, persist_mongo_memory_context
from config import settings
from services.farmer_profile_service import (
    extract_location, extract_language, extract_soil_type,
    extract_crops_grown, extract_irrigation_availability
)

def load_memory_context(farmer_id: str) -> dict:
    if not farmer_id:
        return {"profile": {}, "history": [], "mongo_connected": False, "memory_source": "none"}
        
    if settings.ENABLE_MONGO_MEMORY:
        mongo_ctx = load_mongo_memory_context(farmer_id)
        if mongo_ctx is not None:
            mongo_ctx["memory_source"] = "mongo"
            return mongo_ctx
            
    profile = get_farmer_profile(farmer_id)
    history = get_recent_conversation_history(farmer_id)
    
    return {
        "profile": profile,
        "history": history,
        "mongo_connected": False,
        "memory_source": "mock"
    }

def enrich_profile_from_message(message: str, existing_profile: dict) -> dict:
    updates = {}
    
    loc = extract_location(message)
    if loc: updates["location"] = loc
        
    lang = extract_language(message)
    if lang: updates["language"] = lang
        
    soil = extract_soil_type(message)
    if soil: updates["soil_type"] = soil
        
    crops = extract_crops_grown(message)
    if crops: updates["crops_grown"] = crops
        
    irrigation = extract_irrigation_availability(message)
    if irrigation: updates["irrigation_available"] = irrigation
        
    return updates

def save_interaction_context(farmer_id: str, state: dict, response: dict) -> bool:
    if not farmer_id:
        return False
        
    if settings.ENABLE_ASYNC_PERSISTENCE:
        return True
        
    if settings.ENABLE_MONGO_MEMORY:
        success = persist_mongo_memory_context(farmer_id, state, response)
        if success:
            return True
            
    # Assume the last message in state is the user message
    messages = state.get("messages", [])
    if messages:
        last_msg = messages[-1]
        content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
        save_conversation_message(farmer_id, "user", content)
        
        # Enrich profile
        profile = get_farmer_profile(farmer_id)
        updates = enrich_profile_from_message(content, profile)
        
        # Also include any metadata the agent discovered (like soil type, location)
        metadata = response.get("metadata", {})
        if metadata.get("soil_type"): updates["soil_type"] = metadata["soil_type"]
        if metadata.get("location"): updates["location"] = metadata["location"]
        if metadata.get("recommended_crops"): updates["crops_grown"] = metadata["recommended_crops"]
        
        if updates:
            update_farmer_profile(farmer_id, updates)
            
    save_agent_interaction(farmer_id, response.get("intent", "unknown"), response)
    return True
