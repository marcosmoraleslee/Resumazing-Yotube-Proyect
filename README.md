# ResuMazing — YouTube RAG Pipeline
A complete end‑to‑end workflow that transforms any YouTube video into searchable, timestamp‑aware knowledge using audio ingestion → transcription → chunking → embeddings → Pinecone.

### 📌 Overview
ResuMazing is a modular pipeline designed to convert YouTube content into structured data suitable for semantic search and Retrieval‑Augmented Generation (RAG).
The project downloads audio, transcribes it with Whisper, chunks the transcript, generates embeddings with OpenAI, and stores them in Pinecone for fast vector search.

The repository is organized into three notebooks, each representing a core stage of the pipeline.

## 🧩 Pipeline Architecture
### Notebook 1 — Ingestion
Handles URL parsing and audio extraction.

### Key features:

Extracts YouTube video IDs from both standard and shortened URLs.

Validates the URL before processing.

Downloads the audio using yt-dlp and saves it as VIDEO_ID.mp3 in data/.

Creates session_state.json to store the active video ID for downstream notebooks.

Output:  
A clean MP3 file and a persistent session state.

### Notebook 2 — Transcription
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

### Notebook 3 — Chunk & Embed
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

### Notebook 4 - RAG Chat Engine (Multi‑Turn + Memory + Debug)

This project includes a production‑ready multi‑turn RAG chat function that powers the conversational experience in ResuMazing. It combines conversation history, query rewriting, Pinecone retrieval, structured prompting, and detailed debugging to deliver grounded, context‑aware responses.

Core Responsibilities
Maintain conversation history across turns

Rewrite user questions into standalone queries for better retrieval

Fetch relevant video chunks from Pinecone

Build a structured LLM prompt using history + context

Generate safe, grounded answers

Track token usage for debugging and cost monitoring

Update memory with each interaction

How the Chat Function Works
Load Conversation State  
Retrieves previous messages and checks if the user is starting a new session.

Rewrite the Question  
Converts the user query into a standalone form optimized for semantic search.

Retrieve Context from Pinecone  
Performs vector search and assembles a clean context block with timestamps.

Save User Message  
Adds the new user message to the session history.

Format Conversation History  
Converts the full history into a readable text block for the prompt.

Build the RAG Prompt  
Includes:

System persona

First‑message behavior

Conversation history

Retrieved video context

User question
Ensures friendly tone, grounded answers, and no hallucinations.

Generate the Response  
Calls the LLM and captures:

Prompt tokens

Completion tokens

Total cost

Debug Output  
Prints detailed diagnostics:

Timestamp

Session ID

First‑message flag

Token breakdown

OpenAI usage

Question + answer

Save Assistant Response  
Stores the generated answer in the conversation history.

Result
A robust, fully‑featured RAG chat engine supporting:

Multi‑turn memory

Query rewriting

Pinecone retrieval

Timestamp‑aware context

Structured prompting

Token accounting

Safe, grounded responses

This function serves as the backbone of the conversational experience in both the notebook pipeline and the Streamlit application.


## 🖥️ Streamlit Application (Production Phase)
The project is currently evolving from a notebook‑based pipeline into a fully interactive Streamlit application. This app will serve as the front‑end layer of ResuMazing, allowing users to process YouTube videos and interact with the RAG system in a clean, intuitive interface.

Current Progress
We are actively developing the Streamlit UI and several core features are already functional:

YouTube Link Ingestion (Working):  
Users can paste a YouTube URL directly into the app.
The ingestion service validates the link, extracts the video ID, and triggers the audio download pipeline seamlessly.

Model Conversation (Working):  
The chat interface is operational.
Users can ask questions about the processed video, and the app retrieves relevant chunks from Pinecone to generate accurate, context‑aware responses.

Session Management (Working):  
The app maintains state across user actions using st.session_state, ensuring smooth transitions between ingestion, processing, and chat.

In Progress
We are refining the user experience and adding new capabilities:

Improved UX/UI:  
Enhancing layout, spacing, mobile responsiveness, and visual hierarchy.
Adjusting container spacing, centering elements (such as the logo), and improving readability.

Additional Features:

Suggested questions based on the video content

Progress indicators during ingestion and transcription

Optional voice input for asking questions

Better error handling and user feedback

Cleaner modular structure (modules/ folder for services and UI utilities)

Goal of the Streamlit App
The final application will allow users to:

Paste a YouTube link

Process the video end‑to‑end (audio → transcript → chunks → embeddings)

View a summary of the video

Ask questions via text or voice

Receive precise answers powered by Pinecone + OpenAI

Enjoy a polished, modern UI inspired by tools like NotebookLM

This Streamlit layer transforms the pipeline into a real product—accessible, interactive, and ready for demos or deployment.

<img width="1837" height="815" alt="image" src="https://github.com/user-attachments/assets/3a5a209c-afa8-4347-88ad-2489b0216d52" />

<img width="1762" height="847" alt="image" src="https://github.com/user-attachments/assets/2e4a9c94-a103-4334-a850-9c983232603a" />

<img width="1782" height="857" alt="image" src="https://github.com/user-attachments/assets/32a95bde-ba24-43c2-b1c8-c567090f34fd" />




🤝 Contributing
Contributions, improvements, and feature extensions are welcome.
Feel free to open an issue if you want to expand the project (Streamlit UI, full RAG backend, LangChain integration, etc.).

👤 Author
Marcos Morales — AI Engineering Bootcamp @ Ironhack
Madrid, Spain


