from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional, Dict, Any
from detector import analyze_message

app = FastAPI()

# ================================
# CONFIG
# ================================

API_KEY = "mysecretkey123"
api_key_header = APIKeyHeader(name="x-api-key")

# ================================
# AUTH
# ================================

def verify_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ================================
# MODELS (Judge Payload)
# ================================

class ScamMessage(BaseModel):
    sender: str
    text: str
    timestamp: Optional[int] = None

class JudgeRequest(BaseModel):
    sessionId: Optional[str] = None
    message: ScamMessage
    conversationHistory: Optional[list] = []
    metadata: Optional[Dict[str, Any]] = {}

# ================================
# ROOT ENDPOINT (Tester)
# ================================

@app.post("/")
def honeypot_root(token: str = Depends(verify_key)):
    return {
        "status": "success",
        "reply": "Honeypot API is live and accessible"
    }

# ================================
# ANALYZE ENDPOINT (Judges)
# ================================

@app.post("/analyze")
def analyze_judge(data: JudgeRequest, token: str = Depends(verify_key)):
    text = data.message.text

    result = analyze_message(text)

    reply = "Why is my account being suspended?"

    if result["risk_level"] == "high":
        reply = "I am worried. What should I do now?"
    elif result["risk_level"] == "medium":
        reply = "Can you explain more about this?"
    else:
        reply = "Okay, noted."

    return {
        "status": "success",
        "reply": reply,
        "analysis": result
    }
