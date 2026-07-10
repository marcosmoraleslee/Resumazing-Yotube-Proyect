import os

from dotenv import load_dotenv
from openai import OpenAI



def transcribe_user_audio(audio_file):
    """
    Convert microphone audio into text using Whisper.
    """

    load_dotenv()


    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )


    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )


    return transcript.text