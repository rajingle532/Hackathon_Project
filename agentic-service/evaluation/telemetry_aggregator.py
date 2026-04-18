from db.mongo import get_database
from config import settings
import logging

log = logging.getLogger("telemetry_aggregator")

def _collect_recent(collection_name: str, limit: int = 100) -> list[dict]:
    try:
        db = get_database()
        if db is not None:
            col = db[collection_name]
            cursor = col.find().sort("_id", -1).limit(limit)
            docs = list(cursor)
            for doc in docs:
                doc.pop("_id", None)
            return docs
        return []
    except Exception as e:
        log.error(f"Error fetching from {collection_name}: {e}")
        return []

def collect_recent_telemetry(limit: int = 100) -> list[dict]:
    return _collect_recent(settings.TELEMETRY_COLLECTION, limit)

def collect_recent_feedback(limit: int = 100) -> list[dict]:
    return _collect_recent(settings.FEEDBACK_COLLECTION, limit)

def collect_recent_hindsight(limit: int = 100) -> list[dict]:
    return _collect_recent(settings.HINDSIGHT_COLLECTION, limit)
