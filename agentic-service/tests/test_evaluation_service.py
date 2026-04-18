import pytest
from evaluation.evaluation_service import evaluate_response

def test_evaluate_response_pass():
    actual = {
        "intent": "advisory",
        "tools_used": ["weather_tool"],
        "reply": "water your crops",
        "metadata": {"response_score": 0.8},
        "context_used": "water"
    }
    expected = {
        "expected_intent": "advisory",
        "expected_tools": ["weather_tool"],
        "expected_keywords": ["water"],
        "minimum_score": 0.7
    }
    res = evaluate_response(actual, expected)
    assert res["passed"] == True
    assert res["intent_match"] == True
    assert res["tool_match"] == True
    assert res["keyword_match_score"] == 1.0

def test_evaluate_response_fail_intent():
    actual = {"intent": "unknown", "metadata": {"response_score": 0.8}}
    expected = {"expected_intent": "advisory"}
    res = evaluate_response(actual, expected)
    assert res["passed"] == False
    assert res["intent_match"] == False
