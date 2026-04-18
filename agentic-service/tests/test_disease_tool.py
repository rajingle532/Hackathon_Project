import pytest
from tools.disease_tool import disease_needed, get_disease_context

def test_disease_needed():
    assert disease_needed("My crop has a fungus") == True
    assert disease_needed("There are spots on the leaves") == True
    assert disease_needed("How do I irrigate?") == False

def test_get_disease_context(monkeypatch):
    def mock_predict(*args, **kwargs):
        return {
            "disease_name": "Leaf Spot",
            "confidence": 0.8,
            "treatment": "Mock Treatment"
        }
    monkeypatch.setattr("tools.disease_tool.predict_crop_disease", mock_predict)
    
    ctx = get_disease_context("My leaves have spots")
    assert ctx["disease_name"] == "Leaf Spot"
    assert ctx["confidence"] == 0.8
    assert "spots" in ctx["symptoms_detected"]
    assert ctx["requires_escalation"] == False # Because 0.8 > 0.60
    
def test_get_disease_context_escalation(monkeypatch):
    def mock_predict(*args, **kwargs):
        return {
            "disease_name": "Unknown",
            "confidence": 0.4, # < 0.60
            "treatment": "Mock Treatment"
        }
    monkeypatch.setattr("tools.disease_tool.predict_crop_disease", mock_predict)
    ctx = get_disease_context("It looks bad")
    assert ctx["requires_escalation"] == True
