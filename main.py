from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from detector import analyze_message

app = FastAPI()

# API key setup (matches tester)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
API_KEY = "mysecretkey123"

class MessageRequest(BaseModel):
    message: str | None = None

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

#  ROOT endpoint → tester ping
@app.post("/")
def root(token: str = Depends(verify_api_key)):
    return {
        "status": "ok",
        "message": "Honeypot API is live and accessible"
    }

#  ANALYZE endpoint → real evaluation
@app.post("/analyze")
def analyze(data: MessageRequest, token: str = Depends(verify_api_key)):
    if not data.message:
        # tester sends no body → respond safely
        return {
            "status": "ok",
            "note": "Endpoint reachable. No message provided."
        }

    return analyze_message(data.message)
