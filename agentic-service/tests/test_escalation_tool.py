import pytest
from tools.escalation_tool import escalation_needed, get_escalation_context

def test_escalation_needed():
    assert escalation_needed("disease", 0.9, "expert") == True
    assert escalation_needed("disease", 0.4, "normal text") == True
    assert escalation_needed("disease", 0.9, "normal text") == False

def test_get_escalation_context():
    ctx = get_escalation_context("disease", 0.4, "my crop is dying")
    assert ctx["requires_escalation"] == True
    assert ctx["consultant_type"] == "Plant Pathologist"
    assert "Low confidence" in ctx["escalation_reason"] or "Explicit consultant" in ctx["escalation_reason"]
    
    ctx2 = get_escalation_context("disease", 0.9, "normal")
    assert ctx2["requires_escalation"] == False
