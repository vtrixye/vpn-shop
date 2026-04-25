from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Пользователи", callback_data="users_menu"),
        InlineKeyboardButton(text="Подписки", callback_data="subs_menu"),
        InlineKeyboardButton(text="Ноды", callback_data="nodes_menu"),
        InlineKeyboardButton(text="Назад", callback_data="main_menu")
    )

    return keyboard.as_markup()