import os
import uuid as uuid_lib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
from remnawave.models import CreateUserRequestDto, UserResponseDto
from dotenv import load_dotenv
from services.remnawave_service import get_remnawave
from utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

DEFAULT_SUB_USER_ID = os.getenv("DEFAULT_SUB_USER_ID")
DEFAULT_INTERNAL_SQUAD = uuid_lib.UUID("dee381c9-17dd-4221-ab57-511543f58d7b")
remnawave = get_remnawave()

async def create_user(
        username: str,
        expire_at: datetime,
        description: Optional[str] = None,
        tag: Optional[str] = None,
        telegram_id: Union[str, int, None] = DEFAULT_SUB_USER_ID,
        hwid_device_limit: Optional[int] = 2,
        active_internal_squads: Optional[List[uuid_lib.UUID]] = None
) -> UserResponseDto:
    
    if telegram_id is None:
        logger.error("telegram_id не найден в переменной окружения DEFAULT_SUB_USER_ID")
        raise ValueError(
            "telegram_id is None"
            )
    else:
        telegram_id = int(telegram_id)

    if active_internal_squads is None:
        active_internal_squads = [DEFAULT_INTERNAL_SQUAD]

    logger.info("Создание DTO")

    logger.info(f"username: {username}, type: {type(username)}")
    logger.info(f"expire_at: {expire_at}, type: {type(expire_at)}")
    logger.info(f"description: {description}, type: {type(description)}")
    logger.info(f"tag: {tag}, type: {type(tag)}")
    logger.info(f"telegram_id: {telegram_id}, type: {type(telegram_id)}")
    logger.info(f"hwid_device_limit: {hwid_device_limit}, type: {type(hwid_device_limit)}")
    logger.info(f"active_internal_squads: {active_internal_squads}, type: {type(active_internal_squads)}")

    user = CreateUserRequestDto(
        username=username,
        expire_at=expire_at,
        description=description,
        tag=tag,
        telegram_id=telegram_id,
        hwid_device_limit=hwid_device_limit,
        active_internal_squads=active_internal_squads
    )

    logger.info("Пробуем создать пользователя")
    try:
        await remnawave.users.create_user(body=user)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    logger.info(f"Отправлен запрос на создание пользователя {username}")