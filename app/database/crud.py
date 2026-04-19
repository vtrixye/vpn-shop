from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from utils.logger import get_logger

logger = get_logger(__name__)

async def create_user(session: AsyncSession, id: int, name: str, username: str = None):
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