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
    test_markdown = ("""
        **bold text**
        __bold text__
        *italic text*
        _italic text_
        ~~strikethrough text~~
        `inline fixed-width code`
        ==marked text==
        ||spoiler||

        [inline URL](https://t.me/)
        [inline e-mail](mailto:user@example.com)
        [inline phone number](tel:+123456789)
        [inline mention of a user](tg://user?id=123456789)
        ![👍](tg://emoji?id=5368324170671202286)
        ![22:45 tomorrow](tg://time?unix=1647531900&format=wDT)
        $x^2 + y^2$
        \#hashtag $USD +12345678901, card: 4242 4242 4242 4242, https://t.me t.me a@t.me /command @username
        all the text above was on the same line

        # Heading 1
        ## Heading 2
        ### Heading 3
        #### Heading 4
        ##### Heading 5
        ###### Heading 6

        Paragraph text

        ```python
        print('pre-formatted fixed-width code block written in the Python programming language')
        ```

        ---

        - unordered list item
        * unordered list item
        + unordered list item

        1. ordered list item
        2. ordered list item

        - [ ] task list item
        - [x] completed task list item

        >Block quotation started
        >
        >Block quotation continued on the next line
        >Block quotation continued on the same line
        >
        >The last line of the block quotation

        ![](https://telegram.org/example/photo.jpg)
        ![](https://telegram.org/example/video.mp4)
        ![](https://telegram.org/example/audio.mp3)
        ![](https://telegram.org/example/audio.ogg)
        ![](https://telegram.org/example/animation.gif)

        ![](https://telegram.org/example/photo.jpg "Photo caption")
        ![](https://telegram.org/example/video.mp4 "Video caption")
        ![](https://telegram.org/example/audio.mp3 "Audio caption")
        ![](https://telegram.org/example/audio.ogg "Voice note caption")
        ![](https://telegram.org/example/animation.gif "Animation caption")

        | Header 1 | Header 2 |
        |:---------|:--------:|
        | left     | center   |

        Text with a reference[^id1] and another one[^id2].

        [^id1]: Definition of the first footnote.
        [^id2]: Definition of the second footnote.

        $$E = mc^2$$

        ```math
        E = mc^2
        ```

        ## Example Nested Syntax Report for _Q1_
        Intro with <u>underlined text</u>, ==marked text==, and $x^2 + y^2$.
        **Bold _italic <u>underlined italic bold</u> italic_ bold**
        <u>In inline tags, nested **markdown** is parsed</u>
        >Quote with **bold text, ~~strikethrough, and <tg-spoiler>spoiler</tg-spoiler>~~**, plus [a link](https://t.me/).

        - List item with `code`, <sup>superscript</sup>, <sub>subscript</sub>, and a footnote[^note]
        - Another item with **bold <tg-spoiler><code>spoiler code</code></tg-spoiler>**
        - Another item with ~~strikethrough and <ins>inserted text</ins>~~

        | Metric | Value |
        |:-------|------:|
        | Speed  | **42** <sup>ms</sup> |
        | Status | <tg-spoiler>ready</tg-spoiler> |

        [^note]: Footnote with _italic text_ and <u>HTML underline</u>.

        ---

        # Details blocks can contain Markdown content:

        <details open><summary>Summary with **bold text**</summary>

        ### Details heading
        - List item with _italic text_
        - List item with <tg-spoiler>spoiler</tg-spoiler>

        </details>

        # Collages and slideshows can contain Markdown media blocks:

        <tg-collage>

        ![](https://telegram.org/example/photo.jpg)
        ![](https://telegram.org/example/video.mp4)

        </tg-collage>

        <tg-slideshow>

        ![](https://telegram.org/example/photo.jpg)
        ![](https://telegram.org/example/video.mp4)

        </tg-slideshow>"""
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

    