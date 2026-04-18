from graph.state import GraphState
from utils.language_utils import normalize_language
from tools.translation_tool import needs_translation, translate_to_english, translate_from_english
from tools.weather_tool import get_weather_context
from tools.retrieval_tool import retrieve_context_with_metadata
from services.advisory_service import generate_advisory_response
import asyncio

async def advisory_agent_node(state: GraphState) -> GraphState:
    messages = state.get("messages", [])
    if not messages:
        return state
        
    last_message = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
    language = state.get("language", "English")
    
    # 1. Normalize language
    normalized_lang = normalize_language(language)
    
    # 2. Translate to English if needed
    translated_msg = translate_to_english(last_message, normalized_lang)
    
    # 3. Determine if weather context is needed & get it
    weather_ctx = get_weather_context(translated_msg)
    
    # 4. Determine if retrieval context is needed & get it
    retrieval_meta = retrieve_context_with_metadata(translated_msg)
    retrieval_ctx = retrieval_meta.get("retrieval_context", "")
    
    tools_used = []
    if weather_ctx:
        tools_used.append("weather_tool")
    if retrieval_ctx:
        tools_used.append("retrieval_tool")
    if needs_translation(normalized_lang):
        tools_used.append("translation_tool")
        
    # 5. Call LLM
    response = await generate_advisory_response(
        message=translated_msg, # Passing translated_msg to generate response
        language=normalized_lang,
        weather_context=weather_ctx,
        retrieval_context=retrieval_ctx,
        retrieval_metadata=retrieval_meta,
        memory_context=state.get("memory_context")
    )
    
    # 6. Translate back
    final_resp = translate_from_english(response, normalized_lang)
    
    is_fallback = response.startswith("I am unable")
    
    # 7. Return updated state
    return {
        "agent_used": "advisory_agent",
        "translated_message": translated_msg,
        "retrieved_context": retrieval_ctx,
        "tools_used": tools_used,
        "tool_outputs": {"weather": weather_ctx},
        "final_answer": final_resp,
        "final_response": final_resp,
        "language": normalized_lang,
        "metadata": {
            "fallback": is_fallback,
            "weather_location": weather_ctx.get("location") if weather_ctx else None,
            "retrieval_sources": retrieval_meta.get("sources", []),
            "retrieval_categories": retrieval_meta.get("categories", []),
            "retrieval_scores": retrieval_meta.get("scores", [])
        },
        "context_used": {
            "weather": bool(weather_ctx),
            "retrieval": bool(retrieval_ctx),
            "translation": needs_translation(normalized_lang)
        },
        "is_fallback": is_fallback
    }
