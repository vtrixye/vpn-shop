from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    InputRichMessage
    )
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from redis.asyncio import Redis

from telegram.filters import ChatTypeFilter, IsAdmin
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.admin as kb
from utils.validators import VALIDATORS

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private', 'group']), IsAdmin())
admin_router.callback_query.filter(ChatTypeFilter(['private', 'group']), IsAdmin())

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    text = Text.admin_menu()
    keyboard = kb.admin_menu()
    await message.answer_rich(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    await callback.answer()
    text = Text.admin_menu()
    keyboard = kb.admin_menu()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@admin_router.message(Command("test"))
async def test(message: Message, redis: Redis):
    await redis.set(f"user:{message.from_user.id}", "active", ex=3600)
    status = await redis.get(f"user:{message.from_user.id}")
    await message.answer(f"Статус в Redis: {status}")


@admin_router.callback_query(F.data == "subs_control")
async def subs_control(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()
    await state.clear()
    text = await Text.subs_control(session)
    keyboard = kb.subs_control()
    try:
        await callback.message.edit_text(
            rich_message=InputRichMessage(markdown=text),
            reply_markup=keyboard
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e).lower():
            pass
        else:
            raise


class CreateSubState(StatesGroup):
    menu = State()
    editing = State()

@admin_router.callback_query(F.data == "sub_create")
async def sub_create_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    current_state = await state.get_state()
    
    if current_state is None:
        await state.set_state(CreateSubState.menu)
        await state.update_data(mes_id=callback.message.message_id)
           
    data = await state.get_data()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=Text.sub_create(data)),
        reply_markup=kb.sub_create()
    )

@admin_router.callback_query(CreateSubState.menu, F.data.startswith("set:"))
async def set_field(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    field_name = callback.data.split(":")[1]
    
    await state.update_data(current_field=field_name)
    await state.set_state(CreateSubState.editing)
    
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=Text.sub_editing(field_name)),
        reply_markup=kb.sub_editing(field_name)
    )

@admin_router.message(CreateSubState.editing, F.text)
async def capture_field_text(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    
    data = await state.get_data()
    field_name = data.get("current_field")
    mes_id = data.get("mes_id")
    
    validator = VALIDATORS.get(field_name)
    if validator:
        is_valid, result = await validator(message.text)
        if not is_valid:
            return await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=mes_id,
                rich_message=InputRichMessage(markdown=result),
                reply_markup=kb.sub_editing(field_name)
            )
            
        await state.update_data({field_name: result})
    
    await state.set_state(CreateSubState.menu)
    
    updated_data = await state.get_data()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=mes_id,
        rich_message=InputRichMessage(markdown=Text.sub_create(updated_data)),
        reply_markup=kb.sub_create()
    )
    