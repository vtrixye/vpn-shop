import os
from dotenv import load_dotenv

from remnawave.models.webhook import NodeDto

load_dotenv()
DEFAULT_SUB_USER_ID = os.getenv("DEFAULT_SUB_USER_ID")

class Text:
    def main_menu():
        return "Главное меню"
    
    def profile():
        return "Профиль"
    
    def my_subs():
        return "Мои подписки"
    
    def admin_menu():
        return "Панель админа"
    
    def subs_control():
        return "Управление подписками"
    
    def sub_create(data: dict = {}):
        
        username = data.get("username") if data.get("username") else "(не выбрано)"
        expire_at = data.get("expire_at") if data.get("expire_at") else "(не выбрано)"
        hwid = data.get("hwid") if data.get("hwid") else "0"
        telegram = data.get("telegram") if data.get("telegram") else DEFAULT_SUB_USER_ID

        return (
            "Меню создания подписки\n\n"

            f"username: {username}"
            f"expire_at: {expire_at}"
            f"hwid limit: {hwid}"
            f"telegram id: {telegram}"
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