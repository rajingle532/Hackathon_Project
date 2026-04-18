from utils.market_prompts import MARKET_SYSTEM_PROMPT
from utils.market_constants import ESCALATION_THRESHOLD

def build_market_prompt(
    farmer_message: str,
    market_context: dict,
    retrieval_context: str,
    memory_context: dict = None
) -> str:
    prompt = f"{MARKET_SYSTEM_PROMPT}\n\n"
    
    if memory_context:
        profile_ctx = memory_context.get("profile_context", "")
        history_ctx = memory_context.get("history_context", "")
        if profile_ctx:
            prompt += f"=== FARMER PROFILE ===\n{profile_ctx}\n\n"
        if history_ctx:
            prompt += f"=== RECENT HISTORY ===\n{history_ctx}\n\n"
    
    prompt += "=== FARMER MESSAGE ===\n"
    prompt += f"{farmer_message}\n\n"
    
    prompt += "=== MARKET CONTEXT ===\n"
    prompt += f"Commodity: {market_context.get('commodity_name', 'Unknown')}\n"
    prompt += f"Location: {market_context.get('market_location', 'Unknown')}\n"
    prompt += f"Current Price: {market_context.get('market_price', 'Unknown')}\n"
    prompt += f"Price Trend: {market_context.get('price_trend', 'Unknown')}\n"
    prompt += f"Confidence Score: {market_context.get('confidence', 0.0)}\n"
    prompt += f"Suggested Advice: {market_context.get('selling_advice', 'None')}\n"
            
    if market_context.get('confidence', 0.0) < ESCALATION_THRESHOLD:
        prompt += "\n**WARNING:** Market data confidence is low. Please remind the farmer to verify prices locally at their nearest mandi.\n"
        
    if retrieval_context:
        prompt += "\n=== AGRICULTURE KNOWLEDGE CONTEXT ===\n"
        prompt += f"{retrieval_context}\n"
        
    prompt += "\n=== RESPONSE INSTRUCTIONS ===\n"
    prompt += "Provide an expert market analysis and selling recommendation based on the above information.\n"
    
    return prompt
