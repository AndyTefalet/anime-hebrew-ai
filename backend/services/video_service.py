"""Burn Hebrew subtitles into a video using MoviePy."""
import os

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from backend.utils.srt_utils import parse_srt
from backend.utils.hebrew_utils import fix_hebrew_text

# Override by setting HEBREW_FONT_PATH in the environment (e.g. in render.yaml or Dockerfile ENV).
HEBREW_FONT = os.environ.get(
    "HEBREW_FONT_PATH",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf",
)


def _srt_time_to_seconds(timestamp: str) -> float:
    """Convert an SRT timestamp (HH:MM:SS,mmm) to a float number of seconds."""
    h, m, s = timestamp.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def hardcode_subtitles(video_path: str, srt_path: str, output_path: str) -> None:
    """Composite Hebrew subtitle text clips onto *video_path* and write to *output_path*."""
    with open(srt_path, encoding="utf-8") as f:
        blocks = parse_srt(f.read())

    video = VideoFileClip(video_path)
    subtitle_clips = []

    for block in blocks:
        text = fix_hebrew_text(block.text)
        start = _srt_time_to_seconds(block.start)
        end = _srt_time_to_seconds(block.end)

        txt_clip = (
            TextClip(
                text,
                font=HEBREW_FONT,
                fontsize=36,
                color="white",
                stroke_color="black",
                stroke_width=1,
            )
            .set_position(("center", "bottom"))
            .set_start(start)
            .set_end(end)
        )
        subtitle_clips.append(txt_clip)

    final = CompositeVideoClip([video, *subtitle_clips])
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video.close()
    final.close()
