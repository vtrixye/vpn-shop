from aiosend import WebhookRouter
from aiosend.types import Invoice
from services.cryptopay_service.models import PaymentData

router = WebhookRouter()

@router.invoice_paid()
async def handle_payment(invoice: Invoice) -> None:
    from telegram import bot
    
    payload = PaymentData.from_payload(invoice.payload)
    
    await bot.edit_message_text(
        chat_id=payload.chat_id,
        message_id=payload.message_id,
        text=f"payment received: {invoice.amount} {invoice.asset}",
    )