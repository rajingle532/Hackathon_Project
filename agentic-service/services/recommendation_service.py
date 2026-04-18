from services.recommendation_prompt_service import build_recommendation_prompt
from services.llm_service import call_llm
from utils.recommendation_fallbacks import RECOMMENDATION_AGENT_FALLBACK
from utils.logger import setup_logger

log = setup_logger("recommendation_service")

async def generate_recommendation_response(
    farmer_message: str,
    farm_profile: dict,
    recommendation_context: dict,
    retrieval_context: str,
    memory_context: dict = None
) -> str:
    try:
        prompt = build_recommendation_prompt(
            farmer_message=farmer_message,
            farm_profile=farm_profile,
            recommendation_context=recommendation_context,
            retrieval_context=retrieval_context,
            memory_context=memory_context
        )
        
        response = await call_llm(prompt)
        return response
    except Exception as e:
        log.error(f"Failed to generate recommendation response: {e}")
        return RECOMMENDATION_AGENT_FALLBACK
