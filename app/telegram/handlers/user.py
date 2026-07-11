from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputRichMessage
from aiogram.filters import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid as uuid_lib
import asyncio

from telegram.filters import ChatTypeFilter, IsBlocked
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.user as kb
import services.remnawave_service.api as rw
from services.remnawave_service.enums import UsernameType, ExpireType, InternalSquad
from utils.logger import get_logger

logger = get_logger(__name__)

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']), IsBlocked())
user_router.callback_query.filter(ChatTypeFilter(['private']), IsBlocked())

@user_router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.clear()
    await callback.answer()
    text = Text.main_menu()
    keyboard = await kb.main_menu(session=session, id=callback.from_user.id)
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.answer()
    await state.clear()
    await update_user(session, callback.from_user)
    text = await Text.profile(session, callback.from_user.id)
    keyboard = kb.profile()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data == "my_subs")
async def my_subs(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.clear()
    await callback.answer()
    text = Text.my_subs()
    keyboard = await kb.my_subs(session=session, id=callback.from_user.id)
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data.startswith("sub:sq:"))
async def sub_sq(callback: CallbackQuery, session: AsyncSession):
    short_uuid = callback.data.split(":")[-1]

    stmt = select(Subscription).where(Subscription.short_uuid == short_uuid)
    sub = await session.scalar(stmt)

    if not(await rw.check_callback(callback.from_user.id, sub)):
        return

    if sub.tag == "WHITE":
        return await callback.answer(
            "Для этого типа подписки недоступно изменение протоколов и транспортов",
            show_alert=True
        )
    
    await callback.answer()

    text = Text.sub_sq()
    keyboard = kb.sub_sq(sub)
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data.startswith("sub:set:sq:"))
async def sub_set_sq(callback: CallbackQuery, session: AsyncSession):
    short_uuid = callback.data.split(":")[-1]

    stmt = select(Subscription).where(Subscription.short_uuid == short_uuid)
    sub = await session.scalar(stmt)

    if not(await rw.check_callback(callback.from_user.id, sub)):
        return

    name = callback.data.split(":")[-2]

    if not await rw.update_squads(sub, InternalSquad[name]):
        return await callback.answer(
            "Произошла неизвестная ошибка...\nПовторите попытку или обратитесь в поддержку 🫤",
            show_alert=True
        )

    await callback.answer()

    text = Text.sub_sq()
    keyboard = kb.sub_sq(sub)
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

class TransferState(StatesGroup):
    wait_for_id = State()

@user_router.callback_query(F.data.startswith("sub:trans:"))
async def sub_trans(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.answer()
    short_uuid = callback.data.split(":")[-1]

    stmt = select(Subscription).where(Subscription.short_uuid == short_uuid)
    sub = await session.scalar(stmt)

    if not(await rw.check_callback(callback.from_user.id, sub)):
        return
    
    await state.set_state(TransferState.wait_for_id)
    await state.set_data({"short_uuid": sub.short_uuid, "mes_id": callback.message.message_id})

    text = Text.sub_trans()
    keyboard = kb.sub_trans()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )


@user_router.message(TransferState.wait_for_id, F.text)
async def transfer_to(message: Message, state: FSMContext, session: AsyncSession):
    data = state.get_data()
    telegram = message.text.strip()
    if telegram.isdigit() and len(telegram) == 10:
        user = await session.get(User, int(telegram))
        text = Text.transfer_to()
        keyboard = kb.transfer_to(user)
    else:
        text = "![❌](tg://emoji?id=5260342697075416641) Введите Telegram ID (цифры)"
    

    await message.bot.edit_message_text(
        message_id=data["mes_id"],
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data.startswith("sub:opt:"))
async def sub_opt(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    short_uuid = callback.data.split(":")[-1]

    stmt = select(Subscription).where(Subscription.short_uuid == short_uuid)
    sub = await session.scalar(stmt)

    if not(await rw.check_callback(callback.from_user.id, sub)):
        return

    text = Text.sub_opt()
    keyboard = kb.sub_opt(sub)

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

class DevicesState(StatesGroup):
    menu= State()

@user_router.callback_query(F.data.startswith("sub:dev:"))
async def sub_dev(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.answer()
    short_uuid = callback.data.split(":")[-1]

    stmt = select(Subscription).where(Subscription.short_uuid == short_uuid)
    sub = await session.scalar(stmt)

    if not(await rw.check_callback(callback.from_user.id, sub)):
        return

    await state.set_state(DevicesState.menu)
    await state.update_data(uuid=str(sub.uuid))

    hw = await rw.get_user_devices(sub)
    text = Text.sub_dev(hw.total)
    keyboard = kb.sub_dev(hw, short_uuid)

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data.startswith("sub:"))
async def sub_menu(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.answer()
    await state.clear()

    short_uuid = callback.data.split(":")[1]

    stmt = select(Subscription).where(Subscription.short_uuid == short_uuid)
    sub = await session.scalar(stmt)

    if not(await rw.check_callback(callback.from_user.id, sub)):
        return
    
    hw = await rw.get_user_devices(sub)
    text = Text.sub_menu(sub, hw.total)
    keyboard = kb.sub_menu(sub)
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data.startswith("dev:"))
async def delete_device(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    state_data = await state.get_data()
    if state_data.get("uuid") is None:
        return await callback.answer(
            "Ошибка состояния. Перезайдите во вкладку \"Устройства\" и повторите попытку.", 
            show_alert=True
        )
    if await rw.delete_device(uuid=state_data["uuid"], hwid=callback.data.split(":")[-1]):
        await callback.answer(
            "Устройство удалено!"
        )
    else:
        await callback.answer(
            "Ошибка удаления. Перезайдите во вкладку \"Устройства\" и повторите попытку.",
            show_alert=True
        )

    sub = await session.get(Subscription, state_data["uuid"])

    hw = await rw.get_user_devices(sub)
    text = Text.sub_dev(hw.total)
    keyboard = kb.sub_dev(hw, sub.short_uuid)

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@user_router.callback_query(F.data == "trial_sub")
async def trial_sub(callback: CallbackQuery, session: AsyncSession):

    if not await rw.create_user(
            username=UsernameType.TRIAL, expire_at=ExpireType.DAY,
            tag="TRIAL", telegram_id=callback.from_user.id,
            active_internal_squads=[InternalSquad.VLESS_TCP, InternalSquad.CDN]
    ):
        return await callback.answer(
            "Произошла неизвестная ошибка...\nПовторите попытку или обратитесь в поддержку 🫤",
            show_alert=True
        )

    await callback.answer()
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
