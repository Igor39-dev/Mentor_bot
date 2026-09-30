"""Keyboard builders for bot UI."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def build_main_keyboard() -> ReplyKeyboardMarkup:
    """Build main menu keyboard with knowledge check button."""
    keyboard = [[KeyboardButton(text="Проверка знаний")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
