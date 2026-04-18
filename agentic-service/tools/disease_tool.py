from utils.disease_keywords import DISEASE_KEYWORDS
from tools.symptom_parser_tool import extract_symptoms
from services.disease_api_service import predict_crop_disease
from utils.disease_constants import ESCALATION_THRESHOLD

def disease_needed(message: str) -> bool:
    """Check if the message contains disease-related keywords."""
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in DISEASE_KEYWORDS)

def get_disease_context(message: str, image_path: str = None) -> dict:
    """Gather full disease context using symptoms and API."""
    symptoms = extract_symptoms(message)
    
    prediction = predict_crop_disease(image_path=image_path, symptoms=symptoms)
    
    confidence = prediction.get("confidence", 0.0)
    requires_escalation = confidence < ESCALATION_THRESHOLD and confidence > 0.0
    
    return {
        "disease_name": prediction.get("disease_name"),
        "confidence": confidence,
        "symptoms_detected": symptoms,
        "treatment": prediction.get("treatment", ""),
        "requires_escalation": requires_escalation
    }
