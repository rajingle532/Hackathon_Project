from utils.market_keywords import CROP_ALIASES, MARKET_KEYWORDS
from config import settings

def extract_commodity(message: str) -> str:
    msg_lower = message.lower()
    for kw, val in CROP_ALIASES.items():
        if kw in msg_lower:
            return val
    return settings.DEFAULT_MARKET_CROP

def extract_market_location(message: str) -> str:
    msg_lower = message.lower()
    cities_or_states = ["punjab", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata", "haryana", "up", "mp", "gujarat"]
    for loc in cities_or_states:
        if loc in msg_lower:
            return loc.capitalize()
    return settings.DEFAULT_MARKET_LOCATION

def detect_selling_intent(message: str) -> bool:
    msg_lower = message.lower()
    selling_words = ["sell", "selling", "rate", "price", "profit", "mandi"]
    return any(w in msg_lower for w in selling_words)

def build_market_profile(message: str) -> dict:
    return {
        "commodity_name": extract_commodity(message),
        "market_location": extract_market_location(message),
        "selling_intent": detect_selling_intent(message)
    }
