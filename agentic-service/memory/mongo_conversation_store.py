import logging
import pymongo
from db.collections import get_conversation_collection, get_agent_interaction_collection
from models.conversation_message_model import normalize_conversation_message, validate_conversation_message
from models.agent_interaction_model import normalize_agent_interaction, validate_agent_interaction

log = logging.getLogger("mongo_conversation_store")

def get_recent_history_from_mongo(farmer_id: str, limit: int = 10) -> list[dict]:
    try:
        col = get_conversation_collection()
        if col is None:
            return None
            
        cursor = col.find({"farmer_id": farmer_id}).sort("timestamp", pymongo.DESCENDING).limit(limit)
        docs = list(cursor)
        
        # We stored descending to get recent ones, now reverse to chronological
        docs.reverse()
        for doc in docs:
            doc.pop("_id", None)
            
        return docs
    except Exception as e:
        log.error(f"Error fetching history from Mongo: {e}")
        return None

def save_message_to_mongo(message: dict) -> bool:
    try:
        col = get_conversation_collection()
        if col is None:
            return False
            
        norm_msg = normalize_conversation_message(message)
        if validate_conversation_message(norm_msg):
            col.insert_one(norm_msg)
            return True
        return False
    except Exception as e:
        log.error(f"Error saving message to Mongo: {e}")
        return False

def save_agent_interaction_to_mongo(interaction: dict) -> bool:
    try:
        # Also save interaction to conversation stream for unified history
        col_conv = get_conversation_collection()
        if col_conv is not None:
            norm_msg = normalize_conversation_message({
                "farmer_id": interaction.get("farmer_id"),
                "role": "system",
                "content": interaction.get("reply"),
                "intent": interaction.get("intent"),
                "metadata": interaction.get("metadata", {}),
                "timestamp": interaction.get("timestamp")
            })
            if validate_conversation_message(norm_msg):
                col_conv.insert_one(norm_msg)
                
        # Save detailed metadata in interactions collection
        col_agent = get_agent_interaction_collection()
        if col_agent is not None:
            norm_interaction = normalize_agent_interaction(interaction)
            if validate_agent_interaction(norm_interaction):
                col_agent.insert_one(norm_interaction)
                return True
        return False
    except Exception as e:
        log.error(f"Error saving agent interaction to Mongo: {e}")
        return False
