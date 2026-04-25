from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

async def main_menu(session: AsyncSession, id: int) -> InlineKeyboardMarkup:
    user = await session.get(User, id)
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text="Попробовать бесплатно", callback_data="trial_sub"))
    
    keyboard.row(InlineKeyboardButton(text="Купить", callback_data="buy_sub"))
    keyboard.row(
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
        InlineKeyboardButton(text="Поддержка", callback_data="help")
    )
    
    if user.admin:
        keyboard.row(InlineKeyboardButton(text="Админ панель", callback_data="admin_menu"))
    
    return keyboard.as_markup()

