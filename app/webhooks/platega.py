import os
from fastapi import Request, APIRouter, Header, HTTPException

from utils.logger import get_logger
from services.platega_service import handling_webhook

logger = get_logger(__name__)
platega_router = APIRouter(tags=["platega"])

MERCHANT_ID = os.getenv("PLATEGA_MERCHANT_ID")
SECRET_KEY = os.getenv("PLATEGA_SECRET_KEY")

@platega_router.post("/webhooks/platega")
async def platega_webhook(
    request: Request,
    x_merchantid: str = Header(None),
    x_secret: str = Header(None),
    ):

    if x_merchantid != MERCHANT_ID or x_secret != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    body = await request.json()

    await handling_webhook(body)

    return {"status": "ok"}