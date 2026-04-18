def build_feedback_summary_prompt(feedback_summary: dict) -> str:
    """
    Generate future prompt snippets from historical feedback.
    This is prepared for future integration.
    """
    if not feedback_summary or feedback_summary.get("total_feedback", 0) == 0:
        return ""
        
    prompt = "=== HISTORICAL FEEDBACK ON THIS TOPIC ===\n"
    for idx, fb in enumerate(feedback_summary.get("feedbacks", [])):
        prompt += f"{idx+1}. Type: {fb.get('feedback_type')}\n"
        if fb.get('feedback_reason'):
            prompt += f"   Reason: {fb.get('feedback_reason')}\n"
    
    return prompt
