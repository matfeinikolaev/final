"""Интерактивный скрипт создания суперпользователя."""
import asyncio
from getpass import getpass

from app.core.database import AsyncSessionLocal, async_engine
from app.core.security import get_password_hash
from app.models.user import User


async def main():
    print("--- Создание суперпользователя ---")
    email = input("Email: ").strip()
    password = getpass("Пароль: ").strip()
    first_name = input("Имя: ").strip()
    last_name = input("Фамилия: ").strip()

    async with AsyncSessionLocal() as db:
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        await db.commit()
        print(f"Суперпользователь {email} создан.")

    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
