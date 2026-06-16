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
        InlineKeyboardButton(text="username", icon_custom_emoji_id="5814247475141153332", callback_data="set:username"),
        InlineKeyboardButton(text="Истекает через", icon_custom_emoji_id="5776213190387961618", callback_data="set:expire_at"),
        InlineKeyboardButton(text="Устройства", icon_custom_emoji_id="5877318502947229960", callback_data="set:hwid"),
        InlineKeyboardButton(text="Владелец", icon_custom_emoji_id="5879770735999717115", callback_data="set:telegram"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="subs_control")
    )
    keyboard.adjust(1, 1, 1, 1, 1, 1)
    return keyboard.as_markup()

def sub_editing(field_name: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    match field_name:
        case "expire_at":
            keyboard.add(
                InlineKeyboardButton(text="Месяц (30 дн)", callback_data="set:30", icon_custom_emoji_id="5258258882022612173"),
                InlineKeyboardButton(text="Квартал (90 дн)", callback_data="set:90", icon_custom_emoji_id="5258258882022612173"),
                InlineKeyboardButton(text="Год (365 дн)", callback_data="set:365", icon_custom_emoji_id="5258258882022612173")
            )
            keyboard.adjust(2, 1)
            
        case "hwid":
            keyboard.add(
                InlineKeyboardButton(text="1", callback_data="set:1", icon_custom_emoji_id="5877318502947229960"),
                InlineKeyboardButton(text="2", callback_data="set:2", icon_custom_emoji_id="5877318502947229960"),
                InlineKeyboardButton(text="3", callback_data="set:3", icon_custom_emoji_id="5877318502947229960")
            )
            keyboard.adjust(3)
            
        case "username":
           keyboard.add(
                InlineKeyboardButton(text="Случайный", callback_data="set:random", icon_custom_emoji_id="5350314303352223876")
            )
        case "telegram":
            keyboard.add(
                InlineKeyboardButton(text="По умолчанию", callback_data="set:def", icon_custom_emoji_id="5258096772776991776")
            )

    keyboard.row(
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="sub_create")
    )

    return keyboard.as_markup()