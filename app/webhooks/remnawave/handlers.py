import os
from dotenv import load_dotenv
from remnawave.models.webhook import UserDto, NodeDto
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot

from telegram.text import Text
from telegram import bot
from webhooks.remnawave import remnawave_handler
from utils.logger import get_logger
from database.crud import *

load_dotenv()
DEFAULT_SUB_USER_ID = os.getenv("DEFAULT_SUB_USER_ID")
ADMIN_GROUP_ID= os.getenv("ADMIN_GROUP_ID")
logger = get_logger(__name__)
bot: Bot

@remnawave_handler("user.created")
async def user_created(session: AsyncSession, user: UserDto):
    await create_sub(session=session, user=user)

@remnawave_handler("user.modified")
async def user_modified(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    if sub is not None:
        await update_sub(session=session, user=user)
    else:
        await create_sub(session=session, user=user)

@remnawave_handler("user.disabled")
async def user_disabled(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    sub.status = "DISABLED"
    await session.commit()

@remnawave_handler("user.enabled")
async def user_enabled(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    sub.status = "ACTIVE"
    await session.commit()

@remnawave_handler("user.expired")
async def user_expired(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    if sub.user_id != DEFAULT_SUB_USER_ID:
        text = Text.user_expired()
        await bot.send_message(chat_id=sub.user_id, text=text)
    sub.status = "EXPIRED"
    await session.commit()

@remnawave_handler("user.expires_in_24_hours")
async def user_expires_in_24_hours(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    if sub.user_id != DEFAULT_SUB_USER_ID:
        text = Text.user_expires_in_24_hours()
        await bot.send_message(chat_id=sub.user_id, text=text)
    sub.status = "EXPIRED"
    await session.commit()

@remnawave_handler("node.connection_lost")
async def node_connection_lost(node: NodeDto):
    text = Text.node_connection_lost(node)
    await bot.send_message(chat_id=ADMIN_GROUP_ID, text=text)

@remnawave_handler("node.connection_restored")
async def node_connection_lost(node: NodeDto):
    text = Text.node_connection_restored(node)
    await bot.send_message(chat_id=ADMIN_GROUP_ID, text=text)