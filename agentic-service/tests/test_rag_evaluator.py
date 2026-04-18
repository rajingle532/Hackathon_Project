import pytest
from evaluation.rag_evaluator import evaluate_rag_quality

def test_evaluate_rag_quality():
    res = evaluate_rag_quality("The brown spots are early blight", ["brown spots", "blight", "fungicide"])
    assert res["rag_score"] == 2/3
    assert "blight" in res["matched_keywords"]
    assert "fungicide" in res["missing_keywords"]

def test_evaluate_rag_quality_empty():
    res = evaluate_rag_quality("", ["test"])
    assert res["rag_score"] == 0.0
