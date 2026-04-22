from webhooks.telegram import telegram_router
from webhooks.remnawave import remnawave_router

routers = [
    telegram_router,
    remnawave_router
]