from fastapi import Request, APIRouter
from aiogram import types
from telegram.bot import bot, dp
from ..utils.logger import get_logger

logger = get_logger(__name__)
telegram_router = APIRouter(tags=["telegram"])

@telegram_router.post("/webhooks/telegram")
async def telegram_webhook(request: Request):
    try:
        update = types.Update.model_validate(await request.json())
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error"}