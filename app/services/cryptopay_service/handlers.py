from aiogram import Bot
from telegram import bot
from aiosend.types import Invoice
from services.cryptopay_service import cp, PaymentData

bot: Bot

@cp.invoice_paid(PaymentData.filter())
async def handle_payment(
    invoice: Invoice,
    payload: PaymentData
) -> None:
    await bot.edit_message_text(
        chat_id = payload.chat_id,
        message_id=payload.message_id,
        text=f"payment received: {invoice.amount} {invoice.asset}",
    )