import os
from sqlalchemy.ext.asyncio import AsyncSession
from remnawave.models.webhook import NodeDto
from sqlalchemy import select, func

from database.models import User, Subscription

DEFAULT_SUB_USER_ID = os.getenv("DEFAULT_SUB_USER_ID")

class Text:
    def main_menu():
        return "## Главное меню"
    
    def trial_sub():
        return (
            "🎉 **Пробный период активирован!**\n\n"
            "Вы успешно получили доступ на **одни сутки**."
        )

    async def profile(session: AsyncSession, id: int):
        user = await session.get(User, id)
        stmt = select(func.count()).where(Subscription.user_id == id, Subscription.status == "ACTIVE")
        sub_count = await session.scalar(stmt)

        return (
            "## ![🛂](tg://emoji?id=5258011929993026890) Профиль\n\n"
            f'> ![🛂](tg://emoji?id=5936017305585586269) **ID:** `{id}`  \n'
            f'> ![💳](tg://emoji?id=5769403330761593044) **Баланс:** `{user.balance} ₽`  \n'
            f'> ![🟢](tg://emoji?id=5778335621491723621) **Активные подписки:** `{sub_count}`'
        )
    
    def my_subs():
        return (
            "## ![🛂](tg://emoji?id=5257965174979042426) Мои подписки\n\n"
            "Список ваших активных и завершенных подписок:"
        )
    
    def admin_menu():
        return (
            "## ![🛂](tg://emoji?id=5258096772776991776) Панель админа\n\n"
            "Управление системой и пользователями:"
        )

    async def subs_control(session: AsyncSession) -> str:
        result = await session.execute(
            select(
                Subscription.status,
                func.count(Subscription.uuid)
            )
            .group_by(Subscription.status)
        )
        
        stats = {status: count for status, count in result.all()}
        
        total = sum(stats.values())
        
        active = stats.get("ACTIVE", 0)
        expired = stats.get("EXPIRED", 0)
        disabled = stats.get("DISABLED", 0)
        
        text = (
            '## ![📊](tg://emoji?id=5203993413346680064) Статистика подписок\n\n'
            '| Статус | Количество |\n'
            '| :--- | :---: |\n'
            f'| ![📊](tg://emoji?id=5203993413346680064) **Всего** | `{total}` |\n'
            f'| ![🟢](tg://emoji?id=5416081784641168838) **ACTIVE** | `{active}` |\n'
            f'| ![🔴](tg://emoji?id=5411225014148014586) **EXPIRED** | `{expired}` |\n'
            f'| ![🔘](tg://emoji?id=5240241223632954241) **DISABLED** | `{disabled}` |'
        )
      
        return text
    
    def sub_create(data: dict = {}):
        
        username = data.get("username", "(не выбрано)")
        expire_at = data.get("expire_at", "(не выбрано)")
        hwid = data.get("hwid", "0")
        telegram = data.get("telegram", DEFAULT_SUB_USER_ID)

        return (
            "## 📝 Создание подписки\n\n"
            f'> ![🛂](tg://emoji?id=5814247475141153332) **Username:** `{username}`  \n'
            f'> ![🕘](tg://emoji?id=5776213190387961618) **Истекает:** `{expire_at}`  \n'
            f'> ![💻](tg://emoji?id=5877318502947229960) **Устройства:** `{hwid}`  \n'
            f'> ![🚹](tg://emoji?id=5879770735999717115) **Владелец:** `{telegram}`'
        )
    
    def set_username():
        return "✏️ **Введите username:**"

    def user_expired(sub: Subscription):
        return (
            f"![🕘](tg://emoji?id=5776213190387961618) **Подписка истекла**\n\n"
            f"Время действия подписки `{sub.username}` подошло к концу."
        )
    
    def user_expires_in_24_hours(sub: Subscription):
        return (
            f"⚠️ **Внимание**\n\n"
            f"Подписка `{sub.username}` истекает через **24 часа**!"
        )
    
    def node_connection_lost(node: NodeDto):
        return f"🚨 **Потеряно соединение!**\n\nНода: `{node.name}` недоступна."
    
    def node_connection_restored(node: NodeDto):
        return f"✅ **Соединение восстановлено!**\n\nНода: `{node.name}` снова в строю."
    
    def invoice_created(invoice):
        return (
            "🧾 **Счет на оплату**\n\n"
            f"Сумма к оплате: **{invoice.amount} {invoice.fiat}**\n\n"
            "Перейдите по ссылке ниже для завершения платежа:"
        )
    
    def invoice_paid():
        return "🎉 **Оплата прошла успешно!**\n\nСредства зачислены на ваш баланс."
    
    def top_up():
        return "💰 **Пополнение баланса**\n\nВведите сумму пополнения в рублях *(минимум 100)*:"
    
    def payment():
        return "💳 **Оплата**\n\nВыберите удобный способ оплаты ниже:"