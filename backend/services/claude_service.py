"""Hebrew translation of SRT blocks via Claude Sonnet."""
import os
import json
import anthropic
from backend.utils.srt_utils import SRTBlock

_client: anthropic.AsyncAnthropic | None = None

SYSTEM_PROMPT = """\
You are a professional Hebrew subtitle translator for anime and animated series.

Translate each subtitle into natural, fluent Hebrew. Follow these rules exactly:
1. Produce idiomatic Hebrew a native speaker would naturally say — avoid word-for-word calques.
2. Match the character's register: dramatic lines stay dramatic, humor stays funny, shouts feel urgent.
3. Keep every subtitle short enough to read comfortably within its time slot.
4. Accept source text in any language (Japanese, English, etc.) and output Hebrew only.
5. Preserve every "index" value exactly as received — do not reorder or renumber.
6. Return ONLY a raw JSON array. No markdown fences, no explanation, no extra keys.

Input:  [{"index": 1, "text": "source text"}, ...]
Output: [{"index": 1, "text": "תרגום עברי"}, ...]
"""


def _get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        _client = anthropic.AsyncAnthropic(api_key=api_key)
    return _client


async def translate_blocks_to_hebrew(blocks: list[SRTBlock]) -> list[SRTBlock]:
    """Translate SRT blocks to Hebrew via Claude. Timestamps and indices are preserved."""
    client = _get_client()

    # Build compact payload — only send what Claude needs to translate
    payload = [{"index": b.index, "text": b.text} for b in blocks]
    user_message = json.dumps(payload, ensure_ascii=False)

    message = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = message.content[0].text.strip()
    translated = json.loads(raw)

    # Map index → translated text for O(1) lookup
    translation_map: dict[int, str] = {item["index"]: item["text"] for item in translated}

    return [
        SRTBlock(
            index=b.index,
            start=b.start,
            end=b.end,
            text=translation_map.get(b.index, b.text),  # fallback to English on miss
        )
        for b in blocks
    ]
