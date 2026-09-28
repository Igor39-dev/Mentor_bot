"""Temporary FSM states for Redis storage smoke test."""

from aiogram.fsm.state import State, StatesGroup


class FsmDemoStates(StatesGroup):
    """Demo flow: wait for the next user message after /start."""

    waiting_next_message = State()
