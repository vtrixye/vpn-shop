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

def test() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="test", url="happ://crypt4/Z1OOWHo/kMQcWcaxFY9ydf7Xrn1Npttxy8NMH/ibbj1Bez44PqmWamd+WVd2LbTVB4DCvylIoBmjz4VWFP4Noa9dFHmyaDEdc0/2lsKwj3s+8w5OfX6rLCwp7L/hxXmy9XA7Ei/w77XZlr8DR9BYtkfk7x8cl2VevLiA1Mgkx5U4gmc8Q1AXr9w1muDT5KJTkTfb6v1qnzzutDsgbrme1dWrTVB8Bwz+E02zfziTTvezslN61AmPp0Xp7MTLjKydexBipSooADXm9+1oOnghxC8VlABKFwCTkud4F8igQm9CX+3pE/2xB6dTe3OZcJY683lne0MAnu+bmhJkt4+MLAF40N8IG+9d0+e33pjpEV84EriB3O2m+JYvpR7JVw6aQrldPkkcHMG1MK+deke02/g843y7Qan3n8BmZsk23XWWepXxUyBU4EXbHyJljllPQdTjeSaW+YSOD8tA2cC0bbsOkWohkR6nNBp+sdWc3CVOl/SLmGzGouEQS9gOxe/Y+0pJziTvvHsQ2bW8BVyucodyDdRHR6SB3Epq6mEQ2rMI/3Uzxm0f0IgGHFcxvNrY0VIubpEeOoK5gLfqDoFEJ+dLpyKlUr0FEaifXUPIqO5uYEYXkOxrprGLjLI3/Ks/V+QW4ltn0IMibMxAfC5au9bwzpmOnuqMDFIkToW5OCc="))

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