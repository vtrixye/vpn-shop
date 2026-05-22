from aiogram import Router, F
from aiogram.types import Message

from services.cryptopay_service import get_cryptopay
from services.cryptopay_service.models import PaymentData
from telegram.filters import ChatTypeFilter, IsBlocked
from utils.logger import get_logger

logger = get_logger(__name__)

cryptopay_router = Router()
cryptopay_router.message.filter(ChatTypeFilter(['private']), IsBlocked())
cryptopay_router.callback_query.filter(ChatTypeFilter(['private']), IsBlocked())

@cryptopay_router.message(F.text == "test_invoice")
async def get_invoice(message: Message) -> None:
    payload = PaymentData(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    cp = get_cryptopay()
    invoice = await cp.create_invoice(
        amount=100,
        currency_type="fiat",
        fiat="RUB",
        accepted_assets=["USDT", "TON"],
        description="test description",
        hidden_message="test hidden message",
        payload=payload.pack()
        )
    await message.answer(f"pay: {invoice.mini_app_invoice_url}")