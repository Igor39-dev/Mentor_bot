"""FSM states for knowledge check flow."""

from aiogram.fsm.state import State, StatesGroup


class KnowledgeCheckStates(StatesGroup):
    """Knowledge check flow: question → voice answer → feedback."""

    waiting_voice_answer = State()
