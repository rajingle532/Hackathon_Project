import json
import os
import datetime
from config import settings
import logging

log = logging.getLogger("report_builder")

def build_evaluation_report(results: list[dict]) -> dict:
    if not results:
        return {
            "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
            "overall_pass_rate": 0.0,
            "average_response_score": 0.0,
            "average_rag_score": 0.0,
            "top_failure_categories": [],
            "agent_breakdown": {}
        }
        
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    total_score = sum(r.get("response_score", 0.0) for r in results)
    total_rag = sum(r.get("rag_score", 0.0) for r in results)
    
    # Just a placeholder for agent_breakdown since simple results don't track agent yet in evaluation_service
    # We could extend results to include agent, but keeping it simple for now.
    
    return {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "overall_pass_rate": passed / total,
        "average_response_score": total_score / total,
        "average_rag_score": total_rag / total,
        "top_failure_categories": [],
        "agent_breakdown": {}
    }

def save_report(report: dict, report_name: str) -> str:
    try:
        if not os.path.exists(settings.EVALUATION_REPORTS_DIR):
            os.makedirs(settings.EVALUATION_REPORTS_DIR)
            
        path = os.path.join(settings.EVALUATION_REPORTS_DIR, report_name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return path
    except Exception as e:
        log.error(f"Error saving report: {e}")
        return ""
