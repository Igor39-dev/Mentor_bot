"""Repository for Question model."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from mentor_bot.db.models import Question


class QuestionRepository:
    """Repository for managing questions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_random_active_question(self) -> Question | None:
        """Get a random active question from the database."""
        stmt = select(Question).where(Question.is_active == True).order_by(func.random()).limit(1)  # noqa: E712
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_random_active_question_by_category(self, category: str) -> Question | None:
        """Get a random active question from the database by category."""
        stmt = (
            select(Question)
            .where(Question.is_active == True, Question.category == category)  # noqa: E712
            .order_by(func.random())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_question_by_id(self, question_id: int) -> Question | None:
        """Get question by ID."""
        stmt = select(Question).where(Question.id == question_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
