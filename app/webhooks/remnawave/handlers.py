import os
from remnawave.models.webhook import UserDto, NodeDto
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from aiogram.types import InputRichMessage

import telegram.keyboards.user as kb
from telegram.text import Text
from telegram import bot
from webhooks.remnawave import remnawave_handler
from utils.logger import get_logger
from database.crud import *
from database.models import User, Subscription

DEFAULT_SUB_USER_ID = os.getenv("DEFAULT_SUB_USER_ID")
ADMIN_GROUP_ID= int(os.getenv("ADMIN_GROUP_ID"))
logger = get_logger(__name__)
bot: Bot

@remnawave_handler("user.created")
async def user_created(session: AsyncSession, user: UserDto):
    sub = await create_sub(session=session, user=user)

@remnawave_handler("user.deleted")
async def user_deleted(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    if sub is None:
        return
    await session.delete(sub)
    await session.commit()
    logger.info(f"Удалена подписка {sub.username}")

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
    if sub is None:
        return
    sub.status = "DISABLED"
    await session.commit()

@remnawave_handler("user.enabled")
async def user_enabled(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    if sub is None:
        return
    sub.status = "ACTIVE"
    await session.commit()

@remnawave_handler("user.expired")
async def user_expired(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    if sub is None:
        return
    if sub.user_id != DEFAULT_SUB_USER_ID:
        text = Text.user_expired(sub)
        keyboard = kb.delete_button()
        await bot.send_rich_message(
            chat_id=sub.user_id,
            rich_message=InputRichMessage(markdown=text),
            reply_markup=keyboard
        )
    sub.status = "EXPIRED"
    await session.commit()

@remnawave_handler("user.expiration")
async def handle_expiration(session: AsyncSession, user: UserDto, meta: dict):
    offset = meta.get("expiration")
    logger.info(f"handling expiration {offset}")
    if offset is None or offset != -24:
        return
    if user.tag == "TRIAL":
        return
    
    sub = await session.get(Subscription, user.uuid)
    if sub is None:
        return
    
    if sub.user_id != DEFAULT_SUB_USER_ID:
        text = Text.user_expiration(sub, offset)
        keyboard = kb.delete_button()
        await bot.send_rich_message(
            chat_id=sub.user_id,
            rich_message=InputRichMessage(markdown=text),
            reply_markup=keyboard
        )

@remnawave_handler("user.expires_in_24_hours")
async def user_expires_in_24_hours(session: AsyncSession, user: UserDto):
    if user.tag == "TRIAL":
        return
    sub = await session.get(Subscription, user.uuid)
    if sub is None:
        return
    if sub.user_id != DEFAULT_SUB_USER_ID:
        text = Text.user_expires_in_24_hours(sub)
        keyboard = kb.delete_button()
        await bot.send_rich_message(
            chat_id=sub.user_id,
            rich_message=InputRichMessage(markdown=text),
            reply_markup=keyboard
        )

@remnawave_handler("node.connection_lost")
async def node_connection_lost(session: AsyncSession, node: NodeDto):
    text = Text.node_connection_lost(node)
    await bot.send_rich_message(
            chat_id=ADMIN_GROUP_ID,
            rich_message=InputRichMessage(markdown=text)
        )

@remnawave_handler("node.connection_restored")
async def node_connection_restored(session: AsyncSession, node: NodeDto):
    text = Text.node_connection_restored(node)
    await bot.send_rich_message(
            chat_id=ADMIN_GROUP_ID,
            rich_message=InputRichMessage(markdown=text)
        )