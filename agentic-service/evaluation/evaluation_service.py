import logging
from evaluation.rag_evaluator import evaluate_rag_quality
from config import settings

log = logging.getLogger("evaluation_service")

def evaluate_response(actual_response: dict, expected_data: dict) -> dict:
    result = {
        "passed": False,
        "response_score": actual_response.get("metadata", {}).get("response_score", 0.0),
        "intent_match": False,
        "tool_match": False,
        "keyword_match_score": 0.0,
        "rag_score": 0.0
    }
    
    # Intent Check
    expected_intent = expected_data.get("expected_intent")
    actual_intent = actual_response.get("intent")
    if expected_intent and actual_intent == expected_intent:
        result["intent_match"] = True
        
    # Tool Check
    expected_tools = expected_data.get("expected_tools", [])
    actual_tools = actual_response.get("tools_used", [])
    if expected_tools:
        matched_tools = [t for t in expected_tools if t in actual_tools]
        result["tool_match"] = len(matched_tools) == len(expected_tools)
    else:
        result["tool_match"] = True
        
    # Keywords Check (on reply)
    expected_keywords = expected_data.get("expected_keywords", [])
    actual_reply = actual_response.get("reply", "").lower()
    
    if expected_keywords:
        matched_kw = [kw for kw in expected_keywords if kw.lower() in actual_reply]
        result["keyword_match_score"] = len(matched_kw) / len(expected_keywords)
    else:
        result["keyword_match_score"] = 1.0
        
    # RAG Check (on context)
    context_str = str(actual_response.get("context_used", {}))
    rag_result = evaluate_rag_quality(context_str, expected_keywords)
    result["rag_score"] = rag_result["rag_score"]
    
    # Passed Check
    min_score = expected_data.get("minimum_score", settings.MIN_ACCEPTABLE_RESPONSE_SCORE)
    
    if (result["intent_match"] and 
        result["tool_match"] and 
        result["response_score"] >= min_score):
        result["passed"] = True
        
    return result
