import requests
from config import settings
from utils.logger import setup_logger
from utils.disease_fallbacks import DISEASE_API_FALLBACK
from tools.symptom_parser_tool import detect_possible_disease
from utils.disease_constants import DEFAULT_DISEASE

log = setup_logger("disease_api_service")

def predict_crop_disease(image_path: str = None, symptoms: list[str] = None) -> dict:
    """Predict crop disease via external ML API or fallback to symptom heuristics."""
    
    # 1. Fallback heuristic if no image is provided
    if not image_path or not settings.ENABLE_DISEASE_IMAGE_SUPPORT:
        if symptoms:
            heuristic_disease = detect_possible_disease(symptoms)
            confidence = 0.50 if heuristic_disease != DEFAULT_DISEASE else 0.0
            return {
                "success": True,
                "disease_name": heuristic_disease.replace("_", " ").title(),
                "confidence": confidence,
                "treatment": "Follow general guidelines for this condition.",
                "raw_response": {"source": "heuristic"}
            }
        else:
            return {
                "success": False,
                "disease_name": DEFAULT_DISEASE,
                "confidence": 0.0,
                "treatment": DISEASE_API_FALLBACK,
                "raw_response": {}
            }
            
    # 2. Call external ML API (Placeholder for actual requests.post)
    try:
        # Currently we just mock the request as instructed, but setup structure
        # response = requests.post(settings.DISEASE_API_URL, files={"file": open(image_path, "rb")}, timeout=settings.ML_TIMEOUT)
        # response.raise_for_status()
        # data = response.json()
        data = {"disease": "Mock Disease API Output", "confidence": 0.85, "treatment": "Mock treatment"}
        
        return {
            "success": True,
            "disease_name": data.get("disease", DEFAULT_DISEASE),
            "confidence": data.get("confidence", 0.0),
            "treatment": data.get("treatment", ""),
            "raw_response": data
        }
    except Exception as e:
        log.error(f"Disease API call failed: {e}")
        return {
            "success": False,
            "disease_name": DEFAULT_DISEASE,
            "confidence": 0.0,
            "treatment": DISEASE_API_FALLBACK,
            "raw_response": {"error": str(e)}
        }
