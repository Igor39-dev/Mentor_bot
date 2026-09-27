"""Application settings loaded from environment variables."""

from functools import lru_cache
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE: Final[str] = ".env"


class Settings(BaseSettings):
    """Runtime configuration from `.env` and process environment."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    BOT_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
