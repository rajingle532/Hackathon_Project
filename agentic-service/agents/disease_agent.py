from graph.state import GraphState
from utils.language_utils import normalize_language
from tools.translation_tool import needs_translation, translate_to_english, translate_from_english
from tools.disease_tool import get_disease_context, disease_needed
from tools.retrieval_tool import retrieve_context_with_metadata
from services.disease_service import generate_disease_response
from utils.disease_fallbacks import DISEASE_AGENT_FALLBACK
from config import settings
import asyncio

async def disease_agent_node(state: GraphState) -> GraphState:
    messages = state.get("messages", [])
    if not messages:
        return state
        
    last_message = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
    language = state.get("language", "English")
    image_path = state.get("uploaded_image_path")
    
    # 1. Normalize and translate
    normalized_lang = normalize_language(language)
    translated_msg = translate_to_english(last_message, normalized_lang)
    
    # 2. Extract disease context
    disease_ctx = get_disease_context(translated_msg, image_path)
    
    # 3. Retrieve relevant knowledge based on prediction or message
    search_query = translated_msg
    if disease_ctx.get("disease_name") and disease_ctx.get("disease_name") != "Unknown Disease":
        search_query += f" {disease_ctx['disease_name']}"
        
    retrieval_meta = retrieve_context_with_metadata(search_query)
    retrieval_ctx = retrieval_meta.get("retrieval_context", "")
    
    tools_used = ["disease_tool"]
    if retrieval_ctx:
        tools_used.append("retrieval_tool")
    if needs_translation(normalized_lang):
        tools_used.append("translation_tool")
        
    # 4. Generate LLM response
    response = await generate_disease_response(
        farmer_message=translated_msg,
        disease_context=disease_ctx,
        retrieval_context=retrieval_ctx,
        memory_context=state.get("memory_context")
    )
    
    # 5. Translate back
    final_resp = translate_from_english(response, normalized_lang)
    
    is_fallback = final_resp == DISEASE_AGENT_FALLBACK or response.startswith("I am unable")
    
    # 6. Build metadata
    metadata = state.get("metadata", {})
    # Set explicit escalation metadata
    req_escalation = disease_ctx.get("requires_escalation") or (disease_ctx.get("confidence", 0.0) < settings.ESCALATION_CONFIDENCE_THRESHOLD)
    
    metadata.update({
        "disease_name": disease_ctx.get("disease_name"),
        "disease_confidence": disease_ctx.get("confidence"),
        "symptoms_detected": disease_ctx.get("symptoms_detected"),
        "requires_escalation": req_escalation,
        "escalation_reason": "Low disease confidence" if req_escalation else None,
        "consultant_type": "Plant Pathologist" if req_escalation else None,
        "escalation_target": settings.DEFAULT_ESCALATION_TARGET if req_escalation else None,
        "agent_confidence": disease_ctx.get("confidence"),
        "retrieval_sources": retrieval_meta.get("sources", []),
        "retrieval_categories": retrieval_meta.get("categories", []),
        "retrieval_scores": retrieval_meta.get("scores", []),
        "fallback": is_fallback
    })
    
    context_used = state.get("context_used", {})
    context_used.update({
        "disease": True,
        "retrieval": bool(retrieval_ctx),
        "translation": needs_translation(normalized_lang)
    })
    
    return {
        "agent_used": "disease_agent",
        "translated_message": translated_msg,
        "retrieved_context": retrieval_ctx,
        "tools_used": tools_used,
        "final_answer": final_resp,
        "final_response": final_resp,
        "language": normalized_lang,
        "metadata": metadata,
        "context_used": context_used,
        "is_fallback": is_fallback,
        "disease_prediction": disease_ctx,
        "disease_name": disease_ctx.get("disease_name"),
        "disease_confidence": disease_ctx.get("confidence"),
        "symptoms_detected": disease_ctx.get("symptoms_detected"),
        "treatment_recommendation": disease_ctx.get("treatment"),
        "requires_escalation": req_escalation,
        "escalation_reason": "Low disease confidence" if req_escalation else None,
        "consultant_type": "Plant Pathologist" if req_escalation else None,
        "escalation_target": settings.DEFAULT_ESCALATION_TARGET if req_escalation else None,
        "agent_confidence": disease_ctx.get("confidence")
    }
