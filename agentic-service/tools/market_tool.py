from utils.market_keywords import MARKET_KEYWORDS
from tools.commodity_parser_tool import build_market_profile
from services.market_api_service import get_market_price

def market_needed(message: str) -> bool:
    """Check if the message contains market-related keywords."""
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in MARKET_KEYWORDS)

def get_market_context(message: str) -> dict:
    """Gather full market context using parser and API."""
    profile = build_market_profile(message)
    prediction = get_market_price(profile)
    
    return {
        "commodity_name": prediction.get("commodity_name", profile.get("commodity_name")),
        "market_location": prediction.get("market_location", profile.get("market_location")),
        "market_price": prediction.get("market_price", "Unknown"),
        "price_trend": prediction.get("price_trend", "unknown"),
        "confidence": prediction.get("confidence", 0.0),
        "selling_advice": prediction.get("selling_advice", ""),
        "market_profile": profile
    }
