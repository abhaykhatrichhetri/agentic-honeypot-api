from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from detector import analyze_message

app = FastAPI()

API_KEY = "mysecretkey123"

class MessageRequest(BaseModel):
    message: str

# ✅ UNIVERSAL tester endpoint (GET + POST, NO BODY)
@app.api_route("/", methods=["GET", "POST"], include_in_schema=False)
def tester_endpoint(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "status": "ok",
        "message": "Honeypot API is live and accessible"
    }

# ✅ REAL evaluation endpoint (POST + BODY)
@app.post("/analyze")
def analyze(data: MessageRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    return analyze_message(data.message)
