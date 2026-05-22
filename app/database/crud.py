import os
from datetime import timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Subscription
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