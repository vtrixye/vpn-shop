from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputRichMessage, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid as uuid_lib

from database.models import Subscription
from telegram.text import Text
from telegram.keyboards import payment as kb
from services.cryptopay_service import get_cryptopay
from services.cryptopay_service.models import PaymentData
from telegram.filters import ChatTypeFilter, IsBlocked
from utils.logger import get_logger
from utils.pricing import *
from utils.validators import validate_payment_state_data

logger = get_logger(__name__)

payment_router = Router()
payment_router.message.filter(ChatTypeFilter(['private']), IsBlocked())
payment_router.callback_query.filter(ChatTypeFilter(['private']), IsBlocked())

class BuySubState(StatesGroup):
    wait_devices = State()

class RenewSubState(StatesGroup):
    wait_changes = State()

class TopUpState(StatesGroup):
    wait_amount = State()

class Payment(StatesGroup):
    wait_for_method = State()

@payment_router.callback_query(F.data.startswith("sub:renew:"))
async def sub_renew(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    short_uuid = callback.data.split(":")[-1]

    stmt = select(Subscription).where(Subscription.short_uuid == short_uuid)
    sub = await session.scalar(stmt)

    if sub.tag == "UNLIMITED":
        return await callback.answer(
            text="Ваша подиска уже безлимитная",
            show_alert=True
        )

    await callback.answer()

    amount = calculate_renew(sub=sub, time=1, devices=sub.hwid_device_limit)
    logger.info(f"Цена вычислена {amount}")
    if await state.get_state() == RenewSubState.wait_changes:
        data = await state.get_data()
    else:
        await state.set_state(RenewSubState.wait_changes)
        data = {
                "sub": str(sub.uuid),
                "devices": sub.hwid_device_limit,
                "time": 1,
                "back": f"sub:{short_uuid}",
                "amount": amount,
                "type": "sub_renewal"
            }
        await state.update_data(data)

    text = Text.sub_renew(data)
    keyboard = kb.sub_renew(sub, amount)

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.callback_query(F.data == "dev_renew")
async def dev_renew(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    if not validate_payment_state_data(data):
        return await callback.answer(
            text=Text.state_error(),
            show_alert=True
        )

    sub = await session.get(Subscription, uuid_lib.UUID(data["sub"]))

    amount = calculate_add_device(sub)

    text = Text.dev_renew(amount)
    keyboard = kb.dev_renew(sub)

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.callback_query(F.data == "buy_sub")
async def buy_sub(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    text = Text.buy_sub()
    keyboard = kb.buy_sub()

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.callback_query(F.data.startswith("buy_month_"))
async def buy_month(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    time = int(callback.data.split("_")[-1])
    await state.set_state(BuySubState.wait_devices)
    amount = price_list["time"][time]
    await state.set_data(
        {"time": time, "devices": 1, "type": "sub_purchase",
         "amount": amount, "sub": "new", "back": "buy_dev_1"}
    )

    text = Text.buy_devices(time)
    keyboard = await kb.buy_devices(state)

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.callback_query(F.data.startswith("buy_dev_"))
async def buy_dev(callback: CallbackQuery, state: FSMContext):
    devices = int(callback.data.split("_")[-1])
    if devices > 6 or devices < 1:
        return await callback.answer(
            text=Text.unknown_error(),
            show_alert=True
        )
    data = await state.get_data()
    if data.get("time") is None or data.get("sub") is None:
        return await callback.answer(
            text=Text.state_error(),
            show_alert=True
        )
    await state.set_state(BuySubState.wait_devices)
    await callback.answer()
    amount = calculate_buy(time=data["time"], devices=devices)
    await state.update_data({"devices": devices, "amount": amount, "back": callback.data})

    text = Text.buy_devices(data["time"])
    keyboard = await kb.buy_devices(state)

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.callback_query(F.data == "payment_method")
async def pay_sub(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    if not validate_payment_state_data(data):
        return await callback.answer(
            text=Text.state_error(),
            show_alert=True
        )

    await state.set_state(Payment.wait_for_method)
    
    await callback.answer()

    text = Text.payment_method(data["amount"])
    keyboard = kb.payment_method(back=data.get("back"))

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.callback_query(TopUpState.wait_amount, F.data.startswith("top_up_"))
async def top_up_amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    amount = int(callback.data.split("_")[-1])
    await state.set_state(Payment.wait_for_method)
    await state.update_data(amount=amount)
    text = Text.payment_method(amount)
    keyboard = kb.payment_method(back="top_up")
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.callback_query(F.data == "top_up")
async def top_up(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(TopUpState.wait_amount)
    await state.update_data(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    text = Text.top_up()
    keyboard = kb.top_up()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.message(TopUpState.wait_amount)
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
        text = Text.payment_method(amount)
        keyboard = kb.payment_method(back="top_up")

    await message.bot.edit_message_text(
            rich_message=InputRichMessage(markdown=text),
            chat_id=data["chat_id"],
            message_id=data["message_id"],
            reply_markup=keyboard
        )

@payment_router.callback_query(F.data == "cp_top_up")
async def create_invoice_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    
    payload = PaymentData(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    
    cp = get_cryptopay()
    invoice = await cp.create_invoice(
        amount=50,
        currency_type="fiat",
        fiat="RUB",
        accepted_assets=["USDT", "TON"],
        description="test description",
        hidden_message="test hidden message",
        payload=payload.pack()
    )

    text = Text.invoice_created(invoice)
    keyboard = kb.cryptopay_invoice(invoice.mini_app_invoice_url, invoice.amount)
    
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.callback_query(F.data == "pay_stars")
async def pay_stars(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    amount = int(int(data["amount"]) * 0.8)
    price = [LabeledPrice(label="XTR", amount=amount)]
    invoice_link = await callback.bot.create_invoice_link(
        title="Balance top-up",
        description="Top Up Your Balance for Auto-Purchases",
        payload="UNIQUE_PAYLOAD",
        currency="XTR",
        prices=price,
    )

    text = Text.pay_stars()
    keyboard = kb.pay_stars(amount, invoice_link)

    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@payment_router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
