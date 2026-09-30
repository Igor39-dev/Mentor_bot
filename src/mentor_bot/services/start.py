"""Welcome message helper."""


def build_welcome_message() -> str:
    """Return the greeting text sent on /start."""
    return (
        "Привет! Я Mentor Bot — бот для проверки теоретических знаний по Python.\n\n"
        "Нажмите кнопку «Проверка знаний», чтобы получить случайный вопрос и ответить голосовым сообщением."
    )
