from dotenv import load_dotenv
load_dotenv()

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from telegram import setup_webhook, setup_middlewares, shutdown_bot
from webhooks import routers
from database import create_db
from utils.logger import get_logger
import webhooks.remnawave.handlers
from services.remnawave_service import init_remnawave
from services.cryptopay_service import init_cryptopay

logger = get_logger(__name__)

async def init_db():
    try:
        await create_db()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to database\n{e}")
        raise

async def init_bot():
    try:
        await setup_middlewares() 
        await setup_webhook()
        logger.info("Bot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize bot\n{e}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):

    init_cryptopay(app=app)
    await init_db()
    await init_bot()
    init_remnawave()

    yield
    
    await shutdown_bot()

app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)