from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from services.remnawave_service.enums import ExpireType

def get_remaining_time(expire_at: datetime) -> str:
    now = datetime.now(timezone.utc)
    
    if expire_at.tzinfo is None:
        expire_at = expire_at.replace(tzinfo=timezone.utc)
    
    remaining = expire_at - now
    
    if remaining.total_seconds() <= 0:
        return "истекла"
    
    days = remaining.days
    hours = remaining.seconds // 3600
    
    if days >= 10000:
        return "безлимит"
    elif 1 <= days < 10000:
        return f"{days} дн."
    else:
        return f"{hours} ч."
    
def get_expiration_time(period: ExpireType):
    periods = {
            ExpireType.DAY: timedelta(days=1),
            ExpireType.WEEK: timedelta(weeks=1),
            ExpireType.MONTH: timedelta(days=30),
            ExpireType.THREE_MONTHS: timedelta(days=90),
            ExpireType.SIX_MONTHS: timedelta(days=180),
            ExpireType.YEAR: timedelta(days=365),
        }
    return datetime.now() + periods[period]

def now_moscow():
    return datetime.now(ZoneInfo("Europe/Moscow"))
