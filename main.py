from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass