import os
import sys
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import routers
from database import create_db, session_maker

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

for router in routers:
    dp.include_router(router)


async def on_startup():
    try:
        await create_db()
    except Exception as e:
        print(f"Не удалось подключиться к базе данных\n{e}")
    sys.exit(1)
    print("Бот запущен")


async def on_shutdown():
    await bot.session.close()
    print("Бот завершил работу")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # middlewares

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
