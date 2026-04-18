import pytest
from telemetry.scoring_service import calculate_response_score, classify_response_quality

def test_calculate_response_score():
    score1 = calculate_response_score(0.9, False, ["tool1"], False)
    assert score1 == 0.9
    
    score2 = calculate_response_score(0.9, True, ["tool1"], False)
    assert score2 == 0.5  # 0.9 - 0.4
    
    score3 = calculate_response_score(0.9, False, ["tool1", "tool2"], False)
    assert score3 == 0.9 + 0.1  # tool bonus
    
    score4 = calculate_response_score(0.0, False, [], False)
    assert score4 == 0.5 # default
    
def test_classify_response_quality():
    assert classify_response_quality(0.85) == "high"
    assert classify_response_quality(0.65) == "medium"
    assert classify_response_quality(0.4) == "low"
