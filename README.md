# Mentor Bot

Telegram-бот для проверки теоретических знаний Python-разработчиков через голосовые ответы с анализом через LLM.

## Описание

Бот позволяет пользователям проверять свои знания по различным темам Python-разработки:
 - Основы Python
 - Базы данных (БД)
 - Django
 - Asyncio
 - FastAPI
 - Pytest


### Прицип работы бота

1. Пользователь выбирает "Проверка знаний"
2. Выбирает категорию вопроса
3. Получает случайный вопрос из выбранной категории
4. Отправляет голосовой ответ
5. Бот распознает речь (Speech-to-Text)
6. LLM анализирует ответ и дает обратную связь


## Технологический стек

- **Python 3.12**
- **uv** — управление зависимостями
- **Aiogram 3.x** — фреймворк для Telegram-ботов
- **SQLAlchemy 2.x** (async) — ORM для работы с БД
- **asyncpg** — асинхронный драйвер PostgreSQL
- **PostgreSQL** — основная база данных
- **Redis** — хранилище FSM-состояний
- **Alembic** — миграции БД
- **LangChain** — работа с LLM
- **OpenRouter** — доступ к LLM и Speech-to-Text API
- **Docker / Docker Compose** — контейнеризация
- **pytest** — тестирование
- **Ruff** — линтер и форматтер


## Установка и запуск
                  
### Требования
                  
- Python 3.12+
- uv
- Docker и Docker Compose


### Настройка окружения

Клонируйте репозиторий:

```bash
git clone <repository-url>
cd mentor_bot
```

Создайте `.env` файл на основе `.env.example`:

Заполните переменные окружения в `.env`:

```env
BOT_TOKEN=<ваш_токен_telegram_бота>                  
DATABASE_URL=postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/python_theory_bot
REDIS_URL=redis://127.0.0.1:6380/0
                  
OPENROUTER_API_KEY=<ваш_ключ_openrouter>                  
OPENROUTER_MODEL=<модель_llm>
OPENROUTER_STT_MODEL=openai/whisper-large-v3-turbo

POSTGRES_DB=python_theory_bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
| `BOT_TOKEN` | Токен Telegram-бота | `1234567890:ABCdef...` |
| `DATABASE_URL` | URL подключения к PostgreSQL | `postgresql+asyncpg://user:pass@host:port/db` |
| `REDIS_URL` | URL подключения к Redis | `redis://localhost:6379/0` |
| `OPENROUTER_API_KEY` | API ключ OpenRouter | `sk-or-v1-...` |
| `OPENROUTER_MODEL` | Модель LLM для анализа ответов | `anthropic/claude-3.5-sonnet` |
| `OPENROUTER_STT_MODEL` | Модель Speech-to-Text | `openai/whisper-large-v3-turbo` |
| `POSTGRES_DB` | Имя базы данных PostgreSQL | `python_theory_bot` |
| `POSTGRES_USER` | Пользователь PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | `postgres` |


### Запуск через Docker Compose

Запустите инфраструктуру (PostgreSQL + Redis):
```bash
docker-compose up -d
```

Установите зависимости:

```bash
uv sync
```                  

Примените миграции:
```bash
uv run alembic upgrade head
```

Добавьте тестовые вопросы:
```bash                  
uv run python scripts/add_test_questions.py
```

Запустите бота:
```bash
uv run python -m mentor_bot
```

## Структура проекта

```
mentor_bot/
├── alembic/                     # Миграции базы данных
│   ├── versions/                # Версии миграций
│   ├── env.py                   # Конфигурация Alembic
│   └── script.py.mako           # Шаблон миграции
├── scripts/                     # Утилитарные скрипты
│   └── add_test_questions.py    # Скрипт добавления вопросов
├── src/
│   └── mentor_bot/
│       ├── db/                  # Модели и работа с БД
│       │   ├── base.py          # Базовая модель
│       │   ├── models.py        # SQLAlchemy модели
│       │   └── session.py       # Управление сессиями
│       ├── handlers/            # Обработчики Telegram
│       │   ├── start.py         # Команда /start
│       │   └── knowledge_check.py # Основной флоу проверки знаний
│       ├── repositories/        # Слой доступа к данным
│       │   └── question.py      # Репозиторий вопросов
│       ├── services/            # Бизнес-логика и внешние API
│       │   ├── keyboard.py      # Клавиатуры бота
│       │   ├── llm.py           # Интеграция с LLM
│       │   ├── question.py      # Сервис вопросов
│       │   ├── start.py         # Сервис приветствия
│       │   ├── stt.py           # Speech-to-Text сервис
│       │   └── telegram.py      # Утилиты Telegram
│       ├── states/              # FSM состояния
│       │   └── knowledge_check.py # Состояния проверки знаний
│       ├── config.py            # Конфигурация из .env
│       ├── main.py              # Точка входа
│       └── __main__.py          # Запуск как модуль
├── .env.example                 # Шаблон переменных окружения
├── .gitignore                   # Git игнорирование
├── ARCHITECTURE.md              # Описание архитектуры
├── CONVENTIONS.md               # Правила разработки
├── alembic.ini                  # Конфигурация Alembic
├── docker-compose.yml           # Инфраструктура
├── pyproject.toml               # Зависимости и настройки
└── README.md                    # Этот файл
```                  

## Архитектура

Проект следует принципам чистой архитектуры с разделением на слои:

**handlers → services → repositories → database**

- **Handlers** — обработка Telegram-событий, взаимодействие с пользователем
- **Services** — бизнес-логика и интеграции с внешними API (STT, LLM)
- **Repositories** — изолированная работа с базой данных
- **Models** — SQLAlchemy модели данных

Внешние сервисы (Speech-to-Text, LLM) изолированы в сервисном слое для легкой замены провайдеров.

## База данных

### Модель Question

- `id` — первичный ключ
- `text` — текст вопроса
- `category` — категория вопроса (Основы Python, БД, Django, Asyncio, FastAPI, Pytest)
- `is_active` — флаг активности
- `created_at` — дата создания
- `updated_at` — дата обновления


## Линтинг и форматирование
Проект использует **Ruff** для линтинга и форматирования.
        
## Docker

### Порты

В `docker-compose.yml` настроены следующие порты:
- PostgreSQL: `5433:5432` (чтобы не конфликтовать с локальным PostgreSQL)
- Redis: `6380:6379` (чтобы не конфликтовать с локальным Redis)

### Volumes

- `postgres_data` — данные PostgreSQL
- `redis_data` — данные Redis
- `./temp_audio` — временные аудио файлы (маппинг с хоста)

### Полезные команды

Пересборка образа бота после изменений в коде:
```bash
docker-compose build bot
```

Перезапуск только бота:
```bash
docker-compose restart bot
```

Остановка всех сервисов:
```bash
docker-compose down
```

Остановка с удалением volumes (очистка всех данных):
```bash
docker-compose down -v
```

Просмотр логов всех сервисов:
```bash
docker-compose logs -f
```

Выполнение команды внутри контейнера бота:
```bash
docker-compose exec bot <команда>
```

### Переменные окружения для Docker

При запуске через Docker Compose переменные `DATABASE_URL` и `REDIS_URL` автоматически переопределяются для использования внутренних Docker-сервисов (`postgres:5432` и `redis:6379`).

Убедитесь, что в `.env` указаны остальные переменные:
- `BOT_TOKEN`
- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`
- `OPENROUTER_STT_MODEL`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
