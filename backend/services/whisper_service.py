"""Transcription via OpenAI Whisper API with segment and word-level timestamps."""
import os
from openai import AsyncOpenAI
from backend.utils.srt_utils import SRTBlock, whisper_vtt_to_srt_blocks

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        _client = AsyncOpenAI(api_key=api_key)
    return _client


async def transcribe_audio(audio_path: str) -> list[SRTBlock]:
    """
    Transcribe audio with Whisper using segment and word-level timestamps.
    Returns SRTBlocks grouped by segment; word timestamps give accurate boundaries.
    """
    client = _get_client()
    with open(audio_path, "rb") as f:
        response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment", "word"],
        )
    segments = response.segments or []
    return whisper_vtt_to_srt_blocks(segments)
