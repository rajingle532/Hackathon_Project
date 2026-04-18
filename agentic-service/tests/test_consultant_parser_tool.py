import pytest
from tools.consultant_parser_tool import consultant_requested, extract_consultant_type, extract_escalation_reason

def test_consultant_requested():
    assert consultant_requested("I want an expert") == True
    assert consultant_requested("urgent please") == True
    assert consultant_requested("what is the weather") == False

def test_extract_consultant_type():
    assert extract_consultant_type("disease") == "Plant Pathologist"
    assert extract_consultant_type("market") == "Market Advisor"
    assert extract_consultant_type("unknown") == "Agriculture Officer"

def test_extract_escalation_reason():
    assert extract_escalation_reason("expert help", 0.9, "general") == "Explicit consultant requested"
    assert extract_escalation_reason("hello", 0.4, "disease") == "Low confidence in disease advice"
