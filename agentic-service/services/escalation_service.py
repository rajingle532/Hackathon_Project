from services.escalation_prompt_service import build_escalation_prompt
from services.llm_service import call_llm
from utils.escalation_fallbacks import ESCALATION_AGENT_FALLBACK
from utils.logger import setup_logger

log = setup_logger("escalation_service")

async def generate_escalation_response(
    farmer_message: str,
    escalation_context: dict,
    previous_agent_context: dict,
    memory_context: dict = None
) -> str:
    try:
        prompt = build_escalation_prompt(
            farmer_message=farmer_message,
            escalation_context=escalation_context,
            previous_agent_context=previous_agent_context,
            memory_context=memory_context
        )
        
        response = await call_llm(prompt)
        return response
    except Exception as e:
        log.error(f"Failed to generate escalation response: {e}")
        return ESCALATION_AGENT_FALLBACK
