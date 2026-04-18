from services.disease_prompt_service import build_disease_prompt
from services.llm_service import call_llm
from utils.disease_fallbacks import DISEASE_AGENT_FALLBACK
from utils.logger import setup_logger

log = setup_logger("disease_service")

async def generate_disease_response(
    farmer_message: str,
    disease_context: dict,
    retrieval_context: str,
    memory_context: dict = None
) -> str:
    try:
        prompt = build_disease_prompt(
            farmer_message=farmer_message,
            disease_context=disease_context,
            retrieval_context=retrieval_context,
            memory_context=memory_context
        )
        
        response = await call_llm(prompt)
        return response
    except Exception as e:
        log.error(f"Failed to generate disease response: {e}")
        return DISEASE_AGENT_FALLBACK
