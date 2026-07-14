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
    x_merchant_id: str = Header(None),
    x_secret: str = Header(None),
    ):

    headers = dict(request.headers)
    logger.info(f"Все заголовки: {headers}")

    body = await request.json()

    logger.info(f"Тело вебхука: {body}")

    logger.info(f"Webhook: {x_merchant_id} {x_secret}")
    if x_merchant_id != MERCHANT_ID or x_secret != SECRET_KEY:
        logger.info(f"Must be {MERCHANT_ID} {SECRET_KEY}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    


    await handling_webhook(body)

    return {"status": "ok"}