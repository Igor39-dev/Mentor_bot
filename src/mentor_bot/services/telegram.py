"""Telegram Bot API helpers."""

import logging
from pathlib import Path

from aiogram import Bot
from aiogram.types import Voice

logger = logging.getLogger(__name__)


async def download_voice_file(bot: Bot, voice: Voice, temp_dir: Path) -> Path:
    """
    Download voice message from Telegram.

    Args:
        bot: Bot instance
        voice: Voice message object
        temp_dir: Directory for temporary files

    Returns:
        Path to downloaded file
    """
    temp_dir.mkdir(parents=True, exist_ok=True)
    file = await bot.get_file(voice.file_id)
    file_path = temp_dir / f"{voice.file_id}.ogg"
    await bot.download_file(file.file_path, file_path)
    logger.info("Downloaded voice file: %s", file_path)
    return file_path
