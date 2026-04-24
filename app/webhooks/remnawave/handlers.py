from remnawave.models.webhook import UserDto, NodeDto
from sqlalchemy.ext.asyncio import AsyncSession

from webhooks.remnawave import remnawave_handler
from utils.logger import get_logger
from database.crud import *

logger = get_logger(__name__)

@remnawave_handler("user.created")
async def user_created(session: AsyncSession, user: UserDto):
    await create_sub(session=session, user=user)

@remnawave_handler("user.modified")
async def user_modified(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    logger.info("Modified handler")
    if sub is not None:
        logger.info("Known sub")
        await update_sub(session=session, user=user)
    else:
        logger.info("Unknown sub")
        await create_sub(session=session, user=user)

@remnawave_handler("user.disabled")
async def user_disabled(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    sub.status = "DISABLED"
    await session.commit()


@remnawave_handler("user.enabled")
async def user_enabled(session: AsyncSession, user: UserDto):
    sub = await session.get(Subscription, user.uuid)
    sub.status = "ACTIVE"
    await session.commit()