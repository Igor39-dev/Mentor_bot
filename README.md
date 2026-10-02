# Mentor Bot

Telegram-бот для проверки теоретических знаний по Python через голосовые ответы с анализом через **LLM**.

Бот позволяет пользователям проверять свои знания по различным темам Python-разработки: Основы Python, Базы данных (БД), Django, Asyncio, FastAPI, Pytest

ТГ-бот: [@PythonMentor_for_me_bot](https://t.me/PythonMentor_for_me_bot)

<img src="image.png" alt="alt text" width="150">

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
├── alembic.ini                  # Конфигурация Alembic
├── docker-compose.yml           # Инфраструктура
├── pyproject.toml               # Зависимости и настройки
└── README.md                    # Этот файл
```                  


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
- **Aiogram 3.31** — фреймворк для Telegram-ботов
- **SQLAlchemy 2.1** (async) — ORM для работы с БД
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
- [`uv`](https://docs.astral.sh/uv/)
- Docker и Docker Compose
- [openrouter.ai](https://openrouter.ai/models) (API)

### Важно!

При использовании голосовых сообщений бот отправляет аудио в OpenRouter для распознавания речи (STT).

Некоторые антивирусы, могут выполнять проверку HTTPS-соединений и подменять сертификат сервера собственным. Docker-контейнер не доверяет этому сертификату, поэтому запрос к OpenRouter может завершиться ошибкой: Если возникает `httpx.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed`, добавьте домен `openrouter.ai` в список доверенных адресов

### Настройка окружения

Клонируйте репозиторий:

```bash
git clone https://github.com/Igor39-dev/Mentor_bot
```
```bash
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

| Переменная             | Описание                       | Пример                                        |
| ---------------------- | ------------------------------ | --------------------------------------------- |
| `BOT_TOKEN`            | Токен Telegram-бота            | `1234567890:ABCdef...`                        |
| `DATABASE_URL`         | URL подключения к PostgreSQL   | `postgresql+asyncpg://user:pass@host:port/db` |
| `REDIS_URL`            | URL подключения к Redis        | `redis://localhost:6379/0`                    |
| `OPENROUTER_API_KEY`   | API ключ OpenRouter            | `sk-or-v1-...`                                |
| `OPENROUTER_MODEL`     | Модель LLM для анализа ответов | `deepseek/deepseek-v4.1-flash`                 |
| `OPENROUTER_STT_MODEL` | Модель Speech-to-Text          | `openai/whisper-large-v3-turbo`               |
| `POSTGRES_DB`          | Имя базы данных PostgreSQL     | `python_theory_bot`                           |
| `POSTGRES_USER`        | Пользователь PostgreSQL        | `postgres`                                    |
| `POSTGRES_PASSWORD`    | Пароль PostgreSQL              | `postgres`                                    |


### Запуск через Docker Compose

Запустите инфраструктуру (PostgreSQL + Redis + Bot):
```bash
docker-compose up -d
```
(Применение миграции, добавление тестового набора вопросов и запуск бота автоматически)

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


### Volumes

- `postgres_data` — данные PostgreSQL
- `redis_data` — данные Redis
- `./temp_audio` — временные аудио файлы (маппинг с хоста)
