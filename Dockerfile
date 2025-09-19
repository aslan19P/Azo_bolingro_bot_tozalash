# Minimal image for running the Telethon userbot cleaner
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (if Telethon needs libffi? not necessary) but telethon uses pure python; maybe need? We'll leave minimal.
# Copy requirement files first to leverage docker layering
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY userbot ./userbot

# Default command runs the cleaner. Environment variables should be provided at runtime.
CMD ["python", "-m", "userbot.cleaner"]
