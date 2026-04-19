from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from database.crud import *

start_router = Router()

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
    
    await message.answer("Это была команда старт")

@start_router.message(F.text == "кто я")
async def who_am_i(message: Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)

    if user is None:
        return await message.answer("ты никто")
    
    await message.answer(f"ты - {user.name} : {user.id}")
