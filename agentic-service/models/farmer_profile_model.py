from typing import Dict, Any

def normalize_farmer_profile(profile: dict) -> dict:
    if not isinstance(profile, dict):
        return {}
        
    normalized = {}
    
    if profile.get("farmer_id"):
        normalized["farmer_id"] = str(profile.get("farmer_id"))
    
    if profile.get("name"):
        normalized["name"] = str(profile.get("name"))
        
    if profile.get("location"):
        normalized["location"] = str(profile.get("location"))
        
    if profile.get("language"):
        normalized["language"] = str(profile.get("language"))
        
    if profile.get("soil_type"):
        normalized["soil_type"] = str(profile.get("soil_type"))
        
    if "irrigation_available" in profile and profile["irrigation_available"] is True:
        normalized["irrigation_available"] = True
        
    if profile.get("crops_grown") and isinstance(profile["crops_grown"], list):
        normalized["crops_grown"] = [str(c) for c in profile["crops_grown"]]
        
    if profile.get("preferred_market"):
        normalized["preferred_market"] = str(profile.get("preferred_market"))
        
    if profile.get("last_updated"):
        normalized["last_updated"] = str(profile.get("last_updated"))
        
    return normalized

def validate_farmer_profile(profile: dict) -> bool:
    if not isinstance(profile, dict):
        return False
    if not profile.get("farmer_id"):
        return False
    return True
