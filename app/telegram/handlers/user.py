from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputRichMessage
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from telegram.filters import ChatTypeFilter, IsBlocked
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.user as kb
import services.remnawave_service.api as rw
from services.remnawave_service.enums import UsernameType, ExpireType
from utils.logger import get_logger

logger = get_logger(__name__)

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']), IsBlocked())
user_router.callback_query.filter(ChatTypeFilter(['private']), IsBlocked())

@user_router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    text = Text.main_menu()
    keyboard = await kb.main_menu(session=session, id=callback.from_user.id)
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    text = await Text.profile(session, callback.from_user.id)
    keyboard = kb.profile()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

class TopUpState(StatesGroup):
    amount = State()

class Payment(StatesGroup):
    wait_for_method = State()

@user_router.callback_query(TopUpState.amount, F.data.startswith("top_up_"))
async def top_up_amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()


@user_router.callback_query(F.data == "top_up")
async def top_up(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(TopUpState.amount)
    await state.update_data(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    text = Text.top_up()
    keyboard = kb.top_up()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.message(TopUpState.amount)
async def top_up_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = message.text.strip()
    await message.delete()

    if not (amount.isdigit() and 100 <= int(amount) <= 99999):
        text = "Введите целое число (минимум 100)"
        keyboard = kb.top_up()
    else:
        await state.set_state(Payment.wait_for_method)
        await state.update_data(amount=int(amount))
        text = Text.payment()
        keyboard = kb.payment(back="top_up")

    await message.bot.edit_message_text(
            rich_message=InputRichMessage(markdown=text),
            chat_id=data["chat_id"],
            message_id=data["message_id"],
            reply_markup=keyboard
        )

@user_router.callback_query(F.data == "my_subs")
async def my_subs(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    text = Text.my_subs()
    keyboard = await kb.my_subs(session=session, id=callback.from_user.id)
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data.startswith("sub:"))
async def sub_menu(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    short_uuid = callback.data.split(":")[1]
    if not(await rw.check_callback(callback.from_user.id, short_uuid, session)):
        return
    text = await Text.sub_menu(session, short_uuid)
    keyboard = kb.sub_menu()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data == "trial_sub")
async def trial_sub(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    await rw.create_user(
        username=UsernameType.TRIAL, expire_at=ExpireType.DAY,
        tag="TRIAL", telegram_id=callback.from_user.id
        )

    user = await session.get(User, callback.from_user.id)
    user.trial = False
    await session.commit()

    text = Text.trial_sub()
    keyboard = kb.trial_sub()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data == "delete_message")
async def delete_message(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

@user_router.message(Command("rich"))
async def rich(message: Message, command: CommandObject):
    await message.delete()
    if not(command.args):
        return await message.answer(
            text="нет текста",
            reply_markup=kb.delete_button("Удалить")
        )
    
    await message.answer_rich(
        rich_message=InputRichMessage(markdown=command.args),
        reply_markup=kb.delete_button()
    )

@user_router.callback_query()
async def other(callback: CallbackQuery):
    return await callback.answer("В разработке", show_alert=True)
