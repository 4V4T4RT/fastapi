from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def Healt():
    return {"status": "ok"}

    from fastapi import FastAPI, Request, HTTPException
import os, hmac, hashlib

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook")
async def github_webhook(request: Request):
    secret = os.getenv("GITHUB_APP_WEBHOOK_SECRET", "")
    if not secret:
        raise HTTPException(status_code=500, detail="Webhook secret not set")

    signature = request.headers.get("X-Hub-Signature-256", "")
    body = await request.body()

    mac = hmac.new(secret.encode(), body, hashlib.sha256)
    expected_sig = f"sha256={mac.hexdigest()}"
    if not hmac.compare_digest(expected_sig, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    event = request.headers.get("X-GitHub-Event", "unknown")

    print(f"Received GitHub event: {event}")
    print(payload)

    return {"status": "received", "event": event}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
    
    from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}
