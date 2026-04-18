import logging

log = logging.getLogger("rag_evaluator")

def evaluate_rag_quality(retrieved_context: str, expected_keywords: list[str]) -> dict:
    if not retrieved_context or not expected_keywords:
        return {
            "rag_score": 0.0,
            "matched_keywords": [],
            "missing_keywords": expected_keywords
        }
        
    context_lower = retrieved_context.lower()
    matched = []
    missing = []
    
    for kw in expected_keywords:
        if kw.lower() in context_lower:
            matched.append(kw)
        else:
            missing.append(kw)
            
    rag_score = len(matched) / len(expected_keywords) if expected_keywords else 0.0
    
    return {
        "rag_score": rag_score,
        "matched_keywords": matched,
        "missing_keywords": missing
    }
