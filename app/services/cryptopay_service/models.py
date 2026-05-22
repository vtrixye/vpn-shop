from aiosend import PayloadData

class PaymentData(PayloadData, prefix="payment"):
    chat_id: int
    message_id: int