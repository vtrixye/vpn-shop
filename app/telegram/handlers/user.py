from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from telegram.filters import ChatTypeFilter, IsBlocked
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.user as kb
import services.remnawave_service.api as rw
from utils.logger import get_logger

logger = get_logger(__name__)

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']), IsBlocked())
user_router.callback_query.filter(ChatTypeFilter(['private']), IsBlocked())

@user_router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    text = Text.main_menu()
    keyboard = await kb.main_menu(session=session, id=callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)

@user_router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    text = await Text.profile(session, callback.from_user.id)
    keyboard = kb.profile()
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")

@user_router.callback_query(F.data == "my_subs")
async def my_subs(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    text = Text.my_subs()
    keyboard = await kb.my_subs(session=session, id=callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)

@user_router.callback_query(F.data == "trial_sub")
async def trial_sub(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    await rw.create_user(
        username="testhandler", expire_at=datetime.now() + timedelta(days=30), 
        telegram_id=callback.from_user.id, tag="TRIAL"
        )

    user = await session.get(User, callback.from_user.id)
    user.trial = False
    await session.commit()
    
    text = Text.trial_sub()
    keyboard = kb.trial_sub()
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")

@user_router.callback_query()
async def other(callback: CallbackQuery):
    return await callback.answer("В разработке", show_alert=True)
