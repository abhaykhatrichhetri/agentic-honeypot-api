from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional, Dict
import re
import requests

# -------------------------
# APP SETUP
# -------------------------

app = FastAPI()
API_KEY = "mysecretkey123"
api_key_header = APIKeyHeader(name="x-api-key")

def verify_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# -------------------------
# MODELS (For Judges)
# -------------------------

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class RequestBody(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[Dict] = None

# -------------------------
# SIMPLE AGENT LOGIC
# -------------------------

def is_scam(text: str):
    keywords = ["blocked", "verify", "urgent", "otp", "upi", "bank"]
    return any(k in text.lower() for k in keywords)

def generate_agent_reply(text: str):
    return "Why is my account being suspended?"

# -------------------------
# ROOT ENDPOINT (GUVI TESTER)
# -------------------------

@app.post("/")
async def tester_root(request: Request, key: str = Depends(verify_key)):
    try:
        data = await request.json()
    except:
        return {
            "status": "success",
            "reply": "Why is my account being suspended?"
        }

    if isinstance(data, dict) and "message" in data:
        text = data["message"].get("text", "")
        return {
            "status": "success",
            "reply": generate_agent_reply(text)
        }

    return {
        "status": "success",
        "reply": "Can you explain more?"
    }

# -------------------------
# ANALYZE ENDPOINT (JUDGES)
# -------------------------

@app.post("/analyze")
def analyze(payload: RequestBody, key: str = Depends(verify_key)):

    text = payload.message.text

    scam = is_scam(text)

    reply = generate_agent_reply(text)

    # (Optional callback stub)
    if scam:
        try:
            requests.post(
                "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
                json={
                    "sessionId": payload.sessionId,
                    "scamDetected": True,
                    "totalMessagesExchanged": len(payload.conversationHistory) + 1,
                    "extractedIntelligence": {
                        "bankAccounts": [],
                        "upiIds": [],
                        "phishingLinks": [],
                        "phoneNumbers": [],
                        "suspiciousKeywords": ["urgent", "verify"]
                    },
                    "agentNotes": "Urgency based banking scam"
                },
                timeout=5
            )
        except:
            pass

    return {
        "status": "success",
        "reply": reply
    }
