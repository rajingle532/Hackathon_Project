def normalize_evaluation_result(result: dict) -> dict:
    if not isinstance(result, dict):
        return {}
    return {
        "passed": bool(result.get("passed", False)),
        "response_score": float(result.get("response_score", 0.0)),
        "intent_match": bool(result.get("intent_match", False)),
        "tool_match": bool(result.get("tool_match", False)),
        "keyword_match_score": float(result.get("keyword_match_score", 0.0)),
        "rag_score": float(result.get("rag_score", 0.0))
    }

def validate_evaluation_result(result: dict) -> bool:
    if not isinstance(result, dict):
        return False
    if "passed" not in result:
        return False
    return True
