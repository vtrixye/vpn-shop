from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Пользователи", icon_custom_emoji_id="5258513401784573443", callback_data="users_menu"),
        InlineKeyboardButton(text="Подписки", icon_custom_emoji_id="5257965174979042426", callback_data="subs_menu"),
        InlineKeyboardButton(text="Ноды", icon_custom_emoji_id="5879585266426973039", callback_data="nodes_menu"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1, 1, 1, 1)
    return keyboard.as_markup()