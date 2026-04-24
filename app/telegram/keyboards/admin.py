from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Пользователи", callback_data="users"),
        InlineKeyboardButton(text="Ноды", callback_data="nodes")
    )

    return keyboard.as_markup()