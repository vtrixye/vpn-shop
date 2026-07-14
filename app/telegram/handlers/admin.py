from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InputRichMessage
    )
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.exceptions import TelegramBadRequest

from database.crud import *
from telegram.filters import ChatTypeFilter, IsAdmin
from telegram.text import Text
import telegram.keyboards.admin as kb

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

@admin_router.message(Command("test"))
async def cmd_test(message: Message, session: AsyncSession):
    payment =await create_payment(
        session=session,
        user_id=message.from_user.id,
        amount=100,
        currency="RUB",
        payment_type=None,
        payment_method=None,
        status=None,
        data={"test": "test"}
    )

    text = f"Создана запись о платеже {payment.id} для пользователя {message.from_user.id}"
    await message.answer_rich(
        rich_message=InputRichMessage(markdown=text)
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

@admin_router.callback_query(F.data == "stats")
async def admin_menu(callback: CallbackQuery):
    await callback.answer()
    text = Text.stats()
    keyboard = kb.stats()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "subs_stats")
async def subs_control(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    text = await Text.subs_stats(session)
    keyboard = kb.subs_stats()
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

@admin_router.callback_query(F.data == "users_stats")
async def users_control(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    text = await Text.users_stats(session)
    keyboard = kb.users_stats()
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