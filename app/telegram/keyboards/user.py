from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    CopyTextButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from remnawave.models.hwid import GetUserHwidDevicesResponseDto
import uuid as uuid_lib

from services.remnawave_service.enums import InternalSquad
from database.models import User, Subscription
from utils.time import get_remaining_time
from utils.logger import get_logger

logger = get_logger(__name__)

async def main_menu(session: AsyncSession, id: int) -> InlineKeyboardMarkup:
    user = await session.get(User, id)
    keyboard = InlineKeyboardBuilder()
    
    if user.trial:
        keyboard.row(InlineKeyboardButton(text="Пробный период", icon_custom_emoji_id="5258226313285607065", callback_data="trial_sub"))
    
    keyboard.row(InlineKeyboardButton(text="Купить", icon_custom_emoji_id="5359805631320571519", callback_data="buy_sub"))
    keyboard.row( InlineKeyboardButton(text="Профиль", icon_custom_emoji_id="5258011929993026890", callback_data="profile"))

    keyboard.row(
        InlineKeyboardButton(text="Информация",icon_custom_emoji_id="5258503720928288433", callback_data="info"),
        InlineKeyboardButton(text="Канал", icon_custom_emoji_id="5260268501515377807", callback_data="chaneltest")
    )
    if user.admin:
        keyboard.row(InlineKeyboardButton(text="Админ панель", icon_custom_emoji_id="5258096772776991776", callback_data="admin_menu"))
    
    return keyboard.as_markup()

def info() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Политика конфиденциальности", icon_custom_emoji_id="5956561916573782596", url="https://telegra.ph/Politika-konfidencialnosti-06-21-31"),
        InlineKeyboardButton(text="Пользовательское соглашение", icon_custom_emoji_id="5956561916573782596", url="https://telegra.ph/Polzovatelskoe-soglashenie-04-01-19"),
        InlineKeyboardButton(text="Поддержка", icon_custom_emoji_id="5884123981706956210", url="https://t.me/test111support"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu"),
    )

    keyboard.adjust(1, 1, 1, 1)
    return keyboard.as_markup()

def trial_sub() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu"),
    )
    
    return keyboard.as_markup()

def profile() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Пополнить баланс", icon_custom_emoji_id="5258204546391351475", callback_data="1top_up"),
        InlineKeyboardButton(text="Мои подписки", icon_custom_emoji_id="5257965174979042426", callback_data="my_subs"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu"),
    )
    
    keyboard.adjust(1, 1, 1)
    return keyboard.as_markup()

async def my_subs(session: AsyncSession, id: int) -> InlineKeyboardMarkup:
    subs = await session.execute(
        select(Subscription).where(Subscription.user_id == id)
    )

    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Купить", icon_custom_emoji_id="5359805631320571519", callback_data="buy_sub"))

    for sub in subs.scalars():

        icon = "5416081784641168838" if sub.status == "ACTIVE" else "5411225014148014586"
        time = get_remaining_time(sub.expire_at)

        keyboard.add(
            InlineKeyboardButton(
                text=f"{sub.username} ({time})",
                icon_custom_emoji_id=icon,
                callback_data=f"sub:{sub.short_uuid}"
            )
        )
    
    keyboard.add(InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="profile"))

    keyboard.adjust(1, 1, 1, 1, 1)

    return keyboard.as_markup()

def sub_menu(sub: Subscription) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Продлить", callback_data="renew_sub", icon_custom_emoji_id="5776213190387961618"),
        InlineKeyboardButton(text="Копировать ссылку", copy_text=CopyTextButton(text=sub.subscription_url), icon_custom_emoji_id="5258477770735885832"),
        InlineKeyboardButton(text="Устройства", callback_data=f"sub:dev:{sub.short_uuid}", icon_custom_emoji_id="5877318502947229960"),
        InlineKeyboardButton(text="Настройки", callback_data=f"sub:opt:{sub.short_uuid}", icon_custom_emoji_id="5258096772776991776"),
        InlineKeyboardButton(text="Назад", callback_data="my_subs", icon_custom_emoji_id="5258236805890710909")
    )

    keyboard.adjust(1, 1, 1, 1)
    return keyboard.as_markup()

def sub_opt(sub: Subscription) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Протоколы", callback_data=f"sub:sq:{sub.short_uuid}", icon_custom_emoji_id="5875431869842985304"),
        InlineKeyboardButton(text="Передать подписку", callback_data=f"sub:trans:{sub.short_uuid}", icon_custom_emoji_id="5954175920506933873"),
        InlineKeyboardButton(text="Сброс ссылки", callback_data=f"sub:revoke:{sub.short_uuid}", icon_custom_emoji_id="5877465816030515018"),
        InlineKeyboardButton(text="Назад", callback_data=f"sub:{sub.short_uuid}", icon_custom_emoji_id="5258236805890710909")
    )

    keyboard.adjust(1, 1, 1, 1)
    return keyboard.as_markup()

def sub_trans(sub: Subscription):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Назад", callback_data=f"sub:opt:{sub.short_uuid}", icon_custom_emoji_id="5258236805890710909")
    )

    return keyboard.as_markup()  

def transfer_to(short_uuid: str, user: User | None = None):
    keyboard = InlineKeyboardBuilder()

    if user is not None:
        keyboard.row(
            InlineKeyboardButton(text="Подтвердить", callback_data=f"trans:{user.id}:{short_uuid}", icon_custom_emoji_id="5776375003280838798")
        )

    keyboard.row(
        InlineKeyboardButton(text="Назад", callback_data=f"sub:opt:{short_uuid}", icon_custom_emoji_id="5258236805890710909")
    )

    return keyboard.as_markup()

def sub_sq(sub: Subscription) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for squad in InternalSquad:
        if squad is InternalSquad.CDN: continue
        emoji = "5778335621491723621" if uuid_lib.UUID(squad.value) in sub.squads else "5994324703559290598"
        keyboard.row(
            InlineKeyboardButton(text=squad.name, callback_data=f"sub:set:sq:{squad.name}:{sub.short_uuid}", icon_custom_emoji_id=emoji)
        )
    
    keyboard.row(
        InlineKeyboardButton(text="Назад", callback_data=f"sub:opt:{sub.short_uuid}", icon_custom_emoji_id="5258236805890710909")
    )

    return keyboard.as_markup()

def sub_dev(hw: GetUserHwidDevicesResponseDto, short_uuid: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for dev in hw.devices:
        text = f"{dev.user_agent.split('/')[0].upper()} {dev.device_model}"
        text = text[:27] + "..." if len(text) > 30 else text
        keyboard.row(
            InlineKeyboardButton(
                text=text,
                icon_custom_emoji_id="5258130763148172425",
                callback_data=f"dev:{dev.hwid}"
            )
        )
    
    keyboard.row(
        InlineKeyboardButton(text="Назад", callback_data=f"sub:{short_uuid}", icon_custom_emoji_id="5258236805890710909"),
    )

    return keyboard.as_markup()

def delete_button(text = "OK"):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text=text, icon_custom_emoji_id="5260416304224936047", callback_data="delete_message")
    )
    
    return keyboard.as_markup()