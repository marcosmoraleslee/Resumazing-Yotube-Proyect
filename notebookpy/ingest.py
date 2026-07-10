import os
import urllib.parse as urlparse
from pathlib import Path

import yt_dlp


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def extract_youtube_id(url: str) -> str:
    """
    Extract YouTube video ID.
    """

    parsed_url = urlparse.urlparse(url)
    query_params = urlparse.parse_qs(parsed_url.query)

    if "v" in query_params:
        return query_params["v"][0]

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    raise ValueError("Invalid YouTube URL provided.")


def download_youtube_audio(url: str) -> tuple[str, str]:
    """
    Download YouTube audio as mp3.

    Returns:
        video_id
        audio_path
    """

    # Extract ID
    video_id = extract_youtube_id(url)

    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)

    # Output template
    output_template = str(DATA_DIR / f"{video_id}.%(ext)s")

    # yt-dlp configuration (🔥 FIX 403 INCLUDED)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,

        # 🔥 FIX 403 Forbidden
        "cookiesfrombrowser": "chrome",   # o "edge"
        "extractor_args": {"youtube": {"player_client": ["android"]}},

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    audio_path = str(DATA_DIR / f"{video_id}.mp3")

    return video_id, audio_path
