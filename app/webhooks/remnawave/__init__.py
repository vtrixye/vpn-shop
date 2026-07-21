import os
import json
import hmac
import hashlib
import inspect

from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from remnawave.models.webhook import WebhookPayloadDto, UserDto, NodeDto

from utils.logger import get_logger
from database import session_maker

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
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        has_meta = len(params) > 2
        logger.info(f"Registering {event_name}, has_meta={has_meta}")

        async def wrapper(data, meta: Optional[dict] = None):
            async with session_maker() as session:
                if has_meta:
                    logger.info("decorator wrapper meta")
                    return await func(session, data, meta)
                else:
                    return await func(session, data)
        
        remnawave_handler._handlers[event_name] = wrapper
        return wrapper
    return decorator

remnawave_handler._handlers = {}

def _to_dto(event: str, data: dict):
    if event.startswith("user."):
        return UserDto(**data)
    if event.startswith("node."):
        return NodeDto(**data)
    return data

@remnawave_router.post("")
async def remnawave_webhook(payload=Depends(validate_webhook)):
    event = payload.get("event")
    if not event:
        logger.warning("Webhook without event")
        return {"ok": False}

    handler = remnawave_handler._handlers.get(event)
    logger.info(f"Webhook event: {event}, handler found: {handler is not None}")
    if not handler:
        return {"ok": True}
    
    try:
        parsed = WebhookPayloadDto(**payload)
        meta = payload.get("meta")
        logger.info(f"meta received: {meta}")
        typed_data = _to_dto(event, parsed.data)
        await handler(typed_data, meta)
    except Exception:
        logger.exception(f"Error handling event: {event}")
        return {"ok": True}

    return {"ok": True}