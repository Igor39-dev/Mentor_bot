FROM python:3.12-slim

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

# Установка зависимостей
RUN uv sync --frozen --no-dev

# Создание директории для временных аудио файлов
RUN mkdir -p temp_audio

# Запуск приложения
CMD ["uv", "run", "python", "-m", "mentor_bot"]
