def normalize_rag_evaluation(eval_data: dict) -> dict:
    if not isinstance(eval_data, dict):
        return {}
    return {
        "rag_score": float(eval_data.get("rag_score", 0.0)),
        "matched_keywords": list(eval_data.get("matched_keywords", [])),
        "missing_keywords": list(eval_data.get("missing_keywords", []))
    }

def validate_rag_evaluation(eval_data: dict) -> bool:
    if not isinstance(eval_data, dict):
        return False
    if "rag_score" not in eval_data:
        return False
    return True
