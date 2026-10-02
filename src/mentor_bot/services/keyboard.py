"""Keyboard builders for bot UI."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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
    builder = ReplyKeyboardBuilder()
    for category in CATEGORIES:
        builder.add(KeyboardButton(text=category))
    
    builder.adjust(2) 
    return builder.as_markup(resize_keyboard=True)
