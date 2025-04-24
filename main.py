import os
import hmac
import hashlib
from typing import Optional

from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "<votre_secret>")

def verify_signature(raw_body: bytes, signature_header: str):
    sha_name, signature = signature_header.split("=", 1)
    if sha_name not in ("sha1", "sha256"):
        return False
    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=raw_body,
        digestmod=getattr(hashlib, sha_name)
    )
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.post("/webhook")
async def github_webhook(
    request: Request,
    x_hub_signature: str = Header(None),
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None),
):
    body = await request.body()
    sig = x_hub_signature_256 or x_hub_signature
    if not sig or not verify_signature(body, sig):
        raise HTTPException(status_code=401, detail="Invalid signature")
    payload = await request.json()
    if x_github_event == "ping":
        return {"msg": "pong"}
    if x_github_event == "installation":
        action = payload.get("action")
        return {"msg": f"Installation event received: {action}"}
    return {"msg": f"Event {x_github_event} received"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}
