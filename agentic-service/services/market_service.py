from services.market_prompt_service import build_market_prompt
from services.llm_service import call_llm
from utils.market_fallbacks import MARKET_AGENT_FALLBACK
from utils.logger import setup_logger

log = setup_logger("market_service")

async def generate_market_response(
    farmer_message: str,
    market_context: dict,
    retrieval_context: str,
    memory_context: dict = None
) -> str:
    try:
        prompt = build_market_prompt(
            farmer_message=farmer_message,
            market_context=market_context,
            retrieval_context=retrieval_context,
            memory_context=memory_context
        )
        
        response = await call_llm(prompt)
        return response
    except Exception as e:
        log.error(f"Failed to generate market response: {e}")
        return MARKET_AGENT_FALLBACK
