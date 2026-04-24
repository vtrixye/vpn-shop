import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Subscription
from utils.logger import get_logger
from datetime import datetime
from typing import Optional, Union
from remnawave.models import UserDto, CreateUserResponseDto


load_dotenv()

DEFAULT_SUB_USER_ID = os.getenv("")

logger = get_logger(__name__)

async def create_user(session: AsyncSession, id: int, name: str, username: str = None) -> User:
    user = User(
        id=id,
        name=name, 
        username=username,
        balance=0,
        admin=False,
        blocked=False
    )
    session.add(user)
    await session.commit()
    logger.info(f"Пользователь {name} ID: {id} успешно создан")
    return user

async def create_sub(
        session: AsyncSession, 
        user: Union[UserDto, CreateUserResponseDto]
    ) -> Subscription:
    
    sub = Subscription(
        uuid=user.uuid,
        short_uuid=user.short_uuid,
        username=user.username,
        status=user.status,
        
        traffic_limit_bytes=user.traffic_limit_bytes,
        traffic_limit_strategy=user.traffic_limit_strategy,
        
        expire_at=user.expire_at,
        created_at=user.created_at,
        
        email=user.email,
        description=user.description,
        tag=user.tag,
        
        hwid_device_limit=user.hwid_device_limit,
        
        subscription_url=user.subscription_url,
        
        user_id=user.telegram_id if user.telegram_id else DEFAULT_SUB_USER_ID,
        squads=user.active_internal_squads,
    )
    
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
    sub.expire_at = user.expire_at
    sub.email = user.email
    sub.description = user.description
    sub.tag = user.tag
    sub.hwid_device_limit = user.hwid_device_limit
    sub.user_id = user.telegram_id if user.telegram_id else DEFAULT_SUB_USER_ID
    sub.squads = user.active_internal_squads

    await session.commit
    logger.info(
        f"Подписка {sub.username} изменена"
    )