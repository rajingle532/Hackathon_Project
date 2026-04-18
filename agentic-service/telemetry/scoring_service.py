from config import settings

def calculate_response_score(
    confidence: float,
    is_fallback: bool,
    tools_used: list[str],
    requires_escalation: bool
) -> float:
    
    score = settings.DEFAULT_RESPONSE_SCORE
    
    if confidence > 0:
        # Heavily weight the score based on confidence
        score = confidence
        
    if is_fallback:
        score -= 0.4
        
    if requires_escalation:
        score -= 0.2
        
    # Reward for using tools
    if len(tools_used) > 1:
        score += 0.05 * len(tools_used)
        
    # Clamp score
    return max(0.0, min(1.0, score))

def classify_response_quality(score: float) -> str:
    if score >= 0.8:
        return "high"
    elif score >= settings.LOW_CONFIDENCE_SCORE_THRESHOLD:
        return "medium"
    else:
        return "low"

def calculate_rag_score(retrieved_context: str, expected_keywords: list[str]) -> float:
    if not retrieved_context or not expected_keywords:
        return 0.0
    context_lower = retrieved_context.lower()
    matched = sum(1 for kw in expected_keywords if kw.lower() in context_lower)
    return matched / len(expected_keywords)
