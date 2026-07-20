from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Subscription

def validate_payment_state_data(data: dict) -> bool:

    if data.get("type") not in ("sub_purchase", "sub_renewal", "add_device", "deposit"):
        return False

    if data.get("amount") is None or data.get("amount") < 0:
        return False
    
    if data.get("type") == "add_device":
        if data.get("sub") is None:
            return False
        
    if data.get("type") == "sub_purchase":
        if data.get("time") is None or data.get("devices") is None:
            return False
    
    if data.get("type") == "sub_renewal":
        if data.get("sub") is None or data.get("devices") is None or data.get("time") is None:
            return False
    
    if data.get("back") is None:
        return False
    
    return True