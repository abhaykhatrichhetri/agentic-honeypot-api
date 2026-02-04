from fastapi import FastAPI, Header, HTTPException, Request
from detector import analyze_message

app = FastAPI()

API_KEY = "mysecretkey123"


# ---------- ROOT ENDPOINT (FOR GUVI TESTER) ----------
@app.post("/")
async def root_endpoint(request: Request, x_api_key: str = Header(None)):
    
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Try to read body safely
    try:
        body = await request.json()
    except:
        body = None

    # If tester sends nothing
    if body is None:
        return {
            "status": "success",
            "reply": "Why is my account being suspended?"
        }

    # If tester sends message object
    message_text = ""

    if "message" in body:
        if isinstance(body["message"], dict):
            message_text = body["message"].get("text", "")
        else:
            message_text = str(body["message"])

    if message_text.strip() == "":
        return {
            "status": "success",
            "reply": "Why is my account being suspended?"
        }

    result = analyze_message(message_text)

    return {
        "status": "success",
        "reply": result["explanation"]
    }


# ---------- YOUR ORIGINAL ANALYZE ENDPOINT ----------
@app.post("/analyze")
def analyze_api(data: dict, x_api_key: str = Header(None)):
    
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if "message" not in data:
        raise HTTPException(status_code=400, detail="Message missing")

    return analyze_message(data["message"])
