# ResuMazing: YouTube-Driven Intelligent CV Optimizer
ResuMazing is an advanced Retrieval-Augmented Generation (RAG) system designed to bridge the gap between expert advice found in YouTube videos and professional resume building
. Instead of relying on general LLM knowledge, ResuMazing creates a private knowledge base from specific video content to provide grounded, domain-specific resume optimizations
.
🚀 Overview
The system allows users to interact with a YouTube video’s content via text or voice to ask questions and, most importantly, provides a Tool-Calling Agent that analyzes a user's PDF resume and optimizes it based on the specific insights extracted from the video
.
🛠️ System Architecture
The project follows a modular pipeline to transform unstructured video data into actionable intelligence:
1. Data Ingestion & Processing
Audio Extraction: Uses yt-dlp to download the audio track from a YouTube URL
.
Transcription: Employs OpenAI's Whisper-1 to convert audio into text with precise timestamps, allowing the system to reference exactly when a piece of advice was given
.
Semantic Chunking: Content is divided into meaningful blocks rather than arbitrary lengths, ensuring each fragment preserves a complete idea with a small overlap to maintain context
.
2. Vector Brain
Embeddings: Text chunks are converted into mathematical representations of "meaning" using OpenAI embeddings, enabling Semantic Search that understands intent beyond simple keywords
.
Vector Database: All embeddings, metadata, and timestamps are stored in Pinecone for high-speed similarity retrieval
.
3. The RAG Logic
Query Rewriting: To improve retrieval accuracy in multi-turn conversations, the system re-writes user queries into more specific search terms
.
Retrieval-Augmented Generation: Using GPT-4o-mini, the system generates responses "augmented" by the relevant fragments retrieved from Pinecone
.
Anti-Hallucination: Responses are strictly anchored to the retrieved context. If the video doesn't contain the answer, the system is instructed to acknowledge it rather than invent information
.
🤖 The Star Feature: Tool-Calling Agent
The core of ResuMazing is a Tool-Calling Agent built with LangChain. This agent extends the LLM's native capabilities by allowing it to interact with external tools
.
The CV Optimizer Tool: When a user uploads a PDF, the agent triggers a specialized tool that:
Extracts text from the PDF
.
Performs a semantic search for video fragments related to ATS, structure, and keywords
.
Adapts and reorganizes the user's CV content without inventing new experience, ensuring the output is professional and video-aligned
.
Agent Control: To ensure efficiency, the AgentExecutor is configured with:
max_iterations = 2: Limits the reasoning loop to save tokens and prevent infinite cycles
.
early_stopping_method = "force": Guarantees a response even if the maximum iterations are reached
.
verbose = True: Full traceability of the agent's thought process
.
🎙️ Interactive UI
Voice Interface: Built with Streamlit, users can speak their queries. The audio is processed by Whisper-1 and fed into the RAG pipeline as if it were text
.
Memory Management: The system uses a hybrid memory approach (Buffer + Summarization) to maintain long-term context without exceeding token limits
.
🏗️ Tech Stack
LLM: OpenAI GPT-4o-mini
Transcription/Voice: OpenAI Whisper-1
Vector DB: Pinecone
Framework: LangChain (AgentExecutor, Tools)
Interface: Streamlit
Utilities: yt-dlp, Semantic Chunking
🔮 Future Scalability
The agent-based architecture allows for easy expansion. Future tools could include:
Automated Cover Letter generation
.
LinkedIn profile reviews
.
Mock interview generation based on specific video advice.
ResuMazing — Turning video insights into professional opportunities.

