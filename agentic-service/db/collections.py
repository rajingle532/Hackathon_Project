from db.mongo import get_database
from config import settings

def get_farmer_profile_collection():
    db = get_database()
    if db is not None:
        return db[settings.FARMER_PROFILE_COLLECTION]
    return None

def get_conversation_collection():
    db = get_database()
    if db is not None:
        return db[settings.CONVERSATION_COLLECTION]
    return None

def get_agent_interaction_collection():
    db = get_database()
    if db is not None:
        return db[settings.AGENT_INTERACTION_COLLECTION]
    return None
