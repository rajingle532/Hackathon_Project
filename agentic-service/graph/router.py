"""
LangGraph Router (Module 2)
Classifies user intent and routes to the appropriate agent.
"""
from typing import Literal
from langchain_google_genai import ChatGoogleGenAI
from pydantic import BaseModel, Field
from config import settings
from utils.logger import setup_logger
from graph.state import GraphState

log = setup_logger("router")

class IntentClassification(BaseModel):
    intent: Literal[
        "advisory",
        "weather",
        "recommendation",
        "disease",
        "market",
        "escalation",
        "profile_update",
        "video_support",
        "unknown"
    ] = Field(description="The user's core intent.")

def classify_intent(state: GraphState) -> GraphState:
    """Classifies the intent based on the conversation history."""
    log.info("Classifying user intent")
    
    if not settings.is_llm_configured:
        log.warning("LLM not configured. Falling back to 'unknown' intent.")
        return {"intent": "unknown"}
        
    try:
        llm = ChatGoogleGenAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0,
        )
        structured_llm = llm.with_structured_output(IntentClassification)
        
        messages = state.get("messages", [])
        if not messages:
             return {"intent": "unknown"}
             
        # Create a prompt for the classifier
        prompt = "You are a routing agent for Krishi Sakhi. Classify the user intent based on the latest message. If the user asks for an expert, consultant, or states it is an emergency, classify as 'escalation'."
        # For structured output, we just invoke it with messages
        classification = structured_llm.invoke(messages)
        intent = classification.intent
        log.info(f"Classified intent: {intent}")
        return {"intent": intent}
    except Exception as e:
        log.error(f"Intent classification failed: {e}")
        return {"intent": "unknown"}

def route_intent(state: GraphState) -> str:
    """Conditional router based on intent."""
    intent = state.get("intent", "unknown")
    
    allowed_routes = [
        "advisory", "weather", "recommendation", "disease",
        "market", "escalation", "profile_update", "video_support"
    ]
    
    if intent in allowed_routes:
        return f"{intent}_agent"
    
    log.info(f"Unknown intent: {intent}. Routing to advisory_agent as fallback.")
    return "advisory_agent"
