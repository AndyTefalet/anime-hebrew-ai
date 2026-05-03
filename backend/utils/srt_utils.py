"""SRT parsing and building utilities."""
from dataclasses import dataclass
from typing import List
import re


@dataclass
class SRTBlock:
    index: int
    start: str
    end: str
    text: str  # may be multi-line


def parse_srt(content: str) -> List[SRTBlock]:
    blocks = []
    raw_blocks = re.split(r"\n\s*\n", content.strip())
    for raw in raw_blocks:
        lines = raw.strip().splitlines()
        if len(lines) < 3:
            continue
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue
        timing_match = re.match(
            r"(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})",
            lines[1].strip(),
        )
        if not timing_match:
            continue
        start, end = timing_match.group(1), timing_match.group(2)
        text = "\n".join(lines[2:])
        blocks.append(SRTBlock(index=index, start=start, end=end, text=text))
    return blocks


def build_srt(blocks: List[SRTBlock]) -> str:
    parts = []
    for b in blocks:
        parts.append(f"{b.index}\n{b.start} --> {b.end}\n{b.text}\n")
    return "\n".join(parts)


def whisper_vtt_to_srt_blocks(segments: list) -> List[SRTBlock]:
    """Convert OpenAI Whisper verbose_json segments to SRTBlock list."""
    blocks = []
    for i, seg in enumerate(segments, start=1):
        start = _seconds_to_srt_time(seg.start)
        end = _seconds_to_srt_time(seg.end)
        blocks.append(SRTBlock(index=i, start=start, end=end, text=seg.text.strip()))
    return blocks


def text_to_srt_blocks(text: str, seconds_per_block: float = 3.0) -> List[SRTBlock]:
    """Split plain text into SRTBlocks with auto-generated timestamps."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        lines = [text.strip()] if text.strip() else []
    blocks = []
    for i, line in enumerate(lines, start=1):
        start_s = (i - 1) * seconds_per_block
        end_s = i * seconds_per_block
        blocks.append(SRTBlock(
            index=i,
            start=_seconds_to_srt_time(start_s),
            end=_seconds_to_srt_time(end_s),
            text=line,
        ))
    return blocks


def _seconds_to_srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1_000
    ms %= 1_000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
