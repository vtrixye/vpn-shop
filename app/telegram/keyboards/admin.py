from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Авторассылка", icon_custom_emoji_id="5257965174979042426", callback_data="autosend"),
        InlineKeyboardButton(text="Статистика", icon_custom_emoji_id="5879585266426973039", callback_data="stats"),
        InlineKeyboardButton(text="Тест", icon_custom_emoji_id="5879585266426973039", callback_data="test"),        
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1, 1, 1, 1)
    return keyboard.as_markup()

def stats() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Пользователи", icon_custom_emoji_id="5258420634785947640", callback_data="users_stats"),
        InlineKeyboardButton(text="Подписки", icon_custom_emoji_id="5258420634785947640", callback_data="subs_stats"),
        InlineKeyboardButton(text="Ноды", icon_custom_emoji_id="5258420634785947640", callback_data="nodes_stats"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="admin_menu")
    )
    keyboard.adjust(1, 1, 1, 1)
    return keyboard.as_markup()

def subs_stats() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Обновить", icon_custom_emoji_id="5258420634785947640", callback_data="subs_stats"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="stats")
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()

def users_stats() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Обновить", icon_custom_emoji_id="5258420634785947640", callback_data="users_stats"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="stats")
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()

def test_payment(url: str):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Оплатить", icon_custom_emoji_id="5258420634785947640", url=url),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="admin_menu")
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()