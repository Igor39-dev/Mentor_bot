"""Application entry point."""

import logging
from typing import Final

from mentor_bot.config import get_settings

logger = logging.getLogger(__name__)

LOG_FORMAT: Final[str] = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def main() -> None:
    """Configure logging, load settings, and start the application shell."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    settings = get_settings()
    model = settings.openrouter_model or "not configured"
    logger.info("Mentor bot entry point ready (openrouter_model=%s)", model)


if __name__ == "__main__":
    main()
