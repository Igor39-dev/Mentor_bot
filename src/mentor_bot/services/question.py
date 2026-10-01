"""Service layer for question management."""

from sqlalchemy.ext.asyncio import AsyncSession

from mentor_bot.db.models import Question
from mentor_bot.repositories.question import QuestionRepository


class QuestionService:
    """Service for question-related business logic."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = QuestionRepository(session)

    async def get_random_active_question(self) -> Question | None:
        """Get a random active question."""
        return await self.repository.get_random_active_question()

    async def get_question_by_id(self, question_id: int) -> Question | None:
        """Get question by ID."""
        return await self.repository.get_question_by_id(question_id)

    async def get_random_active_question_by_category(self, category: str) -> Question | None:
        """Get a random active question by category."""
        return await self.repository.get_random_active_question_by_category(category)
