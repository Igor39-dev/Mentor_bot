"""Handlers for knowledge check flow."""

import logging
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from mentor_bot.config import get_settings
from mentor_bot.db.session import get_async_session
from mentor_bot.services.keyboard import build_main_keyboard
from mentor_bot.services.question import QuestionService
from mentor_bot.services.stt import STTService
from mentor_bot.services.telegram import download_voice_file
from mentor_bot.states import KnowledgeCheckStates

router = Router(name="knowledge_check")
logger = logging.getLogger(__name__)

TEMP_AUDIO_DIR = Path("temp_audio")


@router.message(F.text == "Проверка знаний")
async def start_knowledge_check(message: Message, state: FSMContext) -> None:
    """Start knowledge check: get random question and wait for voice answer."""
    await state.clear()

    async with get_async_session() as session:
        question_service = QuestionService(session)
        question = await question_service.get_random_active_question()

    if not question:
        await message.answer("К сожалению, вопросы пока не загружены в базу данных.")
        return

    await state.set_state(KnowledgeCheckStates.waiting_voice_answer)
    await state.update_data(question_id=question.id, question_text=question.text)

    await message.answer(f"Вопрос:\n\n{question.text}\n\nОтправьте голосовой ответ.")


@router.message(KnowledgeCheckStates.waiting_voice_answer, F.voice)
async def process_voice_answer(message: Message, state: FSMContext, bot: Bot) -> None:
    """Process voice answer: download, transcribe, show text."""
    if not message.voice:
        return

    data = await state.get_data()
    question_text = data.get("question_text", "")

    audio_path: Path | None = None

    try:
        # Download voice file
        audio_path = await download_voice_file(bot, message.voice, TEMP_AUDIO_DIR)

        # Transcribe audio
        settings = get_settings()
        stt_service = STTService(api_key=settings.OPENROUTER_API_KEY, model=settings.OPENROUTER_STT_MODEL)
        transcribed_text = await stt_service.transcribe_audio(audio_path)

        if not transcribed_text:
            await message.answer("Не удалось распознать текст из голосового сообщения. Попробуйте ещё раз.")
            return

        # Show transcribed text
        await state.clear()
        await message.answer(
            f"Ваш вопрос:\n{question_text}\n\n"
            f"Ваш ответ (распознанный текст):\n{transcribed_text}\n\n"
            "Распознавание завершено успешно!",
            reply_markup=build_main_keyboard(),
        )

    except Exception as e:
        logger.error("Error processing voice message: %s", e)
        await message.answer(
            "Произошла ошибка при обработке голосового сообщения. Попробуйте ещё раз.",
            reply_markup=build_main_keyboard(),
        )
        await state.clear()

    finally:
        # Clean up temporary file
        if audio_path and audio_path.exists():
            audio_path.unlink()
            logger.info("Deleted temporary audio file: %s", audio_path)


@router.message(KnowledgeCheckStates.waiting_voice_answer)
async def invalid_answer_format(message: Message) -> None:
    """Handle non-voice messages when voice is expected."""
    await message.answer("Пожалуйста, отправьте голосовое сообщение с вашим ответом.")
