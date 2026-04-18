import requests
from config import settings
from utils.logger import setup_logger
from utils.market_constants import FALLBACK_PRICE_TREND, FALLBACK_SELLING_ADVICE

log = setup_logger("market_api_service")

def get_market_price(market_profile: dict) -> dict:
    """Get market price from external API or fallback."""
    
    if not settings.ENABLE_MARKET_FALLBACK:
        pass
        
    try:
        # Mock actual external ML api
        # response = requests.get(settings.MARKET_API_URL, params=market_profile, timeout=settings.ML_TIMEOUT)
        # data = response.json()
        
        commodity = market_profile.get("commodity_name", settings.DEFAULT_MARKET_CROP)
        location = market_profile.get("market_location", settings.DEFAULT_MARKET_LOCATION)
        
        # Mock responses based on crop
        if commodity == "Wheat":
            price = "₹2450/quintal"
            trend = "rising"
            advice = "Prices are improving. Waiting 1-2 weeks may provide better returns."
            confidence = 0.81
        elif commodity == "Rice":
            price = "₹2800/quintal"
            trend = "falling"
            advice = "Selling soon may reduce risk if prices continue falling."
            confidence = 0.75
        elif commodity == "Tomato":
            price = "₹1500/quintal"
            trend = "volatile"
            advice = "Tomatoes are highly perishable. Sell immediately unless you have cold storage."
            confidence = 0.90
        else:
            price = "₹2000/quintal"
            trend = "stable"
            advice = "Prices are stable. You may sell now or hold if you have proper storage."
            confidence = 0.65
            
        return {
            "success": True,
            "commodity_name": commodity,
            "market_location": location,
            "market_price": price,
            "price_trend": trend,
            "confidence": confidence,
            "selling_advice": advice,
            "raw_response": {"mock": True}
        }
    except Exception as e:
        log.error(f"Market API call failed: {e}")
        return {
            "success": False,
            "commodity_name": market_profile.get("commodity_name", settings.DEFAULT_MARKET_CROP),
            "market_location": market_profile.get("market_location", settings.DEFAULT_MARKET_LOCATION),
            "market_price": "Unknown",
            "price_trend": FALLBACK_PRICE_TREND,
            "confidence": 0.40,
            "selling_advice": FALLBACK_SELLING_ADVICE,
            "raw_response": {"error": str(e)}
        }
