#!/bin/bash
set -e

echo "Применение миграций Alembic..."
uv run alembic upgrade head

echo "Загрузка тестовых данных..."
uv run python scripts/add_test_questions.py

echo "Запуск бота..."
exec uv run python -m mentor_bot
