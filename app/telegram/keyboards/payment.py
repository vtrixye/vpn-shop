from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

def cryptopay_invoice(url: str, amount: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text=f"Оплатить {amount}₽", icon_custom_emoji_id="5258513401784573443", url=url),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()

def invoice_paid() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

def top_up() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="100₽", callback_data="top_up_100"),
        InlineKeyboardButton(text="200₽", callback_data="top_up_200"),
        InlineKeyboardButton(text="300₽", callback_data="top_up_300"),
        InlineKeyboardButton(text="500₽", callback_data="top_up_500"),
        InlineKeyboardButton(text="Назад", callback_data="profile")
    )

    keyboard.adjust(2, 2, 1)

    return keyboard.as_markup()

def payment(back: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Yookassa", icon_custom_emoji_id="5260416304224936047", callback_data="crypto"),
        InlineKeyboardButton(text="CryptoBot", icon_custom_emoji_id="5260416304224936047", callback_data="crypto"),
        InlineKeyboardButton(text="Telegram Stars", icon_custom_emoji_id="5260416304224936047", callback_data="pay_stars"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5260416304224936047", callback_data=back),
    )

    keyboard.adjust(1, 1, 1, 1)
    
    return keyboard.as_markup()

def pay_stars(price: int, invoice_link: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=f"Pay {price}⭐️",url=invoice_link, icon_custom_emoji_id="5260416304224936047"),
        InlineKeyboardButton(text="Назад", callback_data="top_up", icon_custom_emoji_id="5260416304224936047")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

