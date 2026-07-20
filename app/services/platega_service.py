from typing import Optional, Dict, Any
import os
import json
from plategaio import (
    PlategaAsyncClient,
    CreateTransactionRequest,
    PaymentDetails,
    PlategaAPIError,
    PlategaNetworkError,
)
from sqlalchemy.ext.asyncio import AsyncSession

import database.crud as db
from services.process_payment import process_payment
from database import database
from database.models import Payment, PaymentMethod, PaymentType
from utils.logger import get_logger

logger = get_logger(__name__)

_platega_client: Optional[PlategaAsyncClient] = None


def init_platega() -> None:
    global _platega_client

    merchant_id = os.getenv("PLATEGA_MERCHANT_ID")
    secret_key = os.getenv("PLATEGA_SECRET_KEY")
    
    if not merchant_id or not secret_key:
        raise ValueError("PLATEGA_MERCHANT_ID и PLATEGA_SECRET_KEY должны быть установлены в .env")

    _platega_client = PlategaAsyncClient(
        merchant_id=merchant_id,
        secret=secret_key
    )
    logger.info("✅ Platega клиент инициализирован")


async def close_platega() -> None:
    global _platega_client
    
    if _platega_client:
        await _platega_client.close()
        _platega_client = None

def get_platega_client() -> PlategaAsyncClient:
    if _platega_client is None:
        raise RuntimeError("Platega клиент не инициализирован. Вызовите init_platega()")
    return _platega_client

async def create_payment(
    amount: float,
    currency: str = "RUB",
    description: str = "",
    return_url: str = "https://t.me/GrapeVpnRobot",
    failed_url: str = "https://t.me/GrapeVpnRobot",
    payment_method: int = 2,
    payload: Optional[Dict] = None,
) -> Dict[str, Any]:

    client = get_platega_client()

    payload = json.dumps(payload)
    
    try:
        request = CreateTransactionRequest(
            paymentMethod=payment_method,
            paymentDetails=PaymentDetails(amount=amount, currency=currency),
            description=description,
            returnUrl=return_url,
            failedUrl=failed_url,
            payload=payload,
        )
        
        response = await client.create_transaction(request)
        
        logger.info(f"✅ Платеж создан: {response.transaction_id}, статус: {response.status}")
        
        return {
            "success": True,
            "transaction_id": response.transaction_id,
            "redirect_url": response.redirect,
            "status": response.status,
        }
        
    except PlategaAPIError as e:
        logger.error(f"❌ API ошибка Platega: {e.message} (код {e.status_code})")
        return {
            "success": False,
            "error": e.message,
            "status_code": e.status_code,
        }
        
    except PlategaNetworkError as e:
        logger.error(f"❌ Сетевая ошибка Platega: {e}")
        return {
            "success": False,
            "error": "Ошибка соединения с платежной системой",
        }
        
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка при создании платежа: {e}")
        return {
            "success": False,
            "error": "Внутренняя ошибка сервиса",
        }

@database
async def handling_webhook(body: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:

    transaction_id = body.get("id")
    status = body.get("status")
    amount = body.get("amount")
    currency = body.get("currency")
    payload = json.loads(body.get("payload"))

    user_id = payload.get("user_id")
    type = PaymentType(payload.get("type"))
    excepted_amount = payload.get("excepted_amount")

    data = payload.copy()
    data.pop("user_id", None)
    data.pop("type", None)
    data.pop("excepted_amount", None)

    payment = await db.create_payment(
        session=session,
        user_id=int(user_id),
        amount=int(excepted_amount),
        transaction_id=transaction_id,
        paid_amount=int(amount),
        paid_currency=currency,
        payment_method=PaymentMethod.Platega,
        payment_type=type,
        status=status,
        data=data
    )

    logger.info(f"✅ Платеж {transaction_id} сохранен в БД для пользователя {user_id}")

    await process_payment(payment)

