from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

async def main_menu(session: AsyncSession, id: int) -> InlineKeyboardMarkup:
    user = await session.get(User, id)
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text="Попробовать бесплатно", icon_custom_emoji_id="5258226313285607065", callback_data="trial_sub"))
    
    keyboard.row(InlineKeyboardButton(text="Купить", icon_custom_emoji_id="5359805631320571519", callback_data="buy_sub"))
    keyboard.row(
        InlineKeyboardButton(text="Профиль", icon_custom_emoji_id="5258011929993026890", callback_data="profile"),
        InlineKeyboardButton(text="Поддержка",icon_custom_emoji_id="5258503720928288433", callback_data="help")
    )
    
    if user.admin:
        keyboard.row(InlineKeyboardButton(text="Админ панель", icon_custom_emoji_id="5258096772776991776", callback_data="admin_menu"))
    
    return keyboard.as_markup()

