"""Script to add test questions to the database."""

import asyncio
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine

from mentor_bot.config import get_settings
from mentor_bot.db.models import Question


async def add_test_questions() -> None:
    """Add test questions to the database."""
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, echo=True)

    now = datetime.utcnow()

    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: sync_conn.execute(
                Question.__table__.insert(),
                [
                    {
                        "text": "Какие типы данных есть в Python?",
                        "is_active": True,
                        "created_at": now,
                        "updated_at": now,
                    },
                    {
                        "text": "Объясните разницу между списком (list) и кортежем (tuple) в Python.",
                        "is_active": True,
                        "created_at": now,
                        "updated_at": now,
                    },
                ],
            )
        )

    await engine.dispose()
    print("Тестовые вопросы успешно добавлены!")


if __name__ == "__main__":
    asyncio.run(add_test_questions())
