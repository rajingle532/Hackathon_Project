"""
Agentic Service — Request Models
==================================
Pydantic models for incoming API requests.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ConversationTurn(BaseModel):
    """A single turn in conversation history."""
    role: str = Field(..., description="'user' or 'assistant'")
    text: str = Field(..., description="Message text")


class ChatRequest(BaseModel):
    """Request body for POST /agent/chat."""
    message: str = Field(..., min_length=1, description="User message")
    farmer_id: Optional[str] = Field(default=None, description="Farmer MongoDB ID")
    language: str = Field(default="English", description="User's preferred language")
    conversation_history: List[ConversationTurn] = Field(
        default_factory=list,
        description="Last N conversation turns for context",
    )


class HealthCheckRequest(BaseModel):
    """Optional request for detailed health check."""
    check_backend: bool = Field(default=True)
    check_llm: bool = Field(default=True)

class FeedbackRequest(BaseModel):
    interaction_id: str = Field(...)
    farmer_id: Optional[str] = Field(default=None)
    feedback_type: str = Field(...)
    feedback_reason: Optional[str] = Field(default=None)

class HindsightRequest(BaseModel):
    interaction_id: str = Field(...)
    farmer_id: Optional[str] = Field(default=None)
    outcome_status: str = Field(...)
    outcome_reason: Optional[str] = Field(default=None)

class AuthRequest(BaseModel):
    user_id: str = Field(...)
    role: str = Field(...)
