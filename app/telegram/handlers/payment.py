from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputRichMessage, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from telegram.text import Text
from telegram.keyboards import payment as kb
from services.cryptopay_service import get_cryptopay
from services.cryptopay_service.models import PaymentData
from telegram.filters import ChatTypeFilter, IsBlocked
from utils.logger import get_logger

logger = get_logger(__name__)

payment_router = Router()
payment_router.message.filter(ChatTypeFilter(['private']), IsBlocked())
payment_router.callback_query.filter(ChatTypeFilter(['private']), IsBlocked())

class TopUpState(StatesGroup):
    wait_amount = State()

class Payment(StatesGroup):
    wait_for_method = State()

@payment_router.callback_query(TopUpState.wait_amount, F.data.startswith("top_up_"))
async def top_up_amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    amount = int(callback.data.split("_")[-1])
    await state.set_state(Payment.wait_for_method)
    await state.update_data(amount=amount)
    text = Text.payment()
    keyboard = kb.payment(back="top_up")
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
        text = Text.payment()
        keyboard = kb.payment(back="top_up")

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
