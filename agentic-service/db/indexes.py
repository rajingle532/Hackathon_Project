import logging
from db.collections import (
    get_farmer_profile_collection,
    get_conversation_collection,
    get_agent_interaction_collection
)
from pymongo import ASCENDING, DESCENDING

log = logging.getLogger("mongo_indexes")

def ensure_indexes():
    try:
        # Farmer Profiles
        profile_col = get_farmer_profile_collection()
        if profile_col is not None:
            profile_col.create_index([("farmer_id", ASCENDING)], unique=True)
            
        # Conversation Messages
        conv_col = get_conversation_collection()
        if conv_col is not None:
            conv_col.create_index([("farmer_id", ASCENDING), ("timestamp", DESCENDING)])
            
        # Agent Interactions
        agent_col = get_agent_interaction_collection()
        if agent_col is not None:
            agent_col.create_index([("farmer_id", ASCENDING), ("timestamp", DESCENDING)])
            agent_col.create_index([("intent", ASCENDING)])
            
        log.info("MongoDB indexes ensured successfully")
    except Exception as e:
        log.error(f"Failed to ensure MongoDB indexes: {e}")
