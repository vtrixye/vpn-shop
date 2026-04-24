from remnawave.models.webhook import UserDto, NodeDto

from webhooks.remnawave import remnawave_handler
from utils.logger import get_logger
from telegram import bot
from aiogram import Bot

bot: Bot

logger = get_logger(__name__)

@remnawave_handler("user.created")
async def user_created(user: UserDto):
    await bot.send_message(chat_id=1253142390, text=f"Создан пользователь \n{user}")

@remnawave_handler("user.modified")
async def user_modified(user: UserDto):
    await bot.send_message(chat_id=1253142390, text=f"Создан изменен \n{user}")

@remnawave_handler("user.disabled")
async def user_disabled(user: UserDto):
    await bot.send_message(chat_id=1253142390, text=f"Создан деактивирован \n{user}")

@remnawave_handler("user.enabled")
async def user_enabled(user: UserDto):
    await bot.send_message(chat_id=1253142390, text=f"Создан активирован \n{user}")