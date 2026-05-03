# Ani-Hebrew AI — Project Plan

## Goal
Upload a video or audio file → get a Hebrew-translated SRT subtitle file, with an optional in-browser video player to watch with subtitles.

---

## File Structure

```
my-vibe-project/
├── PLAN.md
├── backend/
│   ├── main.py               # FastAPI app entry point
│   ├── routers/
│   │   └── transcribe.py     # /upload and /status endpoints
│   ├── services/
│   │   ├── ffmpeg_service.py # Audio extraction via FFmpeg
│   │   ├── whisper_service.py# OpenAI Whisper API (task=translate → English)
│   │   └── claude_service.py # Claude 3.5 Sonnet → Hebrew translation
│   ├── utils/
│   │   └── srt_utils.py      # SRT parsing / building helpers
│   ├── temp/                 # Temp files (gitignored)
│   ├── requirements.txt
│   └── .env                  # OPENAI_API_KEY, ANTHROPIC_API_KEY
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── components/
        │   ├── UploadCard.jsx    # Drag-and-drop upload (video/audio)
        │   ├── ProgressStepper.jsx # Extracting → Transcribing → Translating → Done
        │   ├── DownloadCard.jsx  # Download translated SRT
        │   └── VideoPlayer.jsx   # MP4 + SRT player (optional)
        └── api/
            └── client.js         # Axios calls to backend
```

---

## Pipeline

```
[User uploads MP4 / MKV / MP3 / WAV]
        │
        ▼
[1. FFmpeg] — if video: extract audio → temp .mp3
        │
        ▼
[2. OpenAI Whisper API]
   audio file → task='translate' → English text + timestamps (VTT/SRT)
        │
        ▼
[3. Claude 3.5 Sonnet]
   English SRT segments → Hebrew translation (Anime Vibe tone, RTL)
        │
        ▼
[4. SRT Builder]
   Reassemble timestamps + Hebrew lines → .srt file
        │
        ▼
[User downloads Hebrew .srt — optionally watches in player]
```

---

## Progress States (UI)

| Step | Label         | Description                          |
|------|---------------|--------------------------------------|
| 1    | Uploading     | File being sent to backend           |
| 2    | Extracting    | FFmpeg pulling audio from video      |
| 3    | Transcribing  | Whisper converting audio → English   |
| 4    | Translating   | Claude converting English → Hebrew   |
| 5    | Done          | SRT ready to download                |

---

## API Endpoints

| Method | Path              | Description                                      |
|--------|-------------------|--------------------------------------------------|
| POST   | /upload           | Accept file, start pipeline, return job_id       |
| GET    | /status/{job_id}  | Return current step + progress                   |
| GET    | /download/{job_id}| Return translated .srt file                      |

---

## Time Budget (5 hours)

| Task                              | Est.   |
|-----------------------------------|--------|
| Backend boilerplate + FFmpeg      | 45 min |
| Whisper integration               | 30 min |
| Claude translation service        | 30 min |
| FastAPI job tracking + endpoints  | 30 min |
| Frontend scaffold + Tailwind      | 45 min |
| ProgressStepper + UploadCard UI   | 45 min |
| VideoPlayer component             | 30 min |
| End-to-end testing + polish       | 45 min |

---

## Notes
- Whisper `task='translate'` returns English directly — no separate translation step needed for transcription.
- Claude system prompt: "You are a Hebrew subtitle translator with an anime-style voice. Translate naturally, preserve timing, use RTL-friendly punctuation."
- SRT index numbers and timestamps pass through unchanged; only the text lines are sent to Claude.
- FFmpeg must be installed on the host machine (`ffmpeg` on PATH).
- Temp files are cleaned up after download.
