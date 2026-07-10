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

    video_id = extract_youtube_id(url)

    DATA_DIR.mkdir(exist_ok=True)

    output_template = str(
        DATA_DIR / f"{video_id}.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    audio_path = DATA_DIR / f"{video_id}.mp3"

    return video_id, str(audio_path)