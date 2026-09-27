import asyncio
import logging
from typing import Final

from aiogram import Bot, Dispatcher
from sqlalchemy import text

from mentor_bot.config import get_settings
from mentor_bot.db import engine
from mentor_bot.handlers import get_root_router

logger = logging.getLogger(__name__)

LOG_FORMAT: Final[str] = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


async def check_database_connection() -> None:
    """Verify that the application can connect to PostgreSQL."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    logger.info("PostgreSQL connection OK")


async def run_bot() -> None:
    """Create Bot/Dispatcher, verify DB, and start long polling."""
    settings = get_settings()
    if not settings.BOT_TOKEN:
        msg = "BOT_TOKEN is empty; set it in .env"
        raise RuntimeError(msg)

    bot = Bot(token=settings.BOT_TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_router(get_root_router())

    try:
        await check_database_connection()
        logger.info("[---Starting Telegram polling---]")
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
        await engine.dispose()
        logger.info("[---Bot resources closed---]")


def main() -> None:
    """Configure logging and run the bot."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("[---Bot stopped by user---]")



if __name__ == "__main__":
    main()
