import os
from sqlalchemy.ext.asyncio import AsyncSession
from remnawave.models.webhook import NodeDto
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import selectinload

from database.models import User, Subscription
from utils.time import get_remaining_time
from utils.pricing import price_list

DEFAULT_SUB_USER_ID = os.getenv("DEFAULT_SUB_USER_ID")

class Text:
    def main_menu():
        return "## ![🛂](tg://emoji?id=5350738242394137300) Добро пожаловать в GRAPE VPN"
    
    def buy_devices(time: int):
        return (
            "## ![🛂](tg://emoji?id=5983399041197675256) Тарифы  \n\n"
            f'> {price_list["device"][time]}₽ за дополнительное устройство'
        )

    def buy_sub():
        return (
            "## ![🛂](tg://emoji?id=5983399041197675256) Тарифы  \n\n"
            f'>  1 месяц - от {price_list["time"][1]}₽  \n'
            f'> 3 месяца - от {price_list["time"][3]}₽  \n'
            f'> 6 месяцев - от {price_list["time"][6]}₽'
        )
    
    def payment_method(amount: int):
        return (
            f"## ![💳](tg://emoji?id=5445353829304387411) Оплата {amount}₽\n\n"
            "Выберите удобный способ оплаты ниже"
        )


    def payment(amount: int):
        return (
            f"## С вас {amount}₽\n\n"
            "Оплатите по ссылке ниже"
        )

    def info():
        return (
            "## ![](tg://emoji?id=5879785854284599288) Информация\n\n"
        )

    def trial_sub():
        return (
            "## ![🎉](tg://emoji?id=5382194935057372936) Пробный период активирован!\n\n"
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
            "## ![🛂](tg://emoji?id=5257965174979042426) Мои подписки"
        )
    
    def sub_revoke():
        return (
            "## ![](tg://emoji?id=5447644880824181073) Сброс ссылки\n\n"
            "> ![🛂](tg://emoji?id=5447644880824181073) Обратите внимание  \n"
            "> При сбросе ссылки ваше текущее подключение может оборваться!"
        )

    def revoke():
        return (
            "## ![]() Ссылка успешно обновлена\n\n"
            "> Если у вас возникли проблемы с подключением, обратитесь в поддержку @123"
        )

    def sub_opt():
        return (
            "## ![🛂](tg://emoji?id=5258096772776991776) Настройки подписки"
        )

    def transfer_to(user: User | None):
        if user is None:
            text = (
                "![](tg://emoji?id=5872829476143894491) **Пользователь не найден**  \n\n"
                "Чтобы передать подписку, пользователь должен быть зарегестрирован в этом боте. "
                "Попробуйте снова."
            )
        else:
            text = (
                "![](tg://emoji?id=5881702736843511327) **Вы уверены?**  \n"
                f"> Подписка будет передана пользователю **{user.name}** `{user.id}`  \n"
                "> Это действие нельзя отменить!"
            )
        return text
    
    def sub_sq():
        return (
            "## ![🛂](tg://emoji?id=5875431869842985304) Управление протоколами и транспортами  \n\n"
            "> ![🛂](tg://emoji?id=5447644880824181073) Обратите внимание  \n"
            "> Не все приложения поддерживают стабильную работу каждого транспорта и протокола. "
            "Вносите изменения, только если знаете, что делаете."
        )

    def sub_menu(sub: Subscription, total: int):
        remaining = get_remaining_time(sub.expire_at)
        devices = f"{int(total)} из {sub.hwid_device_limit or '∞'}"
        text = (
            "## ![🛂](tg://emoji?id=5258011929993026890) Ваша подписка  \n\n"
            f"> ![🛂](tg://emoji?id=5936017305585586269) Имя: {sub.username}  \n"
            f"> ![🛂](tg://emoji?id=5776213190387961618) Истекает через: {remaining}  \n"
            f"> ![🛂](tg://emoji?id=5877318502947229960) Устройства: {devices}"
        )
        return text
    
    def sub_renew(data: dict):
        text = (
            "## ![🛂](tg://emoji?id=5258096772776991776) Параметры продления  \n\n"
            f"> ![🛂](tg://emoji?id=5936017305585586269) Срок продления: {data['time']}  \n"
            f"> ![🛂](tg://emoji?id=5877318502947229960) Устройства: {data['devices']}  \n\n"
        )

        return text

    def dev_renew(amount: int):
        return (
            "## ![🛂](tg://emoji?id=5258096772776991776) Устройства  \n\n"
            "> Стоимость добавления устройства рассчитывается пропорционально "
            "оставшемуся сроку Вашей подписки. При этом минимум - 39₽, а "
            "максимум - 149₽.  \n"
            f"Ваша цена: {amount}₽"
        )

    def admin_menu():
        return (
            "## ![🛂](tg://emoji?id=5258096772776991776) Панель админа"
        )

    def stats():
        return (
            "## ![🛂](tg://emoji?id=5258096772776991776) Статистика"
        )

    async def users_stats(session: AsyncSession) -> str:
        # Общее количество пользователей
        total_result = await session.execute(
            select(func.count(User.id))
        )
        total = total_result.scalar()
        
        # Количество пользователей, у которых trial = True (активен пробный период)
        trial_result = await session.execute(
            select(func.count(User.id))
            .where(User.trial == False)
        )
        
        # Количество пользователей с платной подпиской (хотя бы одна подписка с tag != "TRIAL")
        paid_result = await session.execute(
            select(func.count(distinct(User.id)))
            .join(User.subscriptions)
            .where(
                Subscription.status == "ACTIVE",  # только активные подписки
                Subscription.tag != "TRIAL"       # исключаем пробные
            )
        )
        paid_count = paid_result.scalar() or 0
         
        # Количество пользователей с любой активной подпиской (status = "ACTIVE")
        any_active_result = await session.execute(
            select(func.count(distinct(User.id)))
            .join(User.subscriptions)
            .where(Subscription.status == "ACTIVE")
        )
        any_active_count = any_active_result.scalar() or 0
        
        # Заблокированные пользователи
        blocked_result = await session.execute(
            select(func.count(User.id))
            .where(User.blocked == True)
        )
        blocked_count = blocked_result.scalar()
        
        # Администраторы
        admin_result = await session.execute(
            select(func.count(User.id))
            .where(User.admin == True)
        )
        admin_count = admin_result.scalar()
        
        
        text = (
            '## ![📊](tg://emoji?id=5190806721286657692) Статистика пользователей\n\n'
            '| Показатель | Количество |\n'
            '| :--- | :---: |\n'
            f'| ![📊](tg://emoji?id=5203993413346680064) **Всего пользователей** | `{total}` |\n'
            f'| ![🔘](tg://emoji?id=5416081784641168838) **Активировали TRIAL** | `{trial_result}` |\n'
            f'| ![🟢](tg://emoji?id=5210952531676504517) **Платная подписка** | `{paid_count}` |\n'
            f'| ![🔘](tg://emoji?id=5190806721286657692) **Всего с активной подпиской** | `{any_active_count}` |\n'
            f'| ![🚫](tg://emoji?id=5240241223632954241) **Заблокированы** | `{blocked_count}` |\n'
            f'| ![👑](tg://emoji?id=5210952531676504517) **Администраторы** | `{admin_count}` |\n'
        )
        
        return text

    async def subs_stats(session: AsyncSession) -> str:
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
            '## ![📊](tg://emoji?id=5190806721286657692) Статистика подписок\n\n'
            '| Статус | Количество |\n'
            '| :--- | :---: |\n'
            f'| ![📊](tg://emoji?id=5203993413346680064) **Всего** | `{total}` |\n'
            f'| ![🟢](tg://emoji?id=5416081784641168838) **ACTIVE** | `{active}` |\n'
            f'| ![🔴](tg://emoji?id=5411225014148014586) **EXPIRED** | `{expired}` |\n'
            f'| ![🔘](tg://emoji?id=5240241223632954241) **DISABLED** | `{disabled}` |'
        )
      
        return text
       
    def sub_trans():
        return (
            "Введите Telegram ID пользователя, которому хотите передать подписку  \n"
            "> Пользователь должен быть зарегестрирован в боте. "
            "Для этого нужно только отправить команду /start"
        )
    
    def sub_dev(total: int):

        text = "## ![🕘](tg://emoji?id=5877318502947229960) Ваши устройства\n\n"

        if total == 0:
            text += "Похоже, у вас нет подключенных устройств"
        else:
            text += "Нажмите на кнопку с устройством, чтобы удалить его"

        return text

    def user_expired(sub: Subscription):
        return (
            f"## ![🕘](tg://emoji?id=5776213190387961618) Подписка истекла\n\n"
            f"Время действия подписки `{sub.username}` подошло к концу."
        )
    
    def user_expiration(sub: Subscription, offset: int):
        return (
            f"## ![🚨](tg://emoji?id=5458603043203327669) Внимание\n\n"
            f"Подписка `{sub.username}` истекает через **{abs(offset)} часа**!"
        )            

    def user_expires_in_24_hours(sub: Subscription):
        return (
            f"## ![🚨](tg://emoji?id=5458603043203327669) Внимание\n\n"
            f"Подписка `{sub.username}` истекает через **24 часа**!"
        )
    
    def node_connection_lost(node: NodeDto):
        return f"🚨 **Потеряно соединение!**\n\nНода: `{node.name}` недоступна."
    
    def node_connection_restored(node: NodeDto):
        return f"✅ **Соединение восстановлено!**\n\nНода: `{node.name}` снова в строю."
    
    def invoice_created(invoice):
        return (
            "## ![🧾](tg://emoji?id=5197269100878907942) Счет на оплату\n\n"
            f"Сумма к оплате: **{invoice.amount} {invoice.fiat}**\n\n"
            "Перейдите по ссылке ниже для завершения платежа:"
        )
    
    def invoice_paid():
        return (   
            "## ![🎉](tg://emoji?id=5201691993775818138) Оплата прошла успешно!\n\n"
            "Средства зачислены на ваш баланс."
        )
    
    def top_up():
        return (
            "## ![💳](tg://emoji?id=5190741648237161191) Пополнение баланса\n\n"
            "Введите сумму пополнения в рублях *(минимум 100)*:"
        )
    
    def pay_stars():
        return (
            "## ![💳](tg://emoji?id=5445353829304387411) Telegram Stars\n\n"
            "Оплатите по ссылке ниже"
        )
    
    def state_error():
        return (
            "Произошла ошибка. Поробуйте перезайти в эту вкладку."
        )
    
    def unknown_error():
        return (
            "Произошла неизвестная ошибка...\nПовторите попытку или обратитесь в поддержку 🫤"
        )