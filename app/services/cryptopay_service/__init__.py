import os
from fastapi import FastAPI
from aiosend import CryptoPay, TESTNET, PayloadData
from aiosend.webhook import FastAPIManager

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

class PaymentData(PayloadData, prefix="payment"):
    chat_id: int
    message_id: int