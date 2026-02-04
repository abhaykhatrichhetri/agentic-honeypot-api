from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from detector import analyze_message

app = FastAPI()

API_KEY = "mysecretkey123"


# ---------- AUTH ----------
def verify_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# ---------- MODELS ----------
class IncomingMessage(BaseModel):
    sessionId: str
    message: dict
    conversationHistory: list = []
    metadata: dict = {}


class AnalyzeRequest(BaseModel):
    message: str


# ---------- ROOT HONEYPOT ENDPOINT ----------
@app.post("/")
def honeypot_root(data: IncomingMessage, auth=Depends(verify_key)):
    scam_text = data.message.get("text", "")

    result = analyze_message(scam_text)

    reply = "Why is my account being suspended?"

    if result["risk_level"] == "high":
        reply = "I am worried. What should I do now?"

    return {
        "status": "success",
        "reply": reply
    }


# ---------- ANALYZE ENDPOINT ----------
@app.post("/analyze")
def analyze_api(data: AnalyzeRequest, auth=Depends(verify_key)):
    return analyze_message(data.message)
