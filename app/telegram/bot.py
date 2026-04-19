import os
from aiogram import Bot, Dispatcher
from handlers import routers
from utils.logger import get_logger

logger = get_logger(__name__)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

for router in routers:
    dp.include_router(router)

async def setup_middlewares():
    
    #middlewares

    logger.info("Bot middlewares configured")

async def setup_webhook():
    await bot.set_webhook(
        url=f"{os.getenv('BASE_URL')}{os.getenv('TELEGRAM_WEBHOOK_PATH')}",
        drop_pending_updates=True
    )
    logger.info("Telegram webhook set successfully")

async def shutdown_bot():
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Telegram cleaned up")