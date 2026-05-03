"""Transcription via OpenAI Whisper API with task='translate' (audio → English)."""
import os
from openai import AsyncOpenAI
from utils.srt_utils import SRTBlock, whisper_vtt_to_srt_blocks

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        _client = AsyncOpenAI(api_key=api_key)
    return _client


async def transcribe_to_english(audio_path: str) -> list[SRTBlock]:
    """
    Send audio to Whisper translations endpoint.
    Returns a list of SRTBlock with English text and timestamps.
    The translations endpoint detects any language and always outputs English.
    """
    client = _get_client()
    with open(audio_path, "rb") as f:
        response = await client.audio.translations.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
        )
    segments = response.segments or []
    return whisper_vtt_to_srt_blocks(segments)
