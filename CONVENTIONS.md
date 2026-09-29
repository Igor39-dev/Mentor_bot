# Project Rules

## 1. Project goal

Develop a Telegram bot for testing theoretical Python knowledge.

Main MVP flow:

1. User selects "Проверка знаний".
2. Bot selects a random question from the database.
3. User answers using a voice message.
4. Speech-to-Text converts the voice message to text.
5. LLM analyzes the answer based on the question.
6. Bot returns feedback explaining what is correct, what is missing, and what should be improved.

The MVP should focus on getting this complete flow working.

---

## 2. Technology stack

Use:

- Python 3.12
- uv
- Aiogram 3.x
- SQLAlchemy 2.x with async API only
- asyncpg
- PostgreSQL
- Redis
- Alembic
- LangChain
- OpenRouter
- Speech-to-Text API
- Docker / Docker Compose
- pytest
- Ruff
- Python standard `logging`

Do not use in the MVP:

- Qdrant
- Celery
- web admin panel
- question categories
- Junior/Middle/Senior levels
- reference answers / answer key points
- permanent audio storage
- statistics and user history

The architecture should not prevent adding these features later.

---

## 3. Architecture

Keep the architecture simple and avoid unnecessary abstractions.

Preferred dependency flow:

handlers → services → repositories → database

External AI services are accessed through services:

services → Speech-to-Text  
services → LangChain → OpenRouter

### Handlers

Responsible only for Telegram interaction.

Do not put business logic or database queries directly in handlers.

### Services

Contain application and business logic.

### Repositories

Contain database access logic.

Use asynchronous SQLAlchemy throughout the application.

---

## 4. Questions

MVP uses one common pool of questions without categories or difficulty levels.

Minimal `Question` fields:

- `id`
- `text`
- `created_at`
- `updated_at`
- `is_active`

The bot must be able to select a random active question.

For initial testing, 1–2 questions in the database are sufficient.

Do not implement reference answers yet.

---

## 5. Voice and LLM processing

Processing flow:

Telegram voice  
→ temporary audio file  
→ Speech-to-Text  
→ answer text  
→ LLM  
→ feedback  
→ Telegram

Audio files should not be stored permanently.

STT and LLM implementations must be isolated behind service classes so that providers/models can be replaced later.

The LLM model must be configurable through `.env`, not hardcoded.

The LLM receives at least:

- the original question;
- the user's recognized answer.

---

## 6. FSM and Redis

Use Aiogram FSM with Redis storage.

FSM should keep only temporary state required for the current interaction, such as the current question ID.

Do not use Redis as permanent storage.

---

## 7. Configuration

Use `.env` for secrets and environment-specific settings.

Provide `.env.example`.

At minimum:

```text
BOT_TOKEN=
DATABASE_URL=
REDIS_URL=
OPENROUTER_API_KEY=
OPENROUTER_MODEL=
```
Never commit real secrets to the repository!


## 8. Database and migrations

PostgreSQL is the main database.

Use:

SQLAlchemy 2.x async API
asyncpg
Alembic

All database operations in the application must be asynchronous.

## 9. Logging and external API errors

Use Python's standard logging.

Do not use print() for application diagnostics.

Handle errors from:

Telegram API
PostgreSQL
Redis
Speech-to-Text API
OpenRouter / LLM

External API calls must have timeouts.

Use retries only for appropriate temporary errors such as network failures, 429, or selected 5xx responses.

Never log API keys, tokens, or other secrets.

## 10. Docker

Docker Compose should provide the development infrastructure:

PostgreSQL
Redis

The bot should also have a Dockerfile for containerized execution.

During development, the bot may be launched directly with uv.

## 11. Testing

Testing is not a priority during the initial implementation.

First make the complete MVP flow work.

Tests with pytest can be added after the main functionality is working.

Do not create a large testing infrastructure prematurely.

## 12. Code style

Use Ruff for linting and formatting.

Configuration:

Python target: py312
line length: 120
rules: E, F, I, UP, B, C4, SIM
ignore B008
double quotes
spaces for indentation

Use absolute imports.

Use meaningful docstrings for public and non-obvious functions/classes.

Do not write redundant docstrings that simply repeat the function name.

Use inline comments only for non-obvious logic.

## 13. Development approach

Implement the project incrementally.

Do not generate the entire project at once.

For each development stage:

1. Implement only the functionality required for the current stage.
2. Run the relevant checks.
3. Verify that the application still works.
4. Report what was implemented and any issues found.
5. Stop and wait for confirmation before starting the next stage.

Prioritize a simple working MVP over premature abstraction or additional functionality.
Ask question if needed.
