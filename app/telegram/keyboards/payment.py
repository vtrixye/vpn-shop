from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User

def buy_sub():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="1 месяц", callback_data="buy_month_1", icon_custom_emoji_id="5778605968208170641"),
        InlineKeyboardButton(text="3 месяца", callback_data="buy_month_3", icon_custom_emoji_id="5776213190387961618"),
        InlineKeyboardButton(text="6 месяцев", callback_data="buy_month_6", icon_custom_emoji_id="5778605968208170641"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1, 1, 1)
    return keyboard.as_markup()

async def buy_devices(state: FSMContext):
    keyboard = InlineKeyboardBuilder()

    data = await state.get_data()

    for i in range(1, 7):
        emoji = "5778335621491723621" if data["devices"] == i else "5994324703559290598"
        keyboard.add(
            InlineKeyboardButton(text=f"{i} устр.", callback_data=f"buy_dev_{i}", icon_custom_emoji_id=emoji),
        )

    keyboard.add(
        InlineKeyboardButton(text=f"Оплатить {data['amount']}₽", icon_custom_emoji_id="5445353829304387411", callback_data="pay_sub"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data=f"buy_sub")   
    )

    keyboard.adjust(2, 2, 2, 1, 1)
    return keyboard.as_markup()

def cryptopay_invoice(url: str, amount: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text=f"Оплатить {amount}₽", icon_custom_emoji_id="5258513401784573443", url=url),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()

def invoice_paid() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="main_menu")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

def top_up() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="100₽", callback_data="top_up_100"),
        InlineKeyboardButton(text="200₽", callback_data="top_up_200"),
        InlineKeyboardButton(text="300₽", callback_data="top_up_300"),
        InlineKeyboardButton(text="500₽", callback_data="top_up_500"),
        InlineKeyboardButton(text="Назад", callback_data="profile", icon_custom_emoji_id="5258236805890710909")
    )

    keyboard.adjust(2, 2, 1)

    return keyboard.as_markup()

def payment(back: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text="СБП", icon_custom_emoji_id="5363972466857252756", callback_data="12345"),
        InlineKeyboardButton(text="CryptoBot", icon_custom_emoji_id="5361914370068613491", callback_data="12345"),
        InlineKeyboardButton(text="Telegram Stars", icon_custom_emoji_id="5897792062291449826", callback_data="12345"),
        InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data=back),
    )

    keyboard.adjust(1, 1, 1, 1)
    
    return keyboard.as_markup()

def pay_stars(price: int, invoice_link: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=f"Pay {price}⭐️",url=invoice_link, icon_custom_emoji_id="5260416304224936047"),
        InlineKeyboardButton(text="Назад", callback_data="top_up", icon_custom_emoji_id="5258236805890710909")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

