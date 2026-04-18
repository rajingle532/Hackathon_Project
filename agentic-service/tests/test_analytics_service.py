import pytest
from evaluation.analytics_service import summarize_telemetry, summarize_feedback, summarize_hindsight

def test_summarize_telemetry():
    events = [
        {"response_score": 0.8, "is_fallback": False, "agent_used": "disease"},
        {"response_score": 0.4, "is_fallback": True, "agent_used": "disease"}
    ]
    summary = summarize_telemetry(events)
    assert summary["total_events"] == 2
    assert summary["average_response_score"] == 0.6
    assert summary["fallback_frequency"] == 0.5
    assert "disease" in summary["agent_breakdown"]

def test_summarize_feedback():
    logs = [{"feedback_type": "thumbs_up"}, {"feedback_type": "thumbs_down"}]
    summary = summarize_feedback(logs)
    assert summary["total_feedback"] == 2
    assert summary["approval_ratio"] == 0.5

def test_summarize_hindsight():
    logs = [{"outcome_status": "successful"}]
    summary = summarize_hindsight(logs)
    assert summary["success_ratio"] == 1.0
