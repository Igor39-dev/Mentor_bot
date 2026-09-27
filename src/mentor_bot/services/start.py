"""Welcome message helpers for the start flow."""


def build_welcome_message() -> str:
    """Return the greeting text sent on /start."""
    return (
        "Привет! Я Mentor Bot — бот для проверки теоретических знаний по Python.\n\n"
        "Скоро здесь появится режим «Проверка знаний». Пока доступна только команда /start."
    )
