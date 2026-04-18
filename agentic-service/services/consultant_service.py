from config import settings

def get_consultant_details(consultant_type: str) -> dict:
    if consultant_type == "Plant Pathologist":
        contact_recommendation = "Please contact your nearest agriculture university or plant disease expert."
    elif consultant_type == "Market Advisor":
        contact_recommendation = "Please contact your local mandi secretary or market advisor."
    else:
        contact_recommendation = "Please contact your local agriculture officer."
        
    return {
        "consultant_type": consultant_type,
        "contact_recommendation": contact_recommendation,
        "escalation_target": settings.DEFAULT_ESCALATION_TARGET
    }
