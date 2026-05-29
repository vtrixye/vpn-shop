from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

def cryptopay_invoice(url: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Оплатить 100₽", icon_custom_emoji_id="5258513401784573443", url=url),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()
