from webhooks.telegram import telegram_router
from webhooks.remnawave import remnawave_router
from webhooks.platega import platega_router

routers = [
    telegram_router,
    remnawave_router,
    platega_router
]