"""Application entry point."""

import asyncio
import logging
from typing import Final

from sqlalchemy import text

from mentor_bot.config import get_settings
from mentor_bot.db import engine

logger = logging.getLogger(__name__)

LOG_FORMAT: Final[str] = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


async def check_database_connection() -> None:
    """Verify that the application can connect to PostgreSQL."""
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        logger.info("PostgreSQL connection OK")
    finally:
        await engine.dispose()


def main() -> None:
    """Configure logging, load settings, and verify database connectivity."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    settings = get_settings()
    model = settings.OPENROUTER_MODEL or "not configured"
    logger.info("Mentor bot entry point ready (openrouter_model=%s)", model)

    asyncio.run(check_database_connection())


if __name__ == "__main__":
    main()
