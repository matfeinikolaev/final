"""Creates the database if it doesn't exist. Run before alembic upgrade head."""
import asyncio
import asyncpg
from app.core.config import settings


async def main():
    # Подключаемся к системной БД postgres чтобы создать нашу
    sys_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
    conn = await asyncpg.connect(sys_url)
    exists = await conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname='{settings.DB_NAME}'")
    if not exists:
        await conn.execute(f'CREATE DATABASE "{settings.DB_NAME}"')
        print(f"Database '{settings.DB_NAME}' created.")
    else:
        print(f"Database '{settings.DB_NAME}' already exists.")
    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
