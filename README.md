## ResuMazing — YouTube RAG Pipeline
A complete end‑to‑end workflow that transforms any YouTube video into searchable, timestamp‑aware knowledge using audio ingestion → transcription → chunking → embeddings → Pinecone.

📌 Overview
ResuMazing is a modular pipeline designed to convert YouTube content into structured data suitable for semantic search and Retrieval‑Augmented Generation (RAG).
The project downloads audio, transcribes it with Whisper, chunks the transcript, generates embeddings with OpenAI, and stores them in Pinecone for fast vector search.

The repository is organized into three notebooks, each representing a core stage of the pipeline.

🧩 Pipeline Architecture
Notebook 1 — Ingestion
Handles URL parsing and audio extraction.

Key features:

Extracts YouTube video IDs from both standard and shortened URLs.

Validates the URL before processing.

Downloads the audio using yt-dlp and saves it as VIDEO_ID.mp3 in data/.

Creates session_state.json to store the active video ID for downstream notebooks.

Output:  
A clean MP3 file and a persistent session state.

Notebook 2 — Transcription
Generates a timestamped transcript using Whisper.

Key features:

Loads environment variables and checks for a valid OpenAI API key.

Reads session_state.json to recover the active video ID.

Sends the MP3 file to the whisper-1 model with segment‑level timestamps.

Formats each segment as:

Code
[MM:SS] text
Saves the final transcript as VIDEO_ID.txt in data/.

Output:  
A structured transcript ready for chunking and embedding.

Notebook 3 — Chunk & Embed
Transforms the transcript into vector embeddings stored in Pinecone.

Key features:

Initializes OpenAI and Pinecone using .env credentials.

Loads the transcript associated with the active video ID.

Chunking engine:

~800‑character chunks

15‑word overlap for contextual continuity

Metadata: text, timestamp, video_id, character count

Embedding generation using text-embedding-3-small.

Upserts all vectors into Pinecone under a namespace matching the video ID.

Output:  
A complete vectorized representation of the video, ready for semantic search and RAG.

🚀 End‑to‑End Workflow
Provide a YouTube URL

Download audio (Notebook 1)

Transcribe with Whisper (Notebook 2)

Chunk + embed + store in Pinecone (Notebook 3)

Use the vectors for semantic search or RAG applications

📁 Project Structure
Code
ResuMazing/
│
├── data/
│   ├── VIDEO_ID.mp3
│   ├── VIDEO_ID.txt
│   └── session_state.json
│
├── notebooks/
│   ├── 01_ingestion.ipynb
│   ├── 02_transcription.ipynb
│   └── 03_chunk_embed.ipynb
│
└── README.md
🔧 Requirements
Python 3.10+

ffmpeg installed

Dependencies:

yt-dlp

openai

pinecone-client

python-dotenv

torch (if using Whisper locally)

Environment variables (.env):

Code
OPENAI_API_KEY=...
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=...
🎯 Purpose
This pipeline enables turning long-form YouTube content into structured, searchable knowledge. Ideal for:

Automatic summarization

Q&A systems

Educational content indexing

RAG-powered applications

Interactive dashboards

🤝 Contributing
Contributions, improvements, and feature extensions are welcome.
Feel free to open an issue if you want to expand the project (Streamlit UI, full RAG backend, LangChain integration, etc.).

👤 Author
Marcos Morales — AI Engineering Bootcamp @ Ironhack
Madrid, Spain
