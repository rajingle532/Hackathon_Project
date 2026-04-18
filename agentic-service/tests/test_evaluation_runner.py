import pytest
from evaluation.evaluation_runner import run_golden_dataset_evaluation, run_historical_telemetry_analysis

def test_run_golden_dataset_evaluation(monkeypatch):
    monkeypatch.setattr("evaluation.evaluation_runner.load_all_datasets", lambda: {"test": [{"expected_intent": "test"}]})
    monkeypatch.setattr("evaluation.evaluation_runner.save_report", lambda *args: None)
    
    report = run_golden_dataset_evaluation()
    assert "overall_pass_rate" in report

def test_run_historical_telemetry_analysis(monkeypatch):
    monkeypatch.setattr("evaluation.evaluation_runner.collect_recent_telemetry", lambda x: [])
    monkeypatch.setattr("evaluation.evaluation_runner.collect_recent_feedback", lambda x: [])
    monkeypatch.setattr("evaluation.evaluation_runner.collect_recent_hindsight", lambda x: [])
    monkeypatch.setattr("evaluation.evaluation_runner.save_report", lambda *args: None)
    
    summary = run_historical_telemetry_analysis()
    assert "telemetry_summary" in summary
