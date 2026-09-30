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
