from services.prompt_service import build_advisory_prompt
from services.llm_service import call_llm
from utils.logger import setup_logger

log = setup_logger("advisory_service")

async def generate_advisory_response(
    message: str,
    language: str,
    weather_context: dict = None,
    retrieval_context: str = "",
    retrieval_metadata: dict = None,
    memory_context: dict = None
) -> str:
    try:
        # In this setup, we assume message is the translated_message.
        # Original message can be inferred or passed if needed, but signature is fixed.
        prompt = build_advisory_prompt(
            original_message=message, 
            translated_message=message, 
            weather_context=weather_context or {},
            retrieval_context=retrieval_context,
            language=language,
            retrieval_metadata=retrieval_metadata,
            memory_context=memory_context
        )
        
        response = await call_llm(prompt)
        return response
    except Exception as e:
        log.error(f"Failed to generate advisory response: {e}")
        return "I am unable to generate a detailed recommendation right now. Please consult a local agriculture officer for urgent crop issues."
