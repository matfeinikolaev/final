import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import settings

# Импортируем модели, чтобы Alembic увидел их metadata
from app.models.user import User
from app.models.job import Job
from app.models.resume import Resume
from app.models.category import Category
from app.models.vacancy import Vacancy

# Получаем конфиг Alembic
config = context.config

# Настраиваем логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ВАЖНО: Переопределяем URL базы данных значением из настроек приложения
# Это гарантирует, что Alembic использует тот же URL, что и само приложение
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Указываем metadata, где хранятся наши модели.
# Используем User.metadata, так как User точно привязан к правильному Base.
target_metadata = User.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме (без подключения к БД)."""
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
    """Вспомогательная функция для запуска миграций в online режиме."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме (с подключением к БД)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
