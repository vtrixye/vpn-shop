from datetime import datetime, timedelta
import services.remnawave_service.api as rw

async def validate_username(text: str) -> tuple[bool, any]:
    username = text.strip()
    if len(username) < 3:
        return False, "![❌](tg://emoji?id=5260342697075416641) Юзернейм слишком короткий (минимум 3 символа). Введите еще раз:"
    
    if await rw.is_username_taken(username):
        return False, f"![❌](tg://emoji?id=5260342697075416641) Юзернейм ` {username} ` уже занят в панели! Введите другой:"
    
    if all((64 < ord(x) < 91) or (96 < ord(x) < 123) or x.isdigit() or x in "-_" for x in username):
        return True, username
    else:
        return False, "![❌](tg://emoji?id=5260342697075416641) Юзернейм должен содержать только латинский алфавит, цифры, _ и -"

async def validate_expire_at(text: str) -> tuple[bool, any]:
    clean_text = text.strip()
    
    try:
        days = int(clean_text)
        if days <= 0:
            return False, "![❌](tg://emoji?id=5260342697075416641) Количество дней должно быть больше нуля! Попробуйте еще раз:"
            
        future_date = datetime.now() + timedelta(days=days)
        return True, future_date.strftime("%Y-%m-%d")
        
    except ValueError:
        try:
            parsed_date = datetime.strptime(clean_text, "%d.%m.%Y")
            if parsed_date < datetime.now():
                return False, "![❌](tg://emoji?id=5260342697075416641) Дата не может быть в прошлом! Попробуйте еще раз:"
            return True, parsed_date.strftime("%Y-%m-%d")
            
        except ValueError:
            return False, "![❌](tg://emoji?id=5260342697075416641) Не удалось распарсить дату"

async def validate_hwid(text: str) -> tuple[bool, any]:
    try:
        count = int(text.strip())
        if 1 <= count <= 10:
            return True, count
        return False, "![❌](tg://emoji?id=5260342697075416641) Количество устройств должно быть от 1 до 10:"
    except ValueError:
        return False, "![❌](tg://emoji?id=5260342697075416641) Введите корректное число:"

async def validate_telegram(text: str) -> tuple[bool, any]:
    tg = text.strip()
    if tg.isdigit() and len(tg) == 10:
        return True, int(tg)
    return False, "![❌](tg://emoji?id=5260342697075416641) Введите Telegram ID (цифры)"

VALIDATORS = {
    "username": validate_username,
    "expire_at": validate_expire_at,
    "hwid": validate_hwid,
    "telegram": validate_telegram
}