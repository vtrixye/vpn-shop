from fastapi import Request, APIRouter
from aiogram import types
import telegram
from utils.logger import get_logger

logger = get_logger(__name__)
telegram_router = APIRouter(tags=["telegram"])

@telegram_router.post("/webhooks/telegram")
async def telegram_webhook(request: Request):
    try:
        update = types.Update.model_validate(await request.json())
        await telegram.dp.feed_update(telegram.bot, update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error"}