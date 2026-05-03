FROM python:3.11-slim

# ffmpeg  — audio/video processing
# fonts-noto — includes NotoSansHebrew, needed for correct Hebrew rendering in MoviePy/ImageMagick
# fontconfig — rebuilds the font cache so ImageMagick can discover the installed fonts
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        fonts-noto \
        fontconfig \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

# Tell video_service.py where the Hebrew font lives (Debian path after fonts-noto install)
ENV HEBREW_FONT_PATH=/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render injects $PORT at runtime; default to 10000 if not set
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
