"""Hebrew translation of SRT blocks via Claude 3.5 Sonnet."""
import os
import json
import anthropic
from utils.srt_utils import SRTBlock

_client: anthropic.AsyncAnthropic | None = None

SYSTEM_PROMPT = """\
You are an expert Hebrew subtitle translator specializing in anime and animated content.
Your job is to translate English subtitle text into natural, expressive Hebrew while:
- Preserving the anime/animated vibe, energy, and character voice
- Writing right-to-left Hebrew that displays correctly in SRT players
- Keeping translations concise enough to read on screen in the allotted time
- Never altering subtitle index numbers or timestamps — you only touch the text

You will receive a JSON array of subtitle segments with this shape:
[{"index": 1, "text": "Hello, world!"}, ...]

Respond with ONLY a JSON array in the same shape with translated text:
[{"index": 1, "text": "!שלום, עולם"}, ...]
No markdown, no explanation, no extra keys.
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
    """
    Send English SRT blocks to Claude 3.5 Sonnet and return Hebrew-translated blocks.
    Timestamps and indices are preserved; only .text is replaced.
    """
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
