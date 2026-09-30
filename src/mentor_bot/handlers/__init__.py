"""Telegram handlers (interaction layer)."""

from aiogram import Router

from mentor_bot.handlers.knowledge_check import router as knowledge_check_router
from mentor_bot.handlers.start import router as start_router


def get_root_router() -> Router:
    """Build and return the root router with all handlers attached."""
    root_router = Router(name="root")
    root_router.include_router(start_router)
    root_router.include_router(knowledge_check_router)
    return root_router
