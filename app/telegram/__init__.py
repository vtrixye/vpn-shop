import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from telegram.handlers import routers
from utils.logger import get_logger
from database import session_maker
from telegram.middlewares import DataBaseSession
from services.redis_service import get_redis

logger = get_logger(__name__)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp: Dispatcher = None

async def init_dispatcher():
    global dp

    redis_instance = get_redis()
    storage = RedisStorage(redis=redis_instance, key_builder=DefaultKeyBuilder(with_destiny=True))
    dp = Dispatcher(storage=storage)

    dp["redis"] = redis_instance

    for router in routers:
        dp.include_router(router)

    logger.info("Aiogram Dispatcher with Redis storage initialized successfully")

async def setup_middlewares():
    if dp is None:
        raise RuntimeError("Dispatcher is not initialized")
    dp.update.middleware(DataBaseSession(session_maker))
    logger.info("Bot middlewares configured")

async def setup_webhook():
    await bot.set_webhook(
        url=f"{os.getenv('BASE_URL')}{os.getenv('TELEGRAM_WEBHOOK_PATH')}",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logger.info("Telegram webhook set successfully")

async def shutdown_bot():
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Telegram cleaned up")