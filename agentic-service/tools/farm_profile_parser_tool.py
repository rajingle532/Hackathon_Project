from utils.recommendation_keywords import SOIL_KEYWORDS, SEASON_KEYWORDS, RAINFALL_KEYWORDS, IRRIGATION_KEYWORDS
from config import settings

def extract_soil_type(message: str) -> str:
    msg_lower = message.lower()
    for kw, val in SOIL_KEYWORDS.items():
        if kw in msg_lower:
            return val
    return settings.DEFAULT_SOIL_TYPE

def extract_season(message: str) -> str:
    msg_lower = message.lower()
    for kw, val in SEASON_KEYWORDS.items():
        if kw in msg_lower:
            return val
    return settings.DEFAULT_SEASON

def extract_rainfall_level(message: str) -> str:
    msg_lower = message.lower()
    for kw, val in RAINFALL_KEYWORDS.items():
        if kw in msg_lower:
            return val
    return "medium"

def extract_irrigation_availability(message: str) -> bool:
    msg_lower = message.lower()
    for kw in IRRIGATION_KEYWORDS:
        if kw in msg_lower:
            return True
    return False

def extract_location(message: str) -> str:
    msg_lower = message.lower()
    cities_or_states = ["punjab", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata", "haryana", "up", "mp", "gujarat"]
    for loc in cities_or_states:
        if loc in msg_lower:
            return loc.capitalize()
    return settings.DEFAULT_LOCATION

def build_farm_profile(message: str) -> dict:
    return {
        "soil_type": extract_soil_type(message),
        "season": extract_season(message),
        "location": extract_location(message),
        "rainfall_level": extract_rainfall_level(message),
        "irrigation_available": extract_irrigation_availability(message)
    }
