FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Установка переменной окружения для SSL
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

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

# Копирование скриптов
COPY scripts ./scripts
COPY entrypoint.sh ./

# Установка прав на выполнение для entrypoint
RUN chmod +x entrypoint.sh

# Запуск через entrypoint
ENTRYPOINT ["./entrypoint.sh"]
