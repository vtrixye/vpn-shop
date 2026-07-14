# alembic/env.py
import asyncio
from logging.config import fileConfig
import os
import sys
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ===== ВАЖНО: Добавляем корневую папку в Python path =====
# Т.к. alembic находится в папке app/alembic, а нам нужен доступ к app/
# Поднимаемся на один уровень вверх
sys.path.insert(0, str(Path(__file__).parent.parent))

# ===== Импортируем ваши модели =====
from database.models import Base
from database import engine, session_maker

# ===== Загружаем переменные окружения из .env =====
from dotenv import load_dotenv

# Ищем .env в корне проекта (папка app)
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Загружен .env из {env_path}")
else:
    load_dotenv()
    print("⚠️ .env не найден, используем системные переменные")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ===== Функция получения URL базы данных =====
def get_database_url():
    """Формирует URL для подключения к БД из переменных окружения"""
    
    # Способ 1: Полный URL
    if os.getenv('DATABASE_URL'):
        return os.getenv('DATABASE_URL')
    
    # Способ 2: Отдельные переменные (как у вас в database/__init__.py)
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_NAME']
    if all(os.getenv(var) for var in required_vars):
        return (
            f"postgresql+asyncpg://"
            f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
        )
    
    # Способ 3: Значения по умолчанию (для разработки)
    print("⚠️ ВНИМАНИЕ: Используются значения по умолчанию для БД!")
    return "postgresql+asyncpg://postgres:postgres@localhost:5432/vpn_shop"

# ===== Устанавливаем URL в конфиг =====
db_url = get_database_url()
config.set_main_option('sqlalchemy.url', db_url)
print(f"🔗 Подключение к БД: {db_url.replace(os.getenv('DB_PASSWORD', ''), '****') if os.getenv('DB_PASSWORD') else db_url}")

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with a connection"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine"""
    
    # Создаем асинхронный движок
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()