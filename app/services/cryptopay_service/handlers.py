from aiogram.types import InputRichMessage
from aiosend import WebhookRouter
from aiosend.types import Invoice
from telegram.text import Text
import telegram.keyboards.payment as kb
from services.cryptopay_service.models import PaymentData

router = WebhookRouter()

@router.invoice_paid()
async def handle_payment(invoice: Invoice) -> None:
    from telegram import bot
    
    payload = PaymentData.unpack(invoice.payload)

    text = Text.invoice_paid()
    keyboard = kb.invoice_paid()
    
    await bot.edit_message_text(
        chat_id=payload.chat_id,
        message_id=payload.message_id,
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )