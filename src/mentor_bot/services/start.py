"""Welcome and FSM demo message helpers."""

from typing import Final

FSM_DEMO_VALUE: Final[str] = "fsm-demo-ok"


def build_welcome_message() -> str:
    """Return the greeting text sent on /start."""
    return (
        "Привет! Я Mentor Bot — бот для проверки теоретических знаний по Python.\n\n"
        "Скоро здесь появится режим «Проверка знаний».\n"
        "Сейчас доступен тестовый сценарий FSM: отправь любое следующее сообщение."
    )


def build_fsm_demo_prompt() -> str:
    """Ask the user to send the next message for the FSM demo."""
    return "Напиши любое сообщение — я верну значение, сохранённое во временном FSM-состоянии."


def build_fsm_demo_result(stored_value: str) -> str:
    """Format the value read back from FSM data."""
    return f"FSM работает. Значение из временного состояния: {stored_value}\nСостояние очищено."
