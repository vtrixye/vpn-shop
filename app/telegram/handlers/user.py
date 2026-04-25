from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from telegram.filters import ChatTypeFilter, IsBlocked
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.users as kb

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']), IsBlocked())
user_router.callback_query.filter(ChatTypeFilter(['private']), IsBlocked())

@user_router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery, session: AsyncSession):
    text = Text.main_menu()
    keyboard = await kb.main_menu(session=session, id=callback.from_user.id)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()