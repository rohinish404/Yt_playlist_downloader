# Stage 1: Install FFMPEG
FROM jrottenberg/ffmpeg:4.3-alpine AS ffmpeg

# Stage 2: Install application dependencies
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy FFMPEG binaries from the first stage
COPY --from=ffmpeg /usr/local /usr/local

CMD ["python", "app.py"]
