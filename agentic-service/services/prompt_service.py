from utils.advisory_prompts import ADVISORY_SYSTEM_PROMPT

def build_advisory_prompt(
    original_message: str,
    translated_message: str,
    weather_context: dict,
    retrieval_context: str,
    language: str,
    retrieval_metadata: dict = None,
    memory_context: dict = None
) -> str:
    prompt = f"{ADVISORY_SYSTEM_PROMPT}\n\n"
    
    if memory_context:
        profile_ctx = memory_context.get("profile_context", "")
        history_ctx = memory_context.get("history_context", "")
        if profile_ctx:
            prompt += f"=== FARMER PROFILE ===\n{profile_ctx}\n\n"
        if history_ctx:
            prompt += f"=== RECENT HISTORY ===\n{history_ctx}\n\n"
    
    prompt += "=== FARMER QUESTION ===\n"
    prompt += f"Original message ({language}): {original_message}\n"
    if translated_message != original_message:
        prompt += f"Translated message (English): {translated_message}\n"
        
    if weather_context:
        prompt += "\n=== WEATHER CONTEXT ===\n"
        prompt += f"Temperature: {weather_context.get('temperature', 'N/A')}\n"
        prompt += f"Condition: {weather_context.get('condition', 'N/A')}\n"
        prompt += f"Humidity: {weather_context.get('humidity', 'N/A')}\n"
        prompt += f"Wind Speed: {weather_context.get('wind_speed', 'N/A')}\n"
        prompt += f"Advice: {weather_context.get('advice', 'N/A')}\n"
        
    if retrieval_context:
        prompt += "\n=== AGRICULTURE KNOWLEDGE CONTEXT ===\n"
        if retrieval_metadata:
            sources = ", ".join(retrieval_metadata.get("sources", []))
            categories = ", ".join(retrieval_metadata.get("categories", []))
            prompt += f"Source: {sources}\n"
            prompt += f"Category: {categories}\n"
        prompt += "Knowledge:\n"
        prompt += f"{retrieval_context}\n"
        
    prompt += "\n=== RESPONSE INSTRUCTIONS ===\n"
    prompt += "Based on the context above, provide your expert agricultural advice.\n"
    prompt += "- Use provided context if relevant.\n"
    prompt += "- Do not invent additional facts.\n"
    prompt += "- If retrieval confidence is weak, mention uncertainty.\n"
    prompt += "- Prefer the retrieved knowledge over guessing.\n"
    prompt += "- Keep it farmer-friendly and within safety guidelines.\n"
    
    return prompt
