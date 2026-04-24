import os
import json
import hmac
import hashlib

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, HTTPException
from remnawave.models.webhook import WebhookPayloadDto
from remnawave.controllers.webhooks import WebhookUtility

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

WEBHOOK_SECRET = os.getenv("REMNAWAVE_WEBHOOK_SECRET")

if not WEBHOOK_SECRET:
    raise RuntimeError("REMNAWAVE_WEBHOOK_SECRET is not set")

async def validate_webhook(request: Request):
    signature = request.headers.get("X-Remnawave-Signature")

    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")

    try:
        body = await request.json()

        original_body = json.dumps(body, separators=(",", ":"))

        computed_signature = hmac.new(
            WEBHOOK_SECRET.encode("utf-8"),
            original_body.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(computed_signature, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

    except HTTPException:
        raise
    except Exception:
        logger.exception("Webhook validation failed")
        raise HTTPException(status_code=400, detail="Invalid webhook")
    
    return body

remnawave_router = APIRouter(
    prefix="/webhooks/remnawave",
    tags=["remnawave"]
)

def remnawave_handler(event_name: str):
    def decorator(func):
        remnawave_handler._handlers[event_name] = func
        return func
    return decorator

remnawave_handler._handlers = {}

@remnawave_router.post("")
async def remnawave_webhook(payload=Depends(validate_webhook)):
    event = payload.get("event")

    if not event:
        logger.warning("Webhook without event", extra={"payload": payload})
        return {"ok": False}

    handler = remnawave_handler._handlers.get(event)

    if not handler:
        return {"ok": True}
    
    try:
        parsed = WebhookPayloadDto(**payload)
        typed_data = WebhookUtility.get_typed_data(parsed)
        await handler(typed_data)
    except Exception:
        logger.exception(f"Error handling event: {event}")
        return {"ok": True}

    return {"ok": True}