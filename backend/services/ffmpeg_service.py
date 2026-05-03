"""Audio extraction from video files using FFmpeg."""
import asyncio
import os
from pathlib import Path

# Accepted MIME / extension sets
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"}


def is_video(filename: str) -> bool:
    return Path(filename).suffix.lower() in VIDEO_EXTENSIONS


def is_audio(filename: str) -> bool:
    return Path(filename).suffix.lower() in AUDIO_EXTENSIONS


async def extract_audio(input_path: str, output_path: str) -> None:
    """
    Run FFmpeg to strip audio from a video file and write a mono 16 kHz MP3.
    Raises RuntimeError if FFmpeg exits non-zero.
    """
    cmd = [
        "ffmpeg",
        "-y",              # overwrite output
        "-i", input_path,
        "-vn",             # no video
        "-ar", "16000",    # 16 kHz — optimal for Whisper
        "-ac", "1",        # mono
        "-q:a", "0",       # highest quality VBR
        output_path,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"FFmpeg failed (exit {proc.returncode}):\n{stderr.decode(errors='replace')}"
        )


async def prepare_audio(input_path: str, temp_dir: str, job_id: str) -> str:
    """
    Return a path to an audio file ready for Whisper.
    If input is already audio, returns input_path unchanged.
    If input is video, extracts audio and returns the new path.
    """
    suffix = Path(input_path).suffix.lower()
    if suffix in AUDIO_EXTENSIONS:
        return input_path

    audio_out = os.path.join(temp_dir, f"{job_id}_audio.mp3")
    await extract_audio(input_path, audio_out)
    return audio_out
