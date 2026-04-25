from typing import Union
from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types
    
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        chat = update.message.chat if isinstance(update, CallbackQuery) else update.chat
        return chat.type in self.chat_types

class IsAdmin(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery], session: AsyncSession) -> bool:
        if not update.from_user:
            return False
        
        user = await session.get(User, update.from_user.id)
        if user is None or user.blocked:
            return False
        
        if user.admin:
            return True
        
        return False

class IsBlocked(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery], session: AsyncSession) -> bool:
        if not update.from_user:
            return False
        
        user = await session.get(User, update.from_user.id)
        if user is None or not user.blocked:
            return True
        
        if user.blocked:
            return False
        
        return False