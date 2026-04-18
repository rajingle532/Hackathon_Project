import logging
from db.mongo import get_database
from models.feedback_model import normalize_feedback, validate_feedback
from config import settings

log = logging.getLogger("feedback_store")

def get_feedback_collection():
    db = get_database()
    if db is not None:
        return db[settings.FEEDBACK_COLLECTION]
    return None

def save_feedback(feedback: dict) -> bool:
    try:
        col = get_feedback_collection()
        if col is None:
            return False
            
        norm = normalize_feedback(feedback)
        if validate_feedback(norm):
            col.insert_one(norm)
            return True
        return False
    except Exception as e:
        log.error(f"Error saving feedback: {e}")
        return False

def get_feedback_by_interaction(interaction_id: str) -> list[dict]:
    try:
        col = get_feedback_collection()
        if col is None:
            return []
            
        cursor = col.find({"interaction_id": interaction_id})
        docs = list(cursor)
        for doc in docs:
            doc.pop("_id", None)
        return docs
    except Exception as e:
        log.error(f"Error fetching feedback: {e}")
        return []
