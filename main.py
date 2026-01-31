from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from detector import analyze_message

app = FastAPI()

API_KEY = "mysecretkey123"  # same key you enter in GUVI tester

class MessageRequest(BaseModel):
    message: str

# ✅ GUVI-compatible authentication
def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/analyze")
def analyze(
    data: MessageRequest,
    api_key: str = Depends(verify_api_key)
):
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    return analyze_message(data.message)
