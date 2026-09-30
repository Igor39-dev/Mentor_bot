"""LLM service for answer evaluation using LangChain + OpenRouter."""

import logging

from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class LLMService:
    """Service for evaluating user answers using LLM."""

    def __init__(self, api_key: str, model: str) -> None:
        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            timeout=60.0,
        )

    async def evaluate_answer(self, question_text: str, user_answer: str) -> str:
        """
        Evaluate user's answer to the question using LLM.

        Args:
            question_text: The original question
            user_answer: User's transcribed answer

        Returns:
            LLM feedback on the answer

        Raises:
            Exception: If LLM request fails
        """
        system_prompt = (
            "Ты — опытный преподаватель Python, который проверяет теоретические знания студентов.\n\n"
            "Твоя задача:\n"
            "1. Оценить ответ студента относительно заданного вопроса.\n"
            "2. Указать, что в ответе сказано правильно.\n"
            "3. Указать, что пропущено или объяснено неправильно.\n"
            "4. Дать рекомендации, что нужно улучшить.\n"
            "5. При необходимости привести краткий вариант хорошего ответа.\n\n"
            "НЕ используй числовые оценки или проценты правильности.\n"
            "Отвечай на русском языке, структурированно и понятно."
        )

        user_prompt = f"Вопрос:\n{question_text}\n\nОтвет студента:\n{user_answer}"

        try:
            messages = [
                ("system", system_prompt),
                ("user", user_prompt),
            ]
            response = await self.llm.ainvoke(messages)
            return response.content.strip()
        except Exception as e:
            logger.error("LLM evaluation error: %s", e)
            raise
