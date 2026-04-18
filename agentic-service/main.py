"""
Krishi Sakhi — Agentic Service
================================
FastAPI application serving the agentic AI layer.

This service provides:
  - LangGraph-based intent routing (Module 2)
  - CrewAI agent execution (Module 3+)
  - LangChain tool integration (Module 4+)
  - ChromaDB RAG retrieval (Module 6)
  - Hindsight memory & learning (Module 10+)

Module 1 provides: health check, readiness probe, LLM connectivity,
and backend API connectivity.

Usage:
  python main.py              # starts on port 8080
  uvicorn main:app --reload   # dev mode with auto-reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models.request_models import ChatRequest, FeedbackRequest, HindsightRequest, AuthRequest
from models.response_models import HealthResponse, ReadyResponse, ChatResponse
from fastapi import Request
from services.backend_api_service import backend_api
from services.llm_service import configure_gemini, check_llm_health
from utils.logger import setup_logger

log = setup_logger("main")


# ── Startup / Shutdown ───────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run setup on startup, cleanup on shutdown."""
    log.info("=" * 60)
    log.info(f"[START] {settings.SERVICE_NAME} v{settings.SERVICE_VERSION}")
    log.info(f"   Port:    {settings.PORT}")
    log.info(f"   Backend: {settings.BACKEND_BASE_URL}")
    log.info(f"   ML API:  {settings.ML_API_URL}")
    log.info(f"   Disease: {settings.DISEASE_API_URL}")
    log.info(f"   LLM:     {'configured' if settings.is_llm_configured else 'NOT configured'}")
    log.info("=" * 60)

    # Configure Gemini SDK
    configure_gemini()

    yield  # App is running

    log.info("[STOP] Shutting down agentic service")


# ── Create FastAPI App ───────────────────────────────────────────────
app = FastAPI(
    title="Krishi Sakhi Agentic Service",
    description="Multi-agent AI service for agricultural advisory",
    version=settings.SERVICE_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ───────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """Welcome endpoint."""
    return {
        "message": "Krishi Sakhi Agentic Service",
        "version": settings.SERVICE_VERSION,
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check — returns basic service status."""
    backend_ok = False
    try:
        backend_ok = await backend_api.health_check()
    except Exception:
        pass

    return HealthResponse(
        status="ok",
        service=settings.SERVICE_NAME,
        version=settings.SERVICE_VERSION,
        llm_configured=settings.is_llm_configured,
        backend_reachable=backend_ok,
    )


@app.get("/ready", response_model=ReadyResponse)
async def ready():
    """Readiness probe — checks all components."""
    llm_ok = settings.is_llm_configured

    backend_ok = False
    try:
        backend_ok = await backend_api.health_check()
    except Exception:
        pass

    components = {
        "llm": llm_ok,
        "backend_api": backend_ok,
        "database": False,   # Module 10
        "rag": False,        # Module 6
    }

    all_critical_ready = llm_ok and backend_ok

    return ReadyResponse(
        ready=all_critical_ready,
        components=components,
    )


@app.post("/agent/chat", response_model=ChatResponse)
async def agent_chat(request: ChatRequest, fastapi_req: Request, background_tasks: BackgroundTasks):
    """
    Module 2: LangGraph Agent Chat Endpoint
    Accepts user message, runs the graph workflow, and returns the response.
    """
    from graph.workflow import agent_app
    from langchain_core.messages import HumanMessage, AIMessage
    from memory.memory_service import load_memory_context, save_interaction_context
    from memory.context_builder import build_memory_context

    # Module 15: Security Hardening
    from security.request_validator import validate_chat_request
    from security.auth_service import authenticate_request
    from security.rate_limit_service import check_rate_limit, increment_rate_limit
    from security.security_middleware import secure_message
    from background.event_dispatcher import dispatch_event
    from background.event_types import EVENT_TYPES
    
    # 1. Request Size Check (can also be handled by middleware, but handled here for completeness)
    if fastapi_req.headers.get("content-length"):
        if int(fastapi_req.headers.get("content-length")) > settings.MAX_REQUEST_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="Payload Too Large")
            
    # 2. Validate Request
    is_valid, validation_msg = validate_chat_request(request.model_dump())
    if not is_valid:
        raise HTTPException(status_code=400, detail=validation_msg)
        
    # 3. Auth Check
    auth_header = fastapi_req.headers.get("Authorization")
    api_key_header = fastapi_req.headers.get("X-API-Key")
    auth_result = authenticate_request(auth_header, api_key_header)
    if not auth_result["authenticated"]:
        if settings.ENABLE_EVENT_NOTIFICATIONS:
            dispatch_event(EVENT_TYPES["AUTH_FAILURE"], {"ip": fastapi_req.client.host})
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    # 4. Rate Limit Check
    identifier = request.farmer_id or fastapi_req.client.host
    if not check_rate_limit(identifier):
        if settings.ENABLE_EVENT_NOTIFICATIONS:
            dispatch_event(EVENT_TYPES["RATE_LIMIT_EXCEEDED"], {"identifier": identifier})
        raise HTTPException(status_code=429, detail="Too Many Requests")
    increment_rate_limit(identifier)
    
    # 5. Sanitize, Mask, and Check Injection
    sec_res = secure_message(request.message)
    if sec_res["prompt_injection_detected"]:
        if settings.ENABLE_EVENT_NOTIFICATIONS:
            dispatch_event(EVENT_TYPES["PROMPT_INJECTION_ATTEMPT"], {"farmer_id": request.farmer_id})
        return ChatResponse(
            reply="Your message violates security policies.",
            intent="unknown",
            agent_used="none",
            interaction_id="",
            is_fallback=True,
            metadata={"request_blocked": True, "prompt_injection_detected": True}
        )
        
    safe_message = sec_res["sanitized_message"]

    messages = []
    for turn in request.conversation_history:
        if turn.role == "user":
            messages.append(HumanMessage(content=turn.text))
        else:
            messages.append(AIMessage(content=turn.text))
            
    messages.append(HumanMessage(content=safe_message))
    
    
    # Module 10: Load Context
    farmer_id = request.farmer_id
    memory_ctx_data = {"profile": {}, "history": []}
    memory_built = {}
    
    if settings.ENABLE_MEMORY and farmer_id:
        memory_ctx_data = load_memory_context(farmer_id)
        if settings.ENABLE_HISTORY_CONTEXT or settings.ENABLE_PROFILE_ENRICHMENT:
            memory_built = build_memory_context(
                memory_ctx_data.get("profile", {}),
                memory_ctx_data.get("history", [])
            )
            
    initial_state = {
        "farmer_id": request.farmer_id,
        "language": request.language,
        "messages": messages,
        "intent": None,
        "agent_used": None,
        "final_response": None,
        "cards": [],
        "is_fallback": False,
        "context_used": {},
        "metadata": {},
        "farmer_profile": memory_ctx_data.get("profile"),
        "chat_history": memory_ctx_data.get("history"),
        "memory_context": memory_built,
        "profile_loaded": bool(memory_ctx_data.get("profile")),
        "history_loaded": bool(memory_ctx_data.get("history")),
        "mongo_connected": memory_ctx_data.get("mongo_connected", False),
        "memory_source": memory_ctx_data.get("memory_source", "none"),
        "persistence_success": False,
        "response_score": None,
        "feedback_received": False,
        "feedback_type": "",
        "hindsight_status": "pending",
        "telemetry_event_id": "",
        "response_quality": "",
        "background_tasks_scheduled": False,
        "background_task_ids": [],
        "async_persistence_enabled": settings.ENABLE_ASYNC_PERSISTENCE,
        "async_telemetry_enabled": settings.ENABLE_ASYNC_TELEMETRY,
        "event_dispatch_status": "none",
        "authenticated": auth_result["authenticated"],
        "auth_type": auth_result["auth_type"],
        "rate_limit_remaining": 0,
        "pii_detected": sec_res["pii_detected"],
        "prompt_injection_detected": sec_res["prompt_injection_detected"],
        "request_blocked": sec_res["blocked"],
        "security_flags": [k for k, v in sec_res.items() if v and isinstance(v, bool)]
    }
    
    try:
        final_state = agent_app.invoke(initial_state)
        
        # Build metadata with memory flags
        final_metadata = final_state.get("metadata", {})
        final_metadata["profile_loaded"] = bool(memory_ctx_data.get("profile"))
        final_metadata["history_loaded"] = bool(memory_ctx_data.get("history"))
        final_metadata["mongo_connected"] = memory_ctx_data.get("mongo_connected", False)
        final_metadata["memory_source"] = memory_ctx_data.get("memory_source", "none")
        if memory_ctx_data.get("profile", {}).get("location"):
            final_metadata["farmer_location"] = memory_ctx_data["profile"]["location"]
            
        # Module 10/11: Save interaction
        persistence_success = False
        if settings.ENABLE_MEMORY and farmer_id:
            persistence_success = save_interaction_context(farmer_id, final_state, final_state)
            
        final_metadata["persistence_success"] = persistence_success
            
        # Module 12: Telemetry
        from telemetry.telemetry_service import record_telemetry_event, record_hindsight_placeholder
        telemetry_event = record_telemetry_event(final_state, final_state)
        record_hindsight_placeholder(final_state, final_state, telemetry_event)
        
        interaction_id = telemetry_event.get("interaction_id")
        final_metadata["response_score"] = telemetry_event.get("response_score")
        final_metadata["response_quality"] = telemetry_event.get("response_quality")
            
        # Module 13: Background Tasks
        from background.task_manager import schedule_task
        from background.persistence_tasks import persist_memory_context_task
        from background.telemetry_tasks import record_telemetry_task, record_hindsight_task
        from background.event_dispatcher import dispatch_event
        from background.event_types import EVENT_TYPES
        
        task_ids = []
        
        if settings.ENABLE_BACKGROUND_TASKS:
            if settings.ENABLE_ASYNC_PERSISTENCE and settings.ENABLE_MEMORY and farmer_id:
                tid = schedule_task(background_tasks, "persist_memory", persist_memory_context_task, farmer_id, final_state, final_state)
                if tid: task_ids.append(tid)
                
            if settings.ENABLE_ASYNC_TELEMETRY:
                tid1 = schedule_task(background_tasks, "record_telemetry", record_telemetry_task, telemetry_event)
                tid2 = schedule_task(background_tasks, "record_hindsight", record_hindsight_task, placeholder)
                if tid1: task_ids.append(tid1)
                if tid2: task_ids.append(tid2)
                
            if settings.ENABLE_EVENT_NOTIFICATIONS:
                if final_metadata.get("requires_escalation"):
                    schedule_task(background_tasks, "dispatch_escalation", dispatch_event, EVENT_TYPES["ESCALATION_REQUIRED"], {"interaction_id": interaction_id, "farmer_id": farmer_id})
                if final_metadata.get("response_score", 1.0) < settings.LOW_CONFIDENCE_SCORE_THRESHOLD:
                    schedule_task(background_tasks, "dispatch_low_confidence", dispatch_event, EVENT_TYPES["LOW_CONFIDENCE_ALERT"], {"interaction_id": interaction_id, "farmer_id": farmer_id, "score": final_metadata.get("response_score")})
                if telemetry_event.get("low_quality", False):
                    schedule_task(background_tasks, "dispatch_low_quality", dispatch_event, EVENT_TYPES["LOW_QUALITY_RESPONSE"], {"interaction_id": interaction_id, "farmer_id": farmer_id, "score": final_metadata.get("response_score")})
                    
        final_metadata["background_tasks_scheduled"] = len(task_ids) > 0
        final_metadata["background_task_ids"] = task_ids
        final_metadata["event_dispatch_status"] = "scheduled" if settings.ENABLE_EVENT_NOTIFICATIONS and len(task_ids) > 0 else "none"
        final_metadata["low_quality"] = telemetry_event.get("low_quality", False)
        final_metadata["rag_score"] = telemetry_event.get("rag_score", 0.0)

        final_response_obj = ChatResponse(
            reply=final_state.get("final_response") or "Sorry, I could not process your request.",
            intent=final_state.get("intent") or "unknown",
            agent_used=final_state.get("agent_used") or "none",
            interaction_id=interaction_id,
            tools_used=final_state.get("tools_used") or [],
            cards=final_state.get("cards") or [],
            is_fallback=final_state.get("is_fallback") or False,
            context_used=final_state.get("context_used") or {},
            metadata=final_metadata
        )
        
        return final_response_obj
    except Exception as e:
        log.error(f"Graph execution failed: {e}")
        return ChatResponse(
            reply="I'm sorry, I encountered an internal error processing your request.",
            intent="unknown",
            agent_used="none",
            is_fallback=True
        )

@app.post("/auth/token")
async def login_for_access_token(request: AuthRequest):
    from security.jwt_service import create_access_token
    token = create_access_token(request.model_dump())
    return {"access_token": token, "token_type": "bearer"}

@app.post("/feedback")
async def submit_feedback_endpoint(request: FeedbackRequest, background_tasks: BackgroundTasks):
    from services.feedback_service import submit_feedback
    from background.task_manager import schedule_task
    from background.telemetry_tasks import save_feedback_task
    from background.event_dispatcher import dispatch_event
    from background.event_types import EVENT_TYPES
    
    success = submit_feedback(request.model_dump())
    if not success and not settings.ENABLE_ASYNC_FEEDBACK:
        raise HTTPException(status_code=500, detail="Failed to save feedback")
        
    if settings.ENABLE_ASYNC_FEEDBACK and settings.ENABLE_BACKGROUND_TASKS:
        schedule_task(background_tasks, "save_feedback", save_feedback_task, request.model_dump())
        
    if settings.ENABLE_EVENT_NOTIFICATIONS and settings.ENABLE_BACKGROUND_TASKS:
        schedule_task(background_tasks, "dispatch_feedback", dispatch_event, EVENT_TYPES["NEW_FEEDBACK"], request.model_dump())
        
    return {"status": "success"}

@app.post("/hindsight")
async def submit_hindsight_endpoint(request: HindsightRequest, background_tasks: BackgroundTasks):
    from services.hindsight_service import submit_hindsight_log
    from background.task_manager import schedule_task
    from background.telemetry_tasks import save_hindsight_log_task
    from background.event_dispatcher import dispatch_event
    from background.event_types import EVENT_TYPES
    
    success = submit_hindsight_log(request.model_dump())
    if not success and not settings.ENABLE_ASYNC_TELEMETRY:
        raise HTTPException(status_code=500, detail="Failed to save hindsight log")
        
    if settings.ENABLE_ASYNC_TELEMETRY and settings.ENABLE_BACKGROUND_TASKS:
        schedule_task(background_tasks, "save_hindsight", save_hindsight_log_task, request.model_dump())
        
    if settings.ENABLE_EVENT_NOTIFICATIONS and settings.ENABLE_BACKGROUND_TASKS:
        schedule_task(background_tasks, "dispatch_hindsight", dispatch_event, EVENT_TYPES["NEW_HINDSIGHT"], request.model_dump())
        
    return {"status": "success"}

@app.get("/feedback/{interaction_id}")
async def get_feedback_endpoint(interaction_id: str):
    from services.feedback_service import get_feedback_summary
    return get_feedback_summary(interaction_id)

@app.get("/hindsight/{interaction_id}")
async def get_hindsight_endpoint(interaction_id: str):
    from services.hindsight_service import get_hindsight_summary
    return get_hindsight_summary(interaction_id)

@app.get("/evaluation/run")
async def run_evaluation_endpoint(background_tasks: BackgroundTasks):
    if not settings.ENABLE_EVALUATION_FRAMEWORK:
        return {"status": "disabled", "message": "Evaluation framework is disabled"}
        
    from evaluation.evaluation_runner import run_golden_dataset_evaluation
    # For now, just run it inline so we get the result. 
    # In production, this might be a background task if it takes a long time.
    report = run_golden_dataset_evaluation()
    
    # If it failed, dispatch EVALUATION_FAILURE
    if report.get("overall_pass_rate", 1.0) < 0.8: # Example threshold
        from background.task_manager import schedule_task
        from background.event_dispatcher import dispatch_event
        from background.event_types import EVENT_TYPES
        schedule_task(background_tasks, "dispatch_eval_fail", dispatch_event, EVENT_TYPES["EVALUATION_FAILURE"], {"pass_rate": report.get("overall_pass_rate")})
        
    return {"status": "success", "report": report}

@app.get("/evaluation/report/latest")
async def get_latest_evaluation_report():
    import os, json
    if not settings.ENABLE_EVALUATION_FRAMEWORK:
        return {"status": "disabled"}
        
    reports_dir = settings.EVALUATION_REPORTS_DIR
    if not os.path.exists(reports_dir):
        return {"status": "not_found", "message": "No reports generated yet"}
        
    files = [f for f in os.listdir(reports_dir) if f.startswith("golden_eval_")]
    if not files:
        return {"status": "not_found", "message": "No reports generated yet"}
        
    latest_file = max(files)
    path = os.path.join(reports_dir, latest_file)
    with open(path, "r", encoding="utf-8") as f:
        report = json.load(f)
    return report

@app.get("/evaluation/analytics")
async def run_analytics_endpoint():
    if not settings.ENABLE_EVALUATION_FRAMEWORK:
        return {"status": "disabled", "message": "Evaluation framework is disabled"}
        
    from evaluation.evaluation_runner import run_historical_telemetry_analysis
    summary = run_historical_telemetry_analysis()
    return {"status": "success", "summary": summary}

# ── Main ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    log.info(f"[MAIN] Starting server on port {settings.PORT}...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
    )
