from utils.disease_keywords import SYMPTOM_TO_DISEASE_MAP
from utils.disease_constants import DEFAULT_DISEASE

def extract_symptoms(message: str) -> list[str]:
    """Extract symptoms from a free text message based on keywords."""
    message_lower = message.lower()
    symptoms = []
    
    for symptom in SYMPTOM_TO_DISEASE_MAP.keys():
        if symptom in message_lower:
            symptoms.append(symptom)
            
    return symptoms

def detect_possible_disease(symptoms: list[str]) -> str:
    """Map the first found symptom to a possible disease category."""
    if not symptoms:
        return DEFAULT_DISEASE
        
    for symptom in symptoms:
        if symptom in SYMPTOM_TO_DISEASE_MAP:
            return SYMPTOM_TO_DISEASE_MAP[symptom]
            
    return DEFAULT_DISEASE
