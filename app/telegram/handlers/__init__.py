from telegram.handlers.start import start_router
from telegram.handlers.admin import admin_router
from telegram.handlers.user import user_router
from telegram.handlers.payment import payment_router

routers = [
    start_router,
    admin_router,
    payment_router,
    user_router
]