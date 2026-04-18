from utils.escalation_prompts import ESCALATION_SYSTEM_PROMPT

def build_escalation_prompt(
    farmer_message: str,
    escalation_context: dict,
    previous_agent_context: dict,
    memory_context: dict = None
) -> str:
    prompt = f"{ESCALATION_SYSTEM_PROMPT}\n\n"
    
    if memory_context:
        profile_ctx = memory_context.get("profile_context", "")
        history_ctx = memory_context.get("history_context", "")
        if profile_ctx:
            prompt += f"=== FARMER PROFILE ===\n{profile_ctx}\n\n"
        if history_ctx:
            prompt += f"=== RECENT HISTORY ===\n{history_ctx}\n\n"
    
    prompt += "=== FARMER MESSAGE ===\n"
    prompt += f"{farmer_message}\n\n"
    
    prompt += "=== ESCALATION DETAILS ===\n"
    prompt += f"Reason: {escalation_context.get('escalation_reason', 'Unknown')}\n"
    prompt += f"Consultant Type: {escalation_context.get('consultant_type', 'Agriculture Officer')}\n"
    prompt += f"Target: {escalation_context.get('escalation_target', 'Local Agriculture Department')}\n\n"
    
    if previous_agent_context:
        prompt += "=== PREVIOUS AGENT ATTEMPT (For Context) ===\n"
        prompt += f"Agent: {previous_agent_context.get('agent_used', 'None')}\n"
        prompt += f"Confidence: {previous_agent_context.get('agent_confidence', 0.0)}\n\n"
        
    prompt += "=== RESPONSE INSTRUCTIONS ===\n"
    prompt += "Explain why we cannot fulfill the request automatically and suggest the above consultant.\n"
    
    return prompt
