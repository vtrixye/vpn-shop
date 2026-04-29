import os
from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv
from remnawave import RemnawaveSDK
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

_remnawave: Optional[RemnawaveSDK] = None

def init_remnawave() -> RemnawaveSDK:
    global _remnawave
    
    if _remnawave is not None:
        return _remnawave
    
    base_url = os.getenv("BASE_URL")
    token = os.getenv("REMNAWAVE_TOKEN")
    
    if not base_url:
        logger.error("BASE_URL не указан")
        raise ValueError("BASE_URL не указан в .env")
    
    if not token:
        logger.error("REMNAWAVE_TOKEN не указан")
        raise ValueError("REMNAWAVE_TOKEN не указан в .env")
    
    _remnawave = RemnawaveSDK(base_url=base_url, token=token)
    logger.info("Remnawave SDK успешно инициализирован")
    return _remnawave

def get_remnawave() -> RemnawaveSDK:
    if _remnawave is None:
        return init_remnawave()
    return _remnawave