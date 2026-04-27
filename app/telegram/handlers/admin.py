from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from telegram.filters import ChatTypeFilter, IsAdmin
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.admin as kb

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private', 'group']), IsAdmin())
admin_router.callback_query.filter(ChatTypeFilter(['private', 'group']), IsAdmin())

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    text = Text.admin_menu()
    keyboard = kb.admin_menu()
    await message.answer(text=text, reply_markup=keyboard)

@admin_router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    text = Text.admin_menu()
    keyboard = kb.admin_menu()
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()

@admin_router.callback_query(F.data == "subs_control")
async def subs_control(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = Text.subs_control()
    keyboard = kb.subs_control()
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()

class CreateSubState(StatesGroup):
    edit = State()
    username = State()
    expire_at = State()
    hwid = State()
    telegram = State()

@admin_router.callback_query(F.data == "sub_create")
async def sub_create(callback: CallbackQuery, state: FSMContext):
    text = Text.sub_create()
    keyboard = kb.sub_create()
    await callback.message.edit_text(text=text, reply_markup=keyboard)
    await callback.answer()
    await state.set_state(CreateSubState.edit)
