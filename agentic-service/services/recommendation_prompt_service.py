from utils.recommendation_prompts import RECOMMENDATION_SYSTEM_PROMPT

def build_recommendation_prompt(
    farmer_message: str,
    farm_profile: dict,
    recommendation_context: dict,
    retrieval_context: str,
    memory_context: dict = None
) -> str:
    prompt = f"{RECOMMENDATION_SYSTEM_PROMPT}\n\n"
    
    if memory_context:
        profile_ctx = memory_context.get("profile_context", "")
        history_ctx = memory_context.get("history_context", "")
        if profile_ctx:
            prompt += f"=== FARMER PROFILE (SAVED) ===\n{profile_ctx}\n\n"
        if history_ctx:
            prompt += f"=== RECENT HISTORY ===\n{history_ctx}\n\n"
    
    prompt += "=== FARMER MESSAGE ===\n"
    prompt += f"{farmer_message}\n\n"
    
    prompt += "=== FARM PROFILE ===\n"
    prompt += f"Soil Type: {farm_profile.get('soil_type', 'Unknown')}\n"
    prompt += f"Season: {farm_profile.get('season', 'Unknown')}\n"
    prompt += f"Location: {farm_profile.get('location', 'Unknown')}\n"
    prompt += f"Rainfall: {farm_profile.get('rainfall_level', 'Unknown')}\n"
    prompt += f"Irrigation Available: {farm_profile.get('irrigation_available', False)}\n\n"
    
    prompt += "=== RECOMMENDED CROPS (ML PREDICTION) ===\n"
    crops = recommendation_context.get('recommended_crops', [])
    prompt += f"Crops: {', '.join(crops) if crops else 'None'}\n"
    prompt += f"Confidence Score: {recommendation_context.get('confidence', 0.0)}\n"
    
    reasons = recommendation_context.get('reasoning', [])
    if reasons:
        prompt += "Reasoning:\n"
        for r in reasons:
            prompt += f"- {r}\n"
            
    if recommendation_context.get('confidence', 0.0) < 0.60:
        prompt += "\n**WARNING:** Missing or incomplete profile information. Advise the farmer to conduct a soil test or provide more details.\n"
        
    if retrieval_context:
        prompt += "\n=== AGRICULTURE KNOWLEDGE CONTEXT ===\n"
        prompt += f"{retrieval_context}\n"
        
    prompt += "\n=== RESPONSE INSTRUCTIONS ===\n"
    prompt += "Provide an expert crop recommendation based on the above information.\n"
    
    return prompt
