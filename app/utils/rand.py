import uuid as uuid_lib
from services.remnawave_service.enums import UsernameType
from services.remnawave_service import get_remnawave
from remnawave.exceptions import NotFoundError

remnawave = get_remnawave()

async def generate_username(prefix: UsernameType, attempts: int = 5) -> str:

    for _ in range(attempts):
        username = f"{prefix.value}_{uuid_lib.uuid4().hex[:8]}"

        try:
            await remnawave.users.get_user_by_username(username)
            continue
        except NotFoundError:
            return username
        except Exception:
            raise
    
    raise ValueError(
        f"Не удалось сгенерировать уникальный username за {attempts} попыток"
    )