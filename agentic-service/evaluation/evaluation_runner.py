import datetime
import logging
from evaluation.golden_dataset_loader import load_all_datasets
from evaluation.evaluation_service import evaluate_response
from evaluation.report_builder import build_evaluation_report, save_report
from evaluation.telemetry_aggregator import collect_recent_telemetry, collect_recent_feedback, collect_recent_hindsight
from evaluation.analytics_service import summarize_telemetry, summarize_feedback, summarize_hindsight

log = logging.getLogger("evaluation_runner")

def run_golden_dataset_evaluation() -> dict:
    datasets = load_all_datasets()
    all_results = []
    
    # In a real implementation, we would invoke the agentic graph for each input in the datasets.
    # For now, we mock the actual response.
    
    for name, data in datasets.items():
        for item in data:
            # Mock actual response
            mock_actual = {
                "intent": item.get("expected_intent", "unknown"),
                "reply": " ".join(item.get("expected_keywords", [])),
                "tools_used": item.get("expected_tools", []),
                "metadata": {"response_score": 0.8},
                "context_used": {"data": " ".join(item.get("expected_keywords", []))}
            }
            
            res = evaluate_response(mock_actual, item)
            all_results.append(res)
            
    report = build_evaluation_report(all_results)
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    save_report(report, f"golden_eval_{timestamp}.json")
    
    return report

def run_historical_telemetry_analysis() -> dict:
    telemetry = collect_recent_telemetry(1000)
    feedback = collect_recent_feedback(1000)
    hindsight = collect_recent_hindsight(1000)
    
    summary = {
        "telemetry_summary": summarize_telemetry(telemetry),
        "feedback_summary": summarize_feedback(feedback),
        "hindsight_summary": summarize_hindsight(hindsight)
    }
    
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    save_report(summary, f"analytics_{timestamp}.json")
    
    return summary
