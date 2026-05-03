"""Upload, status, and download endpoints."""
import asyncio
import os
import uuid
from pathlib import Path
from typing import Dict

import aiofiles
from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.ffmpeg_service import is_video, is_audio, prepare_audio
from services.whisper_service import transcribe_to_english
from services.claude_service import translate_blocks_to_hebrew
from utils.srt_utils import build_srt

router = APIRouter()

TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# In-memory job store (replace with Redis/DB for production)
jobs: Dict[str, dict] = {}


class JobStatus(BaseModel):
    job_id: str
    step: str          # uploading | extracting | transcribing | translating | done | error
    message: str = ""


def _set(job_id: str, step: str, message: str = "") -> None:
    jobs[job_id] = {"step": step, "message": message}


async def _run_pipeline(job_id: str, input_path: str, original_filename: str) -> None:
    try:
        # Step 1 — extract audio if needed
        if is_video(original_filename):
            _set(job_id, "extracting", "Extracting audio with FFmpeg…")
            audio_path = await prepare_audio(input_path, TEMP_DIR, job_id)
        else:
            audio_path = input_path

        # Step 2 — transcribe + translate to English via Whisper
        _set(job_id, "transcribing", "Transcribing audio with Whisper…")
        english_blocks = await transcribe_to_english(audio_path)

        # Step 3 — translate English → Hebrew via Claude
        _set(job_id, "translating", "Translating to Hebrew with Claude…")
        hebrew_blocks = await translate_blocks_to_hebrew(english_blocks)

        # Step 4 — write SRT output
        srt_content = build_srt(hebrew_blocks)
        output_path = os.path.join(TEMP_DIR, f"{job_id}_hebrew.srt")
        async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
            await f.write(srt_content)

        _set(job_id, "done", output_path)

    except Exception as exc:
        _set(job_id, "error", str(exc))
    finally:
        # Clean up uploaded + extracted audio (keep output SRT until download)
        for path in [input_path]:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError:
                pass
        extracted = os.path.join(TEMP_DIR, f"{job_id}_audio.mp3")
        if os.path.exists(extracted) and extracted != input_path:
            try:
                os.remove(extracted)
            except OSError:
                pass


@router.post("/upload", response_model=JobStatus)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    filename = file.filename or "upload"
    suffix = Path(filename).suffix.lower()

    if not (is_video(filename) or is_audio(filename)):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Upload an MP4, MKV, MOV, MP3, WAV, etc.",
        )

    job_id = str(uuid.uuid4())
    input_path = os.path.join(TEMP_DIR, f"{job_id}_input{suffix}")

    # Save upload to disk
    async with aiofiles.open(input_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):  # 1 MB chunks
            await f.write(chunk)

    _set(job_id, "uploading", "File received, starting pipeline…")
    background_tasks.add_task(_run_pipeline, job_id, input_path, filename)

    return JobStatus(job_id=job_id, step="uploading", message="File received, starting pipeline…")


@router.get("/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatus(job_id=job_id, **job)


@router.get("/download/{job_id}")
async def download_srt(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["step"] != "done":
        raise HTTPException(status_code=400, detail=f"Job not complete (step: {job['step']})")

    output_path = job["message"]  # stored as the file path on "done"
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Output file missing")

    return FileResponse(
        path=output_path,
        media_type="text/plain; charset=utf-8",
        filename="hebrew_subtitles.srt",
    )
