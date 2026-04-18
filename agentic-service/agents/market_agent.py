from graph.state import GraphState
from utils.language_utils import normalize_language
from tools.translation_tool import needs_translation, translate_to_english, translate_from_english
from tools.market_tool import get_market_context, market_needed
from tools.retrieval_tool import retrieve_context_with_metadata
from services.market_service import generate_market_response
from utils.market_fallbacks import MARKET_AGENT_FALLBACK
from config import settings
import asyncio

async def market_agent_node(state: GraphState) -> GraphState:
    messages = state.get("messages", [])
    if not messages:
        return state
        
    last_message = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
    language = state.get("language", "English")
    
    # 1. Normalize and translate
    normalized_lang = normalize_language(language)
    translated_msg = translate_to_english(last_message, normalized_lang)
    
    # 2. Extract market context
    market_ctx = get_market_context(translated_msg)
    
    # 3. Retrieve relevant knowledge based on prediction or message
    search_query = translated_msg
    commodity = market_ctx.get("commodity_name")
    if commodity and commodity != "Unknown":
        search_query += f" {commodity} storage selling"
        
    retrieval_meta = retrieve_context_with_metadata(search_query)
    retrieval_ctx = retrieval_meta.get("retrieval_context", "")
    
    tools_used = ["market_tool"]
    if retrieval_ctx:
        tools_used.append("retrieval_tool")
    if needs_translation(normalized_lang):
        tools_used.append("translation_tool")
        
    # 4. Generate LLM response
    response = await generate_market_response(
        farmer_message=translated_msg,
        market_context=market_ctx,
        retrieval_context=retrieval_ctx,
        memory_context=state.get("memory_context")
    )
    
    # 5. Translate back
    final_resp = translate_from_english(response, normalized_lang)
    
    is_fallback = final_resp == MARKET_AGENT_FALLBACK or response.startswith("I am unable")
    
    # 6. Build metadata
    metadata = state.get("metadata", {})
    # Set explicit escalation metadata
    req_escalation = market_ctx.get("confidence", 0.0) < settings.ESCALATION_CONFIDENCE_THRESHOLD
    
    metadata.update({
        "commodity_name": market_ctx.get("commodity_name"),
        "market_location": market_ctx.get("market_location"),
        "market_price": market_ctx.get("market_price"),
        "price_trend": market_ctx.get("price_trend"),
        "market_confidence": market_ctx.get("confidence"),
        "requires_escalation": req_escalation,
        "escalation_reason": "Low market confidence" if req_escalation else None,
        "consultant_type": "Market Advisor" if req_escalation else None,
        "escalation_target": settings.DEFAULT_ESCALATION_TARGET if req_escalation else None,
        "agent_confidence": market_ctx.get("confidence"),
        "retrieval_sources": retrieval_meta.get("sources", []),
        "retrieval_categories": retrieval_meta.get("categories", []),
        "retrieval_scores": retrieval_meta.get("scores", []),
        "fallback": is_fallback
    })
    
    context_used = state.get("context_used", {})
    context_used.update({
        "market": True,
        "retrieval": bool(retrieval_ctx),
        "translation": needs_translation(normalized_lang)
    })
    
    return {
        "agent_used": "market_agent",
        "translated_message": translated_msg,
        "retrieved_context": retrieval_ctx,
        "tools_used": tools_used,
        "final_answer": final_resp,
        "final_response": final_resp,
        "language": normalized_lang,
        "metadata": metadata,
        "context_used": context_used,
        "is_fallback": is_fallback,
        "commodity_name": market_ctx.get("commodity_name"),
        "market_location": market_ctx.get("market_location"),
        "market_price": market_ctx.get("market_price"),
        "price_trend": market_ctx.get("price_trend"),
        "selling_advice": market_ctx.get("selling_advice"),
        "market_confidence": market_ctx.get("confidence"),
        "requires_escalation": req_escalation,
        "escalation_reason": "Low market confidence" if req_escalation else None,
        "consultant_type": "Market Advisor" if req_escalation else None,
        "escalation_target": settings.DEFAULT_ESCALATION_TARGET if req_escalation else None,
        "agent_confidence": market_ctx.get("confidence")
    }
