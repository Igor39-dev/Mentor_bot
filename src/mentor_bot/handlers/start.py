"""Handler for /start and a temporary Redis FSM smoke test."""

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from mentor_bot.services.start import (
    FSM_DEMO_VALUE,
    build_fsm_demo_prompt,
    build_fsm_demo_result,
    build_welcome_message,
)
from mentor_bot.states import FsmDemoStates

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Greet the user and store a temporary value in FSM (Redis)."""
    await state.clear()
    await state.set_state(FsmDemoStates.waiting_next_message)
    await state.update_data(demo_value=FSM_DEMO_VALUE)

    await message.answer(build_welcome_message())
    await message.answer(build_fsm_demo_prompt())


@router.message(StateFilter(FsmDemoStates.waiting_next_message))
async def fsm_demo_next_message(message: Message, state: FSMContext) -> None:
    """Read the temporary FSM value, show it, and clear the state."""
    data = await state.get_data()
    stored_value = str(data.get("demo_value", ""))
    await state.clear()
    await message.answer(build_fsm_demo_result(stored_value))
