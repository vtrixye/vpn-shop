from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from telegram.filters import ChatTypeFilter, IsBlocked
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.user as kb
import services.remnawave_service.api as rw
from services.remnawave_service.enums import UsernameType, ExpireType
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
        username=UsernameType.TRIAL, expire_at=ExpireType.DAY,
        tag="TRIAL", telegram_id=callback.from_user.id
        )

    user = await session.get(User, callback.from_user.id)
    user.trial = False
    await session.commit()

    text = Text.trial_sub()
    keyboard = kb.trial_sub()
    await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")

@user_router.callback_query(F.data == "delete_message")
async def delete_message(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

@user_router.callback_query()
async def other(callback: CallbackQuery):
    return await callback.answer("В разработке", show_alert=True)
