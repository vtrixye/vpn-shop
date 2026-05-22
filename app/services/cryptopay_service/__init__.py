import os
from fastapi import FastAPI
from aiosend import CryptoPay, TESTNET
from aiosend.webhook import FastAPIManager
from services.cryptopay_service.handlers import router

CRYPTOPAY_TOKEN = os.getenv("CRYPTOPAY_TOKEN")
if not CRYPTOPAY_TOKEN:
    raise ValueError("CRYPTOPAY_TOKEN is not set")

cp = None

def init_cryptopay(app: FastAPI):
    global cp
    cp = CryptoPay(
        token=CRYPTOPAY_TOKEN,
        network=TESTNET,
        webhook_manager=FastAPIManager(app, "/webhooks/crypto")
    )

    cp.include_router(router=router)

def get_cryptopay() -> CryptoPay:
    if cp is None:
        raise ValueError("CryptoPay не инициализирован")
    return cp