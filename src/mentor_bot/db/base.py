"""SQLAlchemy declarative base for ORM models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""


# Import all models here to ensure they are registered with Base metadata
from mentor_bot.db.models import Question  # noqa: E402, F401
