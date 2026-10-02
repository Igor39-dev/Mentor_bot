"""Script to add test questions to the database."""

import asyncio
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine

from mentor_bot.config import get_settings
from mentor_bot.db.models import Question

questions = [
# Основы Python
{
    "text": "Какие типы данных есть в Python и на какие категории их можно разделить? Чем отличаются кортеж и список? Какая сложность операции добавления элемента в список?",
    "category": "Основы Python",
},
# БД
{
    "text": "Что такое БД и СУБД? Какие БД называют реляционными? Как устанавливаются связи между таблицами и какие они бывают?",
    "category": "БД",
},
# Django
{
    "text": "Что такое Django и для чего используется? Какова архитектура Django, какие основные компоненты она включает?",
    "category": "Django",
},
# Asyncio
{
    "text": "Что такое конкурентность и параллельность? Какие задачи решают многопоточность, многопроцессность и асинхронность?",
    "category": "Asyncio",
},
# FastAPI
{
    "text": "Что такое FastAPI и для каких задач он предназначен?",
    "category": "FastAPI",
},

# Pytest
{
    "text": "Что такое Pytest и каковы его преимущества?",
    "category": "Pytest",
},
]

async def add_test_questions() -> None:
    """Add test questions to the database."""
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, echo=True)

    now = datetime.utcnow()

    questions_to_insert = [
        {
            **question,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
        for question in questions
    ]

    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: sync_conn.execute(
                Question.__table__.insert(),
                questions_to_insert,
            )
        )

    await engine.dispose()

    print(f"Успешно добавлено вопросов: {len(questions_to_insert)}")


if __name__ == "__main__":
    asyncio.run(add_test_questions())
