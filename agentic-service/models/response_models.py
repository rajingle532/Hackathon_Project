"""
Agentic Service — Response Models
===================================
Pydantic models for API responses.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ChatResponse(BaseModel):
    """Response body for POST /agent/chat."""
    reply: str = Field(..., description="Agent's text response")
    intent: str = Field(default="unknown", description="Classified intent")
    agent_used: str = Field(default="none", description="Which agent handled this")
    interaction_id: Optional[str] = Field(default=None, description="Unique ID for this interaction")
    cards: List[Dict[str, Any]] = Field(default_factory=list, description="Structured info cards")
    tools_used: List[str] = Field(default_factory=list, description="Tools used during processing")
    is_fallback: bool = Field(default=False, description="True if fallback was used")
    context_used: Dict[str, Any] = Field(default_factory=dict, description="Context metadata")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional agent metadata")


class ComponentStatus(BaseModel):
    """Status of a single component."""
    healthy: bool
    message: str = ""


class HealthResponse(BaseModel):
    """Response body for GET /health."""
    status: str = "ok"
    service: str = ""
    version: str = ""
    llm_configured: bool = False
    backend_reachable: bool = False


class ReadyResponse(BaseModel):
    """Response body for GET /ready."""
    ready: bool = True
    components: Dict[str, bool] = Field(default_factory=dict)
