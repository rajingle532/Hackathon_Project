import requests
from config import settings
from utils.logger import setup_logger
from utils.recommendation_constants import FALLBACK_CROPS, FALLBACK_REASONING

log = setup_logger("recommendation_api_service")

def predict_recommended_crops(farm_profile: dict) -> dict:
    """Predict crops via external ML API or fallback if incomplete."""
    
    # 1. Fallback if ML API is not strictly available or if we are skipping it (mocked)
    if not settings.ENABLE_RECOMMENDATION_FALLBACK:
        # Simulate an API call failure
        pass

    try:
        # Mock actual external ML api
        # response = requests.post(settings.RECOMMENDATION_API_URL, json=farm_profile, timeout=settings.ML_TIMEOUT)
        # data = response.json()
        
        # We will mock the response matching the requested instructions
        soil = farm_profile.get("soil_type", settings.DEFAULT_SOIL_TYPE)
        season = farm_profile.get("season", settings.DEFAULT_SEASON)
        
        crops = []
        reasoning = []
        
        if soil == "loamy" and season == "kharif":
            crops = ["Rice", "Soybean"]
            reasoning = ["Rice is suitable for loamy soil and kharif season.", "Soybean improves soil fertility."]
        elif soil == "black" and season == "kharif":
            crops = ["Cotton"]
            reasoning = ["Cotton grows extremely well in black soil."]
        elif season == "rabi":
            crops = ["Wheat"]
            reasoning = ["Wheat is the primary rabi crop and suitable for cooler climates."]
        else:
            crops = ["Pulses", "Vegetables"]
            reasoning = ["These crops are versatile and can grow in various conditions."]
            
        return {
            "success": True,
            "recommended_crops": crops,
            "confidence": 0.85,
            "reasoning": reasoning,
            "raw_response": {"mock": True}
        }
    except Exception as e:
        log.error(f"Recommendation API call failed: {e}")
        return {
            "success": True,
            "recommended_crops": FALLBACK_CROPS,
            "confidence": 0.40,
            "reasoning": FALLBACK_REASONING,
            "raw_response": {"error": str(e)}
        }
