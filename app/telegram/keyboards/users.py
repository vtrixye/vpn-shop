from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

async def main_menu(session: AsyncSession, id: int) -> InlineKeyboardMarkup:
    user = await session.get(User, id)
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Попробовать бесплатно", callback_data="trial_sub"))

    keyboard.add(
        InlineKeyboardButton(text="Купить", callback_data="buy_sub"),
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
        InlineKeyboardButton(text="Поддержка", callback_data="help"),
    )
    keyboard.adjust(1, 2)
    if len(keyboard) == 4:
        keyboard.adjust(1, 1, 2)
    
    if user.admin:
        keyboard.add(InlineKeyboardButton(text="Админ панель", callback_data="admin_menu"))
        keyboard.adjust(1, 2, 1)
        if len(keyboard) == 5:
            keyboard.adjust(1, 1, 2, 1)
    return keyboard.as_markup()

