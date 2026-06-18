import os
import uuid as uuid_lib
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Union
from remnawave.models import CreateUserRequestDto, UserResponseDto
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Subscription, User
from services.remnawave_service import get_remnawave
from services.remnawave_service.enums import UsernameType, ExpireType
from utils.logger import get_logger
from utils import rand
from utils import time

logger = get_logger(__name__)

DEFAULT_SUB_USER_ID = os.getenv("DEFAULT_SUB_USER_ID")
if not DEFAULT_SUB_USER_ID:
    raise ValueError("DEFAULT_SUB_USER_ID is not set in environment")

DEFAULT_INTERNAL_SQUAD = uuid_lib.UUID("dee381c9-17dd-4221-ab57-511543f58d7b")
remnawave = get_remnawave()

async def create_user(
        username: Union[str, UsernameType] = UsernameType.REGULAR,
        expire_at: Union[datetime, timedelta, ExpireType] = ExpireType.MONTH,
        description: Optional[str] = None,
        tag: Optional[str] = None,
        telegram_id: Union[str, int] = DEFAULT_SUB_USER_ID,
        hwid_device_limit: int = 2,
        active_internal_squads: Optional[List[uuid_lib.UUID]] = None
) -> UserResponseDto:
    
    if isinstance(username, UsernameType):
        if username in (UsernameType.TEST, UsernameType.TRIAL) and tag is None:
            tag = username.name
        username = await rand.generate_username(username)

    if isinstance(expire_at, ExpireType):
        expire_at = time.get_expiration_time(expire_at)
    elif isinstance(expire_at, timedelta):
        expire_at = datetime.now(timezone.utc) + expire_at

    telegram_id = int(telegram_id)

    if active_internal_squads is None:
        active_internal_squads = [DEFAULT_INTERNAL_SQUAD]

    user = CreateUserRequestDto(
        username=username,
        expire_at=expire_at,
        description=description,
        tag=tag,
        telegram_id=telegram_id,
        hwid_device_limit=hwid_device_limit,
        active_internal_squads=active_internal_squads
    )

    remnawave.users.get_user_by_username
    created_user = await remnawave.users.create_user(body=user)
    logger.info(f"Отправлен запрос на создание пользователя {username}")
    return created_user

async def is_username_taken(username: str) -> bool:
    try:
        await remnawave.users.get_user_by_username(username=username.strip())
        return True
    except Exception as e:
        if "404" in str(e):
            return False
        
        logger.error(f"Не удалось проверить юзернейм {username} через API: {e}")
        return True

async def check_callback(id: int, short_uuid: str, session: AsyncSession):
    sub = session.query(Subscription).filter(
        Subscription.short_uuid == short_uuid
    ).first()
    if sub.user_id != id:
        return False
    try:
        await remnawave.users.get_user_by_short_uuid(short_uuid)
        return True
    except:
        return False