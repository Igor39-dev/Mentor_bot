"""Keyboard builders for bot UI."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

CATEGORIES = [
    "Основы Python",
    "БД",
    "Django",
    "Asyncio",
    "FastAPI",
    "Pytest",
]


def build_main_keyboard() -> ReplyKeyboardMarkup:
    """Build main menu keyboard with knowledge check button."""
    keyboard = [[KeyboardButton(text="Проверка знаний")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def build_category_keyboard() -> ReplyKeyboardMarkup:
    """Build keyboard with question categories."""
    keyboard = [[KeyboardButton(text=category)] for category in CATEGORIES]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
