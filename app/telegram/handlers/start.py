from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from telegram.filters import ChatTypeFilter, IsBlocked
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.users as kb

start_router = Router()
start_router.message.filter(ChatTypeFilter(['private']), IsBlocked())

@start_router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)

    if user is None:
        await create_user(
            session=session,
            id=message.from_user.id,
            name=message.from_user.full_name,
            username=message.from_user.username
        )
    
    text = Text.main_menu()
    keyboard = await kb.main_menu(session=session, id=message.from_user.id)
    await message.answer(text=text, reply_markup=keyboard)