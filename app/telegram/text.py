from remnawave.models.webhook import NodeDto

class Text:
    def main_menu():
        return "Главное меню"
    
    def profile():
        return "Профиль"
    
    def admin_menu():
        return "Панель админа"
    
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