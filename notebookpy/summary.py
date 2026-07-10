import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



def generate_video_summary(video_id: str) -> str:
    """
    Generate a short summary from the video transcript.
    """


    transcript_path = f"data/{video_id}.txt"


    if not os.path.exists(transcript_path):

        raise FileNotFoundError(
            f"Transcript not found: {transcript_path}"
        )


    with open(
        transcript_path,
        "r",
        encoding="utf-8"
    ) as file:

        transcript = file.read()



    prompt = f"""
You are ResuMazing, an AI assistant specialized in CV,
resume optimization and ATS systems.

Summarize the following YouTube transcript.

Requirements:

- Explain the main topic of the video.
- Extract the most important CV/ATS recommendations.
- Use bullet points.
- Keep the summary clear and practical.
- Do not invent information.

Transcript:

{transcript}
"""


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content