from typing import TypedDict, Annotated, List, Optional, Any, Dict
import operator

class GraphState(TypedDict):
    """
    The state of the LangGraph workflow.
    """
    farmer_id: Optional[str]
    language: str
    messages: Annotated[List[Any], operator.add]
    intent: Optional[str]
    agent_used: Optional[str]
    final_response: Optional[str]
    cards: Optional[List[Dict[str, Any]]]
    is_fallback: Optional[bool]
    context_used: Optional[Dict[str, Any]]
    
    # Module 3 Additions
    tool_outputs: Optional[Dict[str, Any]]
    tools_used: Optional[List[str]]
    retrieved_context: Optional[str]
    translated_message: Optional[str]
    final_answer: Optional[str]
    metadata: Optional[Dict[str, Any]]
    
    # Module 6 Additions
    disease_prediction: Optional[Dict[str, Any]]
    disease_name: Optional[str]
    disease_confidence: Optional[float]
    symptoms_detected: Optional[List[str]]
    treatment_recommendation: Optional[str]
    requires_escalation: Optional[bool]
    uploaded_image_path: Optional[str]

    # Module 7 Additions
    soil_type: Optional[str]
    season: Optional[str]
    location: Optional[str]
    rainfall_level: Optional[str]
    irrigation_available: Optional[bool]
    recommended_crops: Optional[List[str]]
    recommendation_confidence: Optional[float]
    recommendation_reasoning: Optional[List[str]]
    farm_profile: Optional[Dict[str, Any]]
    
    # Module 8 Additions
    commodity_name: Optional[str]
    market_location: Optional[str]
    market_price: Optional[str]
    price_trend: Optional[str]
    selling_advice: Optional[str]
    market_confidence: Optional[float]
    market_sources: Optional[List[str]]
    
    # Module 9 Additions
    requires_escalation: Optional[bool]
    escalation_reason: Optional[str]
    escalation_target: Optional[str]
    consultant_type: Optional[str]
    consultant_requested: Optional[bool]
    agent_confidence: Optional[float]
    
    # Module 10 Additions
    farmer_profile: Optional[Dict[str, Any]]
    chat_history: Optional[List[Dict[str, Any]]]
    previous_recommendations: Optional[List[Dict[str, Any]]]
    previous_disease_cases: Optional[List[Dict[str, Any]]]
    conversation_summary: Optional[str]
    memory_context: Optional[Dict[str, Any]]
    profile_loaded: Optional[bool]
    history_loaded: Optional[bool]

    # Module 11 Additions
    mongo_connected: Optional[bool]
    memory_source: Optional[str]
    persistence_success: Optional[bool]

    # Module 12 Additions
    response_score: Optional[float]
    feedback_received: Optional[bool]
    feedback_type: Optional[str]
    hindsight_status: Optional[str]
    telemetry_event_id: Optional[str]
    response_quality: Optional[str]

    # Module 13 Additions
    background_tasks_scheduled: Optional[bool]
    background_task_ids: Optional[List[str]]
    async_persistence_enabled: Optional[bool]
    async_telemetry_enabled: Optional[bool]
    event_dispatch_status: Optional[str]

    # Module 15 Additions
    authenticated: Optional[bool]
    auth_type: Optional[str]
    rate_limit_remaining: Optional[int]
    pii_detected: Optional[bool]
    prompt_injection_detected: Optional[bool]
    request_blocked: Optional[bool]
    security_flags: Optional[List[str]]
