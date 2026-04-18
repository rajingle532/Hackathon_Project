from graph.state import GraphState
from utils.language_utils import normalize_language
from tools.translation_tool import needs_translation, translate_to_english, translate_from_english
from tools.recommendation_tool import get_recommendation_context, recommendation_needed
from tools.retrieval_tool import retrieve_context_with_metadata
from services.recommendation_service import generate_recommendation_response
from utils.recommendation_fallbacks import RECOMMENDATION_AGENT_FALLBACK
from config import settings
import asyncio

async def recommendation_agent_node(state: GraphState) -> GraphState:
    messages = state.get("messages", [])
    if not messages:
        return state
        
    last_message = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
    language = state.get("language", "English")
    
    # 1. Normalize and translate
    normalized_lang = normalize_language(language)
    translated_msg = translate_to_english(last_message, normalized_lang)
    
    # 2. Extract recommendation context
    rec_ctx = get_recommendation_context(translated_msg)
    profile = rec_ctx.get("farm_profile", {})
    
    # 3. Retrieve relevant knowledge based on prediction or message
    search_query = translated_msg
    crops = rec_ctx.get("recommended_crops", [])
    if crops:
        search_query += " " + " ".join(crops)
        
    retrieval_meta = retrieve_context_with_metadata(search_query)
    retrieval_ctx = retrieval_meta.get("retrieval_context", "")
    
    tools_used = ["recommendation_tool"]
    if retrieval_ctx:
        tools_used.append("retrieval_tool")
    if needs_translation(normalized_lang):
        tools_used.append("translation_tool")
        
    # 4. Generate LLM response
    response = await generate_recommendation_response(
        farmer_message=translated_msg,
        farm_profile=profile,
        recommendation_context=rec_ctx,
        retrieval_context=retrieval_ctx,
        memory_context=state.get("memory_context")
    )
    
    # 5. Translate back
    final_resp = translate_from_english(response, normalized_lang)
    
    is_fallback = final_resp == RECOMMENDATION_AGENT_FALLBACK or response.startswith("I am unable")
    
    # 6. Build metadata
    metadata = state.get("metadata", {})
    # Set explicit escalation metadata
    req_escalation = rec_ctx.get("confidence", 0.0) < settings.ESCALATION_CONFIDENCE_THRESHOLD
    
    metadata.update({
        "recommended_crops": crops,
        "recommendation_confidence": rec_ctx.get("confidence"),
        "soil_type": profile.get("soil_type"),
        "season": profile.get("season"),
        "location": profile.get("location"),
        "requires_escalation": req_escalation,
        "escalation_reason": "Low recommendation confidence" if req_escalation else None,
        "consultant_type": "Agriculture Officer" if req_escalation else None,
        "escalation_target": settings.DEFAULT_ESCALATION_TARGET if req_escalation else None,
        "agent_confidence": rec_ctx.get("confidence"),
        "retrieval_sources": retrieval_meta.get("sources", []),
        "retrieval_categories": retrieval_meta.get("categories", []),
        "retrieval_scores": retrieval_meta.get("scores", []),
        "fallback": is_fallback
    })
    
    context_used = state.get("context_used", {})
    context_used.update({
        "recommendation": True,
        "retrieval": bool(retrieval_ctx),
        "translation": needs_translation(normalized_lang)
    })
    
    return {
        "agent_used": "recommendation_agent",
        "translated_message": translated_msg,
        "retrieved_context": retrieval_ctx,
        "tools_used": tools_used,
        "final_answer": final_resp,
        "final_response": final_resp,
        "language": normalized_lang,
        "metadata": metadata,
        "context_used": context_used,
        "is_fallback": is_fallback,
        "recommended_crops": crops,
        "recommendation_confidence": rec_ctx.get("confidence"),
        "recommendation_reasoning": rec_ctx.get("reasoning", []),
        "farm_profile": profile,
        "soil_type": profile.get("soil_type"),
        "season": profile.get("season"),
        "location": profile.get("location"),
        "rainfall_level": profile.get("rainfall_level"),
        "irrigation_available": profile.get("irrigation_available"),
        "requires_escalation": req_escalation,
        "escalation_reason": "Low recommendation confidence" if req_escalation else None,
        "consultant_type": "Agriculture Officer" if req_escalation else None,
        "escalation_target": settings.DEFAULT_ESCALATION_TARGET if req_escalation else None,
        "agent_confidence": rec_ctx.get("confidence")
    }
