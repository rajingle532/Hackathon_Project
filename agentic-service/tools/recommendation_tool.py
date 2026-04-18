from utils.recommendation_keywords import RECOMMENDATION_KEYWORDS
from tools.farm_profile_parser_tool import build_farm_profile
from services.recommendation_api_service import predict_recommended_crops

def recommendation_needed(message: str) -> bool:
    """Check if the message contains crop recommendation-related keywords."""
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in RECOMMENDATION_KEYWORDS)

def get_recommendation_context(message: str) -> dict:
    """Gather full recommendation context using farm profile and API."""
    profile = build_farm_profile(message)
    prediction = predict_recommended_crops(profile)
    
    return {
        "recommended_crops": prediction.get("recommended_crops", []),
        "confidence": prediction.get("confidence", 0.0),
        "reasoning": prediction.get("reasoning", []),
        "farm_profile": profile
    }
