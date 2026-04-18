import pytest
from evaluation.report_builder import build_evaluation_report, save_report

def test_build_evaluation_report():
    results = [
        {"passed": True, "response_score": 0.8, "rag_score": 0.6},
        {"passed": False, "response_score": 0.4, "rag_score": 0.2}
    ]
    report = build_evaluation_report(results)
    assert report["overall_pass_rate"] == 0.5
    assert report["average_response_score"] == 0.6
    assert report["average_rag_score"] == 0.4

def test_save_report(monkeypatch):
    monkeypatch.setattr("os.path.exists", lambda path: True)
    
    # Mock open
    class MockFile:
        def write(self, data): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        
    import builtins
    monkeypatch.setattr(builtins, "open", lambda *args, **kwargs: MockFile())
    
    path = save_report({"test": 1}, "test.json")
    assert "test.json" in path
