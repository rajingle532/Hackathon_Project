from graph.state import GraphState
from utils.language_utils import normalize_language
from tools.translation_tool import needs_translation, translate_to_english, translate_from_english
from tools.escalation_tool import get_escalation_context
from services.escalation_service import generate_escalation_response
from utils.escalation_fallbacks import ESCALATION_AGENT_FALLBACK
import asyncio

async def escalation_agent_node(state: GraphState) -> GraphState:
    messages = state.get("messages", [])
    if not messages:
        return state
        
    last_message = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
    language = state.get("language", "English")
    
    # 1. Normalize and translate
    normalized_lang = normalize_language(language)
    translated_msg = translate_to_english(last_message, normalized_lang)
    
    # Check if we got here from another agent that failed confidence check
    prev_agent = state.get("metadata", {}).get("agent_used", "unknown")
    prev_conf = state.get("metadata", {}).get("agent_confidence", 0.0)
    intent = state.get("intent", "general")
    
    # 2. Extract escalation context
    esc_ctx = get_escalation_context(intent, prev_conf, translated_msg)
    
    tools_used = ["escalation_tool"]
    if needs_translation(normalized_lang):
        tools_used.append("translation_tool")
        
    prev_ctx = {"agent_used": prev_agent, "agent_confidence": prev_conf}
    
    # 3. Generate LLM response
    response = await generate_escalation_response(
        farmer_message=translated_msg,
        escalation_context=esc_ctx,
        previous_agent_context=prev_ctx,
        memory_context=state.get("memory_context")
    )
    
    # 4. Translate back
    final_resp = translate_from_english(response, normalized_lang)
    
    is_fallback = final_resp == ESCALATION_AGENT_FALLBACK or response.startswith("I recommend contacting")
    
    # 5. Build metadata
    metadata = state.get("metadata", {})
    metadata.update({
        "requires_escalation": True,
        "escalation_reason": esc_ctx.get("escalation_reason"),
        "consultant_type": esc_ctx.get("consultant_type"),
        "escalation_target": esc_ctx.get("escalation_target"),
        "fallback": is_fallback
    })
    
    context_used = state.get("context_used", {})
    context_used.update({
        "escalation": True,
        "translation": needs_translation(normalized_lang)
    })
    
    return {
        "agent_used": "escalation_agent",
        "translated_message": translated_msg,
        "tools_used": tools_used,
        "final_answer": final_resp,
        "final_response": final_resp,
        "language": normalized_lang,
        "metadata": metadata,
        "context_used": context_used,
        "is_fallback": is_fallback,
        "requires_escalation": True,
        "escalation_reason": esc_ctx.get("escalation_reason"),
        "consultant_type": esc_ctx.get("consultant_type"),
        "escalation_target": esc_ctx.get("escalation_target")
    }
