import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


load_dotenv(BASE_DIR / ".env")


api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables."
    )


client = OpenAI(api_key=api_key)


def to_timestamp(seconds: float) -> str:
    """
    Convert seconds to MM:SS timestamp.
    """

    minutes = int(seconds // 60)
    secs = int(seconds % 60)

    return f"[{minutes:02d}:{secs:02d}]"


def transcribe_audio(audio_path: str, video_id: str) -> str:
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path:
            Path to mp3 audio.

        video_id:
            YouTube video identifier.

    Returns:
        Transcript text.
    """

    print("🎙️ Starting transcription...")

    with open(audio_path, "rb") as audio_file:

        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,        
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )


    if response.segments is None:
        raise ValueError(
            "Whisper returned no segments."
        )


    transcription_lines = []


    for segment in response.segments:

        timestamp = to_timestamp(segment.start)

        transcription_lines.append(
            f"{timestamp} {segment.text.strip()}"
        )


    transcription_text = "\n".join(
        transcription_lines
    )


    output_path = DATA_DIR / f"{video_id}.txt"


    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(transcription_text)


    print("✅ Transcription completed.")

    return transcription_text