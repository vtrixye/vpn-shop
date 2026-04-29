from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Пользователи", icon_custom_emoji_id="5258513401784573443", callback_data="users_control"),
        InlineKeyboardButton(text="Подписки", icon_custom_emoji_id="5257965174979042426", callback_data="subs_control"),
        InlineKeyboardButton(text="Ноды", icon_custom_emoji_id="5879585266426973039", callback_data="nodes_control"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1, 1, 1, 1)
    return keyboard.as_markup()

def subs_control() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Обновить", icon_custom_emoji_id="5258420634785947640", callback_data="subs_control"),
        InlineKeyboardButton(text="Создать подписку", icon_custom_emoji_id="5274008024585871702", callback_data="sub_create"),
        InlineKeyboardButton(text="Поиск", icon_custom_emoji_id="5874960879434338403", callback_data="sub_search"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="admin_menu")
    )
    keyboard.adjust(1, 1, 1, 1)
    return keyboard.as_markup()

def sub_create() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Готово", icon_custom_emoji_id="5260416304224936047", callback_data="sub_ready"),
        InlineKeyboardButton(text="username", icon_custom_emoji_id="5814247475141153332", callback_data="set_username"),
        InlineKeyboardButton(text="Истекает через", icon_custom_emoji_id="5776213190387961618", callback_data="set_expire_at"),
        InlineKeyboardButton(text="Устройства", icon_custom_emoji_id="5877318502947229960", callback_data="set_hwid"),
        InlineKeyboardButton(text="Владелец", icon_custom_emoji_id="5879770735999717115", callback_data="set_telegram"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="subs_control")
    )
    keyboard.adjust(1, 1, 1, 1, 1, 1)
    return keyboard.as_markup()

def set_username() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Отмена", icon_custom_emoji_id="5258236805890710909", callback_data="sub_create_state")
    )

    return keyboard.as_markup()