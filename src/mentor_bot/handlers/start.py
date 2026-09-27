"""Handler for the /start command."""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from mentor_bot.services.start import build_welcome_message

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Reply with a welcome message when the user sends /start."""
    await message.answer(build_welcome_message())
