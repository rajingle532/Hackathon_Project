import uuid
from telemetry.scoring_service import calculate_response_score, classify_response_quality, calculate_rag_score
from config import settings

def build_telemetry_event(state: dict, response: dict) -> dict:
    interaction_id = str(uuid.uuid4())
    
    metadata = state.get("metadata", {})
    confidence = metadata.get("agent_confidence", 0.0)
    if confidence == 0.0:
        confidence = response.get("metadata", {}).get("disease_confidence", 0.0)
        if confidence == 0.0:
             confidence = response.get("metadata", {}).get("recommendation_confidence", 0.0)
        if confidence == 0.0:
             confidence = response.get("metadata", {}).get("market_confidence", 0.0)
             
    is_fallback = state.get("is_fallback", False) or response.get("is_fallback", False)
    tools_used = state.get("tools_used", []) or response.get("tools_used", [])
    requires_escalation = metadata.get("requires_escalation", False)
    
    score = calculate_response_score(confidence, is_fallback, tools_used, requires_escalation)
    quality = classify_response_quality(score)
    
    low_quality = score < settings.MIN_ACCEPTABLE_RESPONSE_SCORE
    
    rag_score = 0.0
    context_used = state.get("context_used", {}) or response.get("context_used", {})
    if context_used:
        # Provide an empty list for expected keywords as a baseline.
        rag_score = calculate_rag_score(str(context_used), [])
        
    return {
        "interaction_id": interaction_id,
        "farmer_id": state.get("farmer_id", "anonymous"),
        "intent": state.get("intent", "unknown"),
        "agent_used": state.get("agent_used", "none"),
        "confidence": confidence,
        "is_fallback": is_fallback,
        "response_score": score,
        "response_quality": quality,
        "low_quality": low_quality,
        "rag_score": rag_score
    }

def build_hindsight_placeholder(state: dict, telemetry_event: dict) -> dict:
    return {
        "interaction_id": telemetry_event.get("interaction_id"),
        "farmer_id": telemetry_event.get("farmer_id", "anonymous"),
        "intent": telemetry_event.get("intent", "unknown"),
        "agent_used": telemetry_event.get("agent_used", "none"),
        "original_prediction": "N/A", # Optional details
        "outcome_status": "pending",
        "outcome_reason": "Waiting for observation"
    }
