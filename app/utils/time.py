from datetime import datetime, timedelta, timezone
from services.remnawave_service.enums import ExpireType

MSK = timezone(timedelta(hours=3))

def utc_to_msk(dt: datetime | None) -> datetime | None:
    """Конвертирует UTC datetime в naive MSK datetime"""
    if dt is None:
        return None
        
    if dt.tzinfo is not None:
        dt_msk = dt.astimezone(MSK)
        return dt_msk.replace(tzinfo=None)
    
    dt_utc = dt.replace(tzinfo=timezone.utc)
    dt_msk = dt_utc.astimezone(MSK)
    return dt_msk.replace(tzinfo=None)

def get_remaining_time(expire_at: datetime) -> str:
    now = datetime.now()
    
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
    return datetime.now(timezone.utc) + periods[period]
