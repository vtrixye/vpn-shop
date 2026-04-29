import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from remnawave.models.webhook import NodeDto
from sqlalchemy import select, func

from database.models import User, Subscription

load_dotenv()
DEFAULT_SUB_USER_ID = os.getenv("DEFAULT_SUB_USER_ID")

class Text:
    def main_menu():
        return "Главное меню"
    
    async def profile(session: AsyncSession, id: int):
        user = await session.get(User, id)
        stmt = select(func.count()).where(Subscription.user_id == id, Subscription.status == "ACTIVE")
        sub_count = await session.scalar(stmt)

        return (
            "Профиль\n\n"
            "<blockquote>"
            f'<tg-emoji emoji-id="5936017305585586269">🛂</tg-emoji> ID: {id}\n'
            f'<tg-emoji emoji-id="5769403330761593044">🛂</tg-emoji> Баланс: {user.balance}\n'
            f'<tg-emoji emoji-id="5778335621491723621">🛂</tg-emoji> Активные подписки: {sub_count}\n'
            "</blockquote>"
        )
    
    def my_subs():
        return "Мои подписки"
    
    def admin_menu():
        return "Панель админа"

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
            '<b>Меню подписок</b>\n\n'
            "<blockquote>"
            f'<tg-emoji emoji-id="5203993413346680064">🛂</tg-emoji> Всего: {total}\n'
            f'<tg-emoji emoji-id="5416081784641168838">🛂</tg-emoji> ACTIVE: {active}\n'
            f'<tg-emoji emoji-id="5411225014148014586">🛂</tg-emoji> EXPIRED: {expired}\n'
            f'<tg-emoji emoji-id="5240241223632954241">🛂</tg-emoji> DISABLED: {disabled}'
            "</blockquote>"
        )
        
        return text
    
    def sub_create(data: dict = {}):
        
        username = data.get("username") if data.get("username") else "(не выбрано)"
        expire_at = data.get("expire_at") if data.get("expire_at") else "(не выбрано)"
        hwid = data.get("hwid") if data.get("hwid") else "0"
        telegram = data.get("telegram") if data.get("telegram") else DEFAULT_SUB_USER_ID

        return (
            "Меню создания подписки\n\n"
            "<blockquote>"
            f'<tg-emoji emoji-id="5814247475141153332">🛂</tg-emoji> username: {username}\n'
            f'<tg-emoji emoji-id="5776213190387961618">🛂</tg-emoji> Истекает через: {expire_at}\n'
            f'<tg-emoji emoji-id="5877318502947229960">🛂</tg-emoji> Устройства: {hwid}\n'
            f'<tg-emoji emoji-id="5879770735999717115">🛂</tg-emoji> Владелец: {telegram}\n'
            "</blockquote>"
        )

    def user_expired():
        return "Подписка истекла"
    
    def user_expires_in_24_hours():
        return "Подписка истекает через сутки"
    
    def node_connection_lost(node: NodeDto):
        text = (
            f"Потеряно соединение с нодой {node.name}"
        )
        return text
    
    def node_connection_restored(node: NodeDto):
        text = (
            f"Восстановлено соединение с нодой {node.name}"
        )
        return text