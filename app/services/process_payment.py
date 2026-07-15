from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from aiogram.types import InputRichMessage

from database.models import Payment
import telegram.keyboards.payment as kb
from telegram.text import Text
from database import database
from utils.logger import get_logger

logger = get_logger(__name__)

@database
async def process_payment(payment: Payment, session: AsyncSession):
    from telegram import bot
    await bot.edit_message_text(
        text=f"Платеж получен: {payment.id}",
        message_id=payment.data.get("mes_id"),
        chat_id=payment.user_id
    )