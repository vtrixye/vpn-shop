from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    InputRichMessage
    )
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from telegram.filters import ChatTypeFilter, IsAdmin
from database.models import User
from database.crud import *
from telegram.text import Text
import telegram.keyboards.admin as kb

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private', 'group']), IsAdmin())
admin_router.callback_query.filter(ChatTypeFilter(['private', 'group']), IsAdmin())

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    text = Text.admin_menu()
    keyboard = kb.admin_menu()
    await message.answer_rich(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@admin_router.message(Command("test"))
async def cmd_test(message: Message):
    test_markdown = (
        "# 👑 Нативный заголовок H1 (RichBlockSectionHeading)\n"
        "## Подзаголовок уровня H2\n\n"
        "Это стандартный параграф текста. Текст в RichMessage рендерится "
        "чуть крупнее обычного сообщения в Telegram. Внутри него работают привычные "
        "**жирный**, *курсив*, `код` и ||спойлер||.\n\n"
        
        "---" # Превратится в горизонтальную линию (RichBlockDivider)
        "\n\n"
        
        "### 📊 1. Тест нативной таблицы (RichBlockTable)\n"
        "| Название фичи | Статус | Версия |\n"
        "| :--- | :---: | :---: |\n"
        "| Markdown таблицы | ✅ Работает | 3.29 |\n"
        "| Блочная верстка |  Доступно | API 10.1 |\n"
        "| Без экранирования | 🔥 Идеально | Любая |\n\n"
        
        "### 📝 2. Тест списков (RichBlockList)\n"
        "* Обычный маркированный список.\n"
        "* Второй пункт списка.\n"
        "1. Нумерованный список.\n"
        "2. Следующий упорядоченный элемент.\n"
        "- [x] Интерактивный список задач (Task List) — выполнен.\n"
        "- [ ] Задача на будущее — не выполнена.\n\n"
        
        "### 📐 3. Тест математических выражений (LaTeX)\n"
        "Благодаря блоку формул, уравнения теперь рендерятся красиво:\n"
        "$$E = mc^2$$\n"
        "А также интегралы внутри текста: $$\\int_a^b x^2 dx$$\n\n"
        
        "### 💬 4. Тест цитат и спойлеров блоков\n"
        "> Это большая многострочная цитата (RichBlockBlockQuotation).\n"
        "> Она выделяется красивой вертикальной линией слева.\n\n"
        
        "<details>\n"
        "<summary>Развернуть детали (RichBlockDetails)</summary>\n"
        "Здесь прячется скрытый текст, который раскрывается только по тапу пользователя!\n"
        "</details>"
    )

    await message.answer_rich(rich_message=InputRichMessage(markdown=test_markdown))

@admin_router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    await callback.answer()
    text = Text.admin_menu()
    keyboard = kb.admin_menu()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "subs_control")
async def subs_control(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()
    await state.clear()
    text = await Text.subs_control(session)
    keyboard = kb.subs_control()
    try:
        await callback.message.edit_text(
            rich_message=InputRichMessage(markdown=text),
            reply_markup=keyboard
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e).lower():
            pass
        else:
            raise


class CreateSubState(StatesGroup):
    edit = State()
    username = State()
    expire_at = State()
    hwid = State()
    telegram = State()

@admin_router.callback_query(F.data == "sub_create")
async def sub_create(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    text = Text.sub_create()
    keyboard = kb.sub_create()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )
    await state.set_state(CreateSubState.edit)

@admin_router.callback_query(F.data == "sub_create_state")
async def sub_create_state(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    text = Text.sub_create(data)
    keyboard = kb.sub_create()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "set_username")
async def set_username(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    text = Text.set_username()
    keyboard = kb.set_username()
    await callback.message.edit_text(
        rich_message=InputRichMessage(markdown=text),
        reply_markup=keyboard
    )
    await state.update_data(mes_id = callback.message.message_id)
    await state.set_state(CreateSubState.username)

@admin_router.message(CreateSubState.username, F.text)
async def username_state(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(username=message.text)
    data = await state.get_data()
    text = Text.sub_create(data)
    keyboard = kb.sub_create()
    await message.delete()
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data.get("mes_id"),
        rich_message=InputRichMessage(markdown=text))
    await state.set_state(CreateSubState.edit)

    