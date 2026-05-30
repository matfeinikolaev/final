import asyncio
import logging

from app.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Инициализация данных...")
    logger.info("Инициализация завершена (данных для загрузки нет).")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
