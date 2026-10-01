"""FSM states for knowledge check flow."""

from aiogram.fsm.state import State, StatesGroup


class KnowledgeCheckStates(StatesGroup):
    """Knowledge check flow: category selection → question → voice answer → feedback."""

    waiting_category_selection = State()
    waiting_voice_answer = State()
