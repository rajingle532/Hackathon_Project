def extract_location(message: str) -> str:
    msg_lower = message.lower()
    locations = ["punjab", "haryana", "delhi", "maharashtra", "gujarat", "up", "mp", "karnataka", "tamil nadu", "kerala"]
    for loc in locations:
        if loc in msg_lower:
            return loc.title()
    return ""

def extract_language(message: str) -> str:
    msg_lower = message.lower()
    languages = ["hindi", "english", "punjabi", "marathi", "gujarati", "tamil", "telugu"]
    for lang in languages:
        if lang in msg_lower:
            return lang.title()
    return ""

def extract_soil_type(message: str) -> str:
    msg_lower = message.lower()
    soils = ["loamy", "clay", "sandy", "black", "red", "alluvial"]
    for soil in soils:
        if soil in msg_lower:
            return soil
    return ""

def extract_crops_grown(message: str) -> list[str]:
    msg_lower = message.lower()
    known_crops = ["wheat", "rice", "cotton", "soybean", "maize", "sugarcane", "tomato", "onion", "potato"]
    found = [crop.title() for crop in known_crops if crop in msg_lower]
    return found

def extract_irrigation_availability(message: str) -> bool:
    msg_lower = message.lower()
    if any(word in msg_lower for word in ["borewell", "tube well", "canal", "water supply", "irrigation"]):
        return True
    return False
