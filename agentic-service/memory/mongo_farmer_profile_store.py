import logging
import datetime
from db.collections import get_farmer_profile_collection
from models.farmer_profile_model import normalize_farmer_profile, validate_farmer_profile
from memory.farmer_profile_store import merge_farmer_profile

log = logging.getLogger("mongo_farmer_profile_store")

def get_farmer_profile_from_mongo(farmer_id: str) -> dict:
    try:
        col = get_farmer_profile_collection()
        if col is None:
            return None
            
        doc = col.find_one({"farmer_id": farmer_id})
        if doc:
            # remove _id to keep it clean
            doc.pop("_id", None)
            return doc
        return None
    except Exception as e:
        log.error(f"Error fetching farmer profile from Mongo: {e}")
        return None

def upsert_farmer_profile(farmer_id: str, profile: dict) -> dict:
    try:
        col = get_farmer_profile_collection()
        if col is None:
            return profile
            
        norm_profile = normalize_farmer_profile(profile)
        norm_profile["farmer_id"] = farmer_id
        if not validate_farmer_profile(norm_profile):
            return profile
            
        col.update_one(
            {"farmer_id": farmer_id},
            {"$set": norm_profile},
            upsert=True
        )
        return norm_profile
    except Exception as e:
        log.error(f"Error upserting farmer profile to Mongo: {e}")
        return profile

def update_farmer_profile_in_mongo(farmer_id: str, updates: dict) -> dict:
    existing = get_farmer_profile_from_mongo(farmer_id) or {"farmer_id": farmer_id}
    merged = merge_farmer_profile(existing, updates)
    return upsert_farmer_profile(farmer_id, merged)
