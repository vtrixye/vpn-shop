from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User, Subscription
from utils.time import get_remaining_time

async def main_menu(session: AsyncSession, id: int) -> InlineKeyboardMarkup:
    user = await session.get(User, id)
    keyboard = InlineKeyboardBuilder()
    
    if user.trial:
        keyboard.row(InlineKeyboardButton(text="Пробный период", icon_custom_emoji_id="5258226313285607065", callback_data="trial_sub"))
    
    keyboard.row(InlineKeyboardButton(text="Купить", icon_custom_emoji_id="5359805631320571519", callback_data="buy_sub"))
    keyboard.row( InlineKeyboardButton(text="Профиль", icon_custom_emoji_id="5258011929993026890", callback_data="profile"))

    keyboard.row(
        InlineKeyboardButton(text="Поддержка",icon_custom_emoji_id="5258503720928288433", callback_data="help"),
        InlineKeyboardButton(text="Канал", icon_custom_emoji_id="5260268501515377807", url="https://t.me/so2melon")
    )
    if user.admin:
        keyboard.row(InlineKeyboardButton(text="Админ панель", icon_custom_emoji_id="5258096772776991776", callback_data="admin_menu"))
    
    return keyboard.as_markup()

def trial_sub() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu"),
    )
    
    return keyboard.as_markup()

def profile() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Пополнить баланс", icon_custom_emoji_id="5258204546391351475", callback_data="top_up"),
        InlineKeyboardButton(text="Мои подписки", icon_custom_emoji_id="5257965174979042426", callback_data="my_subs"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu"),
    )
    
    keyboard.adjust(1, 1, 1)
    return keyboard.as_markup()

async def my_subs(session: AsyncSession, id: int) -> InlineKeyboardMarkup:
    subs = await session.execute(
        select(Subscription).where(Subscription.user_id == id)
    )

    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Купить", icon_custom_emoji_id="5359805631320571519", callback_data="buy_sub"))

    for sub in subs.scalars():

        icon = "5416081784641168838" if sub.status == "ACTIVE" else "5411225014148014586"
        time = get_remaining_time(sub.expire_at)

        keyboard.add(
            InlineKeyboardButton(
                text=f"{sub.username} ({time})",
                icon_custom_emoji_id=icon,
                callback_data=f"sub:{sub.short_uuid}"
            )
        )
    
    keyboard.add(InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="profile"))

    keyboard.adjust(1, 1, 1, 1, 1)

    return keyboard.as_markup()

def sub_menu(sub: Subscription) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Продлить", callback_data="renew_sub", icon_custom_emoji_id="5776213190387961618"),
        InlineKeyboardButton(text="Подключить", copy_text=sub.subscription_url, icon_custom_emoji_id="5260416304224936047"),
        InlineKeyboardButton(text="Устройства", callback_data="sub_devices", icon_custom_emoji_id="5877318502947229960"),
        InlineKeyboardButton(text="Назад", callback_data="my_subs", icon_custom_emoji_id="5258236805890710909")
    )

    keyboard.adjust(1, 1, 1, 1)
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
        InlineKeyboardButton(text="Telegram Stars", icon_custom_emoji_id="5260416304224936047", callback_data="crypto"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5260416304224936047", callback_data=back),
    )

    keyboard.adjust(1, 1, 1, 1)
    
    return keyboard.as_markup()

def delete_button(text = "OK"):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text=text, icon_custom_emoji_id="5260416304224936047", callback_data="delete_message")
    )
    
    return keyboard.as_markup()