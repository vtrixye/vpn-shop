from webhooks.remnawave import remnawave_handler
from utils.logger import get_logger
from telegram import bot
from aiogram import Bot

bot: Bot

logger = get_logger(__name__)

@remnawave_handler("user.created")
async def user_created(data):
    logger.info("remnawave user_created")
    bot.send_message(chat_id=1253142390, text=f"Создан пользователь \n{data}")
