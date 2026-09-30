"""Speech-to-Text service using OpenRouter."""

import logging
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)


class STTService:
    """Service for converting speech to text using OpenRouter Whisper API."""

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/audio/transcriptions"
        self.timeout = 30.0

    async def transcribe_audio(self, audio_path: Path) -> str:
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to audio file

        Returns:
            Transcribed text

        Raises:
            httpx.HTTPError: If API request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            with audio_path.open("rb") as audio_file:
                files = {"file": (audio_path.name, audio_file, "audio/ogg")}
                data = {"model": self.model}
                headers = {"Authorization": f"Bearer {self.api_key}"}

                try:
                    response = await client.post(self.api_url, headers=headers, files=files, data=data)
                    response.raise_for_status()
                    result = response.json()
                    return result.get("text", "")
                except httpx.HTTPError as e:
                    logger.error("STT API error: %s", e)
                    raise
