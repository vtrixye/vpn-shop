from datetime import datetime, timezone

def get_remaining_time(expire_at: datetime) -> str:
    now = datetime.now(timezone.utc)
    
    if expire_at.tzinfo is None:
        expire_at = expire_at.replace(tzinfo=timezone.utc)
    
    remaining = expire_at - now
    
    if remaining.total_seconds() <= 0:
        return "истекла"
    
    days = remaining.days
    hours = remaining.seconds // 3600
    
    if days >= 1:
        return f"{days} дн."
    else:
        return f"{hours} ч."