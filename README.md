## Правила написания кода

**✅ Хорошо:**
```python
async def orm_create_user(session: AsyncSession,  user_id: int, name: str, username: str = None):
    '''Создание нового пользователя в базе данных'''
    user = User(
        user_id=user_id, 
        name=name, 
        username=username,
        balance=0,
        admin=False,
        blocked=False
    )
    session.add(user)
    await session.commit()
```
**❌ Плохо:**
```python
async def bullshit(session,user_id,name,username):
    user = User(user_id=user_id, name=name, username=username,balance=0,admin=False,blocked=False)
    session.add(user)
    await session.commit()
```
---
**✅ Хорошо:**
```python
import os
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import ChatTypeFilter, IsAdmin
from bot.menu_texts import Texts
import bot.keyboards as kb
```
**❌ Плохо:**
```python
# вперемешку
from sqlalchemy.ext.asyncio import AsyncSession
import os
import bot.keyboards as kb
from bot.menu_texts import Texts
import sys 
from datetime import datetime
from aiogram import Router, F
```
---
**✅ Хорошо:**
```python
user = await session.get(User, message.from_user.id)
data = await state.get_data()
text = "Please enter a valid amount (numbers only)"
```
**❌ Плохо:**
```python
a = await session.get(User, message.from_user.id)
b = await state.get_data()
c = "Please enter a valid amount (numbers only)"
```
