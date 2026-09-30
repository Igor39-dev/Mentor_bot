"""Handler for /start command."""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from mentor_bot.services.keyboard import build_main_keyboard
from mentor_bot.services.start import build_welcome_message

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Greet the user and show main menu."""
    await state.clear()
    await message.answer(build_welcome_message(), reply_markup=build_main_keyboard())
