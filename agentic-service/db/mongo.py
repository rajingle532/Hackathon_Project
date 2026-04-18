import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import settings

log = logging.getLogger("mongo")

_client = None

def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        try:
            _client = MongoClient(
                settings.MONGO_URI,
                serverSelectionTimeoutMS=settings.MONGO_TIMEOUT_MS
            )
            # Force a call to check if connected
            _client.admin.command('ping')
            log.info("Successfully connected to MongoDB")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            log.error(f"MongoDB connection failed: {e}")
            _client = None
    return _client

def get_database():
    client = get_mongo_client()
    if client:
        return client[settings.MONGO_DATABASE]
    return None

def check_mongo_connection() -> bool:
    try:
        client = get_mongo_client()
        if client:
            client.admin.command('ping')
            return True
        return False
    except Exception:
        return False
