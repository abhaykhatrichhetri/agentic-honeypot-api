from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests
import re

app = FastAPI()

API_KEY = "mysecretkey123"
GUVI_CALLBACK = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"


# --------------------
# Data Models
# --------------------

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int


class RequestBody(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: list = []
    metadata: dict = {}


# --------------------
# Helper Functions
# --------------------

def extract_intelligence(text: str):
    phones = re.findall(r"\+91\d{10}", text)
    upi = re.findall(r"\S+@\S+", text)
    urls = re.findall(r"https?://\S+", text)

    keywords = []
    for k in ["urgent", "verify", "account", "blocked", "otp", "upi"]:
        if k in text.lower():
            keywords.append(k)

    return {
        "bankAccounts": [],
        "upiIds": upi,
        "phishingLinks": urls,
        "phoneNumbers": phones,
        "suspiciousKeywords": keywords
    }


def send_callback(session_id, intelligence, total_msgs):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": total_msgs,
        "extractedIntelligence": intelligence,
        "agentNotes": "Scammer using urgency and verification pressure"
    }

    try:
        requests.post(GUVI_CALLBACK, json=payload, timeout=5)
    except:
        pass


# --------------------
# API Endpoint
# --------------------

@app.post("/")
def honeypot_api(data: RequestBody, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = data.message.text.lower()

    scam_keywords = ["account blocked", "verify", "urgent", "otp", "upi", "bank"]

    scam_detected = any(k in text for k in scam_keywords)

    if scam_detected:
        reply = "Why is my account being suspended?"
        intel = extract_intelligence(text)
        total_msgs = len(data.conversationHistory) + 1

        send_callback(data.sessionId, intel, total_msgs)

    else:
        reply = "Can you explain more?"

    return {
        "status": "success",
        "reply": reply
    }
