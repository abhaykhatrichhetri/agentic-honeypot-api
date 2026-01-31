import re

def analyze_message(message: str):
    text = message.lower()

    phone_numbers = re.findall(r"\b\d{10}\b", message)
    urls = re.findall(r"https?://\S+", message)
    emails = re.findall(r"\S+@\S+", message)

    keywords = []
    scam_type = "unknown"
    risk = "low"
    confidence = 0.4
    explanation = "No strong scam indicators detected."

    # Sensitive data request keywords (NEW)
    sensitive_data_words = [
        "upi", "bank", "account", "otp",
        "id proof", "aadhar", "pan",
        "address", "contact details", "contact",
        "gmail", "email"
    ]

    # Lottery / prize scam
    if any(word in text for word in ["lottery", "won", "winner", "prize", "win"]):
        scam_type = "lottery_fraud"
        keywords.extend(["lottery", "winning"])
        risk = "high"
        confidence = 0.9
        explanation = "Message promises a prize or winnings, a common scam pattern."

    # Job scam
    elif any(word in text for word in ["job offer", "work from home", "salary", "hiring"]):
        scam_type = "job_scam"
        keywords.extend(["job", "salary"])
        risk = "medium"
        confidence = 0.7
        explanation = "Message offers a job with vague details, often used in job scams."

    # Loan scam
    elif any(word in text for word in ["loan", "credit", "approved", "instant"]):
        scam_type = "loan_scam"
        keywords.extend(["loan", "credit"])
        risk = "medium"
        confidence = 0.75
        explanation = "Message talks about instant or guaranteed loans, common in financial fraud."

    # Sensitive information request increases risk (NEW FIX)
    if any(word in text for word in sensitive_data_words):
        risk = "high"
        keywords.append("personal_data_request")
        confidence = min(confidence + 0.2, 0.95)
        explanation = "Message requests sensitive personal information, a strong scam indicator."

    # Urgency increases risk
    if any(word in text for word in ["urgent", "immediately", "act now"]):
        risk = "high"
        keywords.append("urgency")
        confidence = min(confidence + 0.1, 0.95)

    # Contact indicators increase confidence
    if phone_numbers or urls or emails:
        confidence = min(confidence + 0.1, 0.95)

    # Agentic recommended action
    if risk == "high":
        recommended_action = "report"
    elif risk == "medium":
        recommended_action = "monitor"
    else:
        recommended_action = "ignore"

    return {
        "scam_type": scam_type,
        "risk_level": risk,
        "recommended_action": recommended_action,
        "indicators": {
            "phone_numbers": phone_numbers,
            "urls": urls,
            "emails": emails,
            "keywords": list(set(keywords))
        },
        "confidence_score": round(confidence, 2),
        "explanation": explanation
    }
