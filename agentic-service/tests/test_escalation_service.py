import pytest
from services.escalation_prompt_service import build_escalation_prompt

def test_build_escalation_prompt():
    esc_ctx = {
        "escalation_reason": "Low confidence",
        "consultant_type": "Plant Pathologist",
        "escalation_target": "Local Department"
    }
    prev_ctx = {
        "agent_used": "disease_agent",
        "agent_confidence": 0.4
    }
    
    prompt = build_escalation_prompt("help", esc_ctx, prev_ctx)
    assert "help" in prompt
    assert "Low confidence" in prompt
    assert "Plant Pathologist" in prompt
    assert "disease_agent" in prompt
