from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from telegram.text import Text
from telegram.keyboards import cryptopay as kb
from services.cryptopay_service import get_cryptopay
from services.cryptopay_service.models import PaymentData
from telegram.filters import ChatTypeFilter, IsBlocked
from utils.logger import get_logger

logger = get_logger(__name__)

cryptopay_router = Router()
cryptopay_router.message.filter(ChatTypeFilter(['private']), IsBlocked())
cryptopay_router.callback_query.filter(ChatTypeFilter(['private']), IsBlocked())

@cryptopay_router.callback_query(F.data == "create_invoice")
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
    keyboard = kb.cryptopay_invoice(invoice.mini_app_invoice_url)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )