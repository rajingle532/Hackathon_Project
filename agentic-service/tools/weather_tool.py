from config import settings
from utils.weather_keywords import WEATHER_KEYWORDS
from services.weather_service import get_current_weather

def weather_needed(message: str) -> bool:
    message_lower = message.lower()
    return any(kw in message_lower for kw in WEATHER_KEYWORDS)

def extract_location_from_message(message: str) -> str:
    """Extract potential location from message using heuristics."""
    # A simple heuristic: if words start with capital letter after 'in', 'for', 'at'
    # For now, just a dummy check for specific cities for the sake of the example.
    msg_lower = message.lower()
    
    cities = ["delhi", "punjab", "mumbai", "pune", "bangalore", "chennai", "kolkata"]
    for city in cities:
        if city in msg_lower:
            return city.capitalize()
            
    return settings.DEFAULT_LOCATION

def get_weather_context(message: str) -> dict:
    if not weather_needed(message):
        return {}
    
    location = extract_location_from_message(message)
    return get_current_weather(location)
