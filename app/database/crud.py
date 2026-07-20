import os
import aiogram
from datetime import timezone, timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Subscription, Payment, PaymentType, PaymentMethod
from utils.logger import get_logger
from utils.time import utc_to_msk
from typing import Union
from remnawave.models import UserDto, CreateUserResponseDto

DEFAULT_SUB_USER_ID = int(os.getenv("DEFAULT_SUB_USER_ID"))

logger = get_logger(__name__)

async def create_user(session: AsyncSession, id: int, name: str, username: str = None) -> User:
    user = User(
        id=id,
        name=name, 
        username=username,
        balance=0,
        admin=False,
        blocked=False,
        trial=True
    )
    session.add(user)
    await session.commit()
    logger.info(f"Пользователь {name} ID: {id} успешно создан")
    return user

async def update_user(session: AsyncSession, from_user: aiogram.types.User):
    user = await session.get(User, from_user.id)
    
    user.name = from_user.full_name
    user.username = from_user.username
    
    await session.commit()

async def create_sub(
        session: AsyncSession, 
        user: Union[UserDto, CreateUserResponseDto]
    ) -> Subscription:
    
    squads = [squad.uuid for squad in user.active_internal_squads]

    sub = Subscription(
        uuid=user.uuid,
        short_uuid=user.short_uuid,
        username=user.username,
        status=user.status,
        
        traffic_limit_bytes=user.traffic_limit_bytes,
        traffic_limit_strategy=user.traffic_limit_strategy,
        
        expire_at=utc_to_msk(user.expire_at),
        created_at=utc_to_msk(user.created_at),
        
        email=user.email,
        description=user.description,
        tag=user.tag,
        
        hwid_device_limit=user.hwid_device_limit,
        
        subscription_url=user.subscription_url,

        user_id=DEFAULT_SUB_USER_ID,
        squads=squads
    )

    if user.telegram_id is not None:
        user_tg = await session.get(User, user.telegram_id)
        if  user_tg is not None:
            sub.user_id = user.telegram_id
    
    session.add(sub)
    await session.commit()
    logger.info(
        f"Подписка {sub.username} добавлена для пользователя {sub.user_id}"
    )
    return sub

async def update_sub(
        session: AsyncSession,
        user: UserDto
    ) -> None:
    sub = await session.get(Subscription, user.uuid)

    sub.status = user.status
    sub.traffic_limit_bytes = user.traffic_limit_bytes
    sub.traffic_limit_strategy = user.traffic_limit_strategy
    sub.expire_at = utc_to_msk(user.expire_at)
    sub.email = user.email
    sub.description = user.description
    sub.tag = user.tag
    sub.hwid_device_limit = user.hwid_device_limit
    sub.user_id = DEFAULT_SUB_USER_ID

    squads = [squad.uuid for squad in user.active_internal_squads]

    sub.squads = squads
    
    if user.telegram_id is not None:
        user_tg = await session.get(User, user.telegram_id)
        if  user_tg is not None:
            sub.user_id = user.telegram_id
    
    await session.commit()
    logger.info(
        f"Подписка {sub.username} изменена"
    )

async def create_payment(
        session: AsyncSession,
        user_id: int,
        amount: int,
        paid_amount: int,
        paid_currency: str,
        transaction_id: str = None,
        payment_type: PaymentType = None,
        payment_method: PaymentMethod = None,
        status: str = None,
        data: dict = None
    ) -> Payment:

    payment = Payment(
        user_id=user_id,
        transaction_id=transaction_id, 
        amount=amount,
        paid_amount=paid_amount,
        paid_currency=paid_currency,
        type=payment_type,
        method=payment_method,
        status=status,
        created_at=utc_to_msk(datetime.now(timezone.utc)),
        data=data
    )

    session.add(payment)
    await session.commit()
    logger.info(
        f"Создана запись о платеже {payment.id} для пользователя {user_id}"
    )
    return payment
