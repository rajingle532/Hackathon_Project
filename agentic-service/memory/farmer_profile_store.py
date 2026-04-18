from typing import Dict, Any
import datetime

# Mock database for simplicity. In reality, this connects to MongoDB.
_MOCK_PROFILES = {}

def get_farmer_profile(farmer_id: str) -> dict:
    return _MOCK_PROFILES.get(farmer_id, {"farmer_id": farmer_id})

def update_farmer_profile(farmer_id: str, updates: dict) -> dict:
    existing = get_farmer_profile(farmer_id)
    merged = merge_farmer_profile(existing, updates)
    _MOCK_PROFILES[farmer_id] = merged
    return merged

def merge_farmer_profile(existing: dict, incoming: dict) -> dict:
    merged = existing.copy()
    for k, v in incoming.items():
        if v: # Only merge if not empty
            if isinstance(v, list):
                # Unique append for lists
                existing_list = merged.get(k, [])
                merged[k] = list(set(existing_list + v))
            else:
                merged[k] = v
    merged["last_updated"] = datetime.datetime.now().isoformat()
    return merged
