from utils.disease_prompts import DISEASE_SYSTEM_PROMPT

def build_disease_prompt(
    farmer_message: str,
    disease_context: dict,
    retrieval_context: str,
    memory_context: dict = None
) -> str:
    prompt = f"{DISEASE_SYSTEM_PROMPT}\n\n"
    
    if memory_context:
        profile_ctx = memory_context.get("profile_context", "")
        history_ctx = memory_context.get("history_context", "")
        if profile_ctx:
            prompt += f"=== FARMER PROFILE ===\n{profile_ctx}\n\n"
        if history_ctx:
            prompt += f"=== RECENT HISTORY ===\n{history_ctx}\n\n"
    
    prompt += "=== FARMER MESSAGE ===\n"
    prompt += f"{farmer_message}\n\n"
    
    prompt += "=== DISEASE CONTEXT ===\n"
    prompt += f"Symptoms Detected: {', '.join(disease_context.get('symptoms_detected', []))}\n"
    prompt += f"Predicted Disease: {disease_context.get('disease_name', 'Unknown')}\n"
    prompt += f"Confidence Score: {disease_context.get('confidence', 0.0)}\n"
    
    if disease_context.get("requires_escalation"):
        prompt += "\n**ESCALATION REQUIRED:** The confidence score is low or the condition may be severe. Suggest consulting an expert.\n"
        
    if retrieval_context:
        prompt += "\n=== AGRICULTURE KNOWLEDGE CONTEXT ===\n"
        prompt += f"{retrieval_context}\n"
        
    prompt += "\n=== RESPONSE INSTRUCTIONS ===\n"
    prompt += "Provide an expert diagnosis and treatment plan based on the above information.\n"
    
    return prompt
