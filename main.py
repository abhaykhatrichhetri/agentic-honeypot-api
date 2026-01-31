from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from detector import analyze_message

app = FastAPI()
security = HTTPBearer()

API_KEY = "mysecretkey123"   # change later if you want

class MessageRequest(BaseModel):
    message: str

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/analyze")
def analyze(data: MessageRequest, token: str = Depends(verify_token)):
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    return analyze_message(data.message)
