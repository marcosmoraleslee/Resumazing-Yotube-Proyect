# ResuMazing: YouTube-Driven Intelligent CV Optimizer

ResuMazing is an advanced **Retrieval-Augmented Generation (RAG)** system designed to bridge the gap between expert career advice found in YouTube videos and professional resume optimization.

Instead of relying solely on the general knowledge of a Large Language Model (LLM), ResuMazing creates a **private knowledge base** from a specific YouTube video. This allows the system to provide grounded, context-aware, and domain-specific recommendations based exclusively on the selected content.

---

## 🚀 Overview

ResuMazing enables users to interact with the knowledge extracted from a YouTube video through both **text and voice conversations**.

Its main feature is a **Tool-Calling Agent** built with LangChain that analyzes a user's resume in PDF format and optimizes it according to the recommendations extracted from the video.

---

## 🛠️ System Architecture

The project follows a modular Retrieval-Augmented Generation (RAG) pipeline that transforms unstructured video content into searchable knowledge.

### 1. Data Ingestion & Processing

#### Audio Extraction

The system uses **yt-dlp** to download only the audio track from a YouTube video.

Since the goal is to understand what is being said, processing the video itself is unnecessary.

#### Speech-to-Text Transcription

The extracted audio is processed using **OpenAI Whisper-1**, which converts speech into text while preserving precise timestamps.

Each transcript segment includes:

- Transcript text
- Start time
- End time

These timestamps allow the chatbot to reference exactly where specific recommendations appear in the original video.

#### Semantic Chunking

Instead of splitting the transcript into arbitrary blocks, the text is divided into **semantic chunks**.

Each chunk preserves a complete idea and includes a small overlap with neighboring chunks to maintain contextual continuity.

---

## 🧠 Vector Brain

### Embeddings

Every semantic chunk is transformed into a numerical vector using **OpenAI's text-embedding-3-small** model.

Embeddings capture the semantic meaning of text rather than simply matching keywords.

For example:

> "Improve your resume"

and

> "Make your CV stronger"

generate very similar embeddings despite using different words.

### Vector Database

The generated embeddings are stored in **Pinecone** together with:

- Original text
- Video timestamp
- Video identifier
- Additional metadata

This enables fast semantic retrieval based on meaning rather than keyword matching.

---

## 🔍 Retrieval-Augmented Generation (RAG)

When a user asks a question, the system follows several steps.

### Query Rewriting

Before searching the vector database, the user's question is automatically rewritten into a clearer standalone query.

This significantly improves retrieval accuracy, especially during multi-turn conversations.

### Semantic Retrieval

The rewritten question is converted into an embedding.

Pinecone then retrieves the most semantically relevant chunks from the corresponding video.

### Response Generation

The retrieved context is combined with:

- Conversation history
- Memory summary
- User question

and passed to **GPT-4o-mini** to generate the final answer.

The model does not rely solely on its pretrained knowledge but instead generates responses augmented with the retrieved information.

---

## 🛡️ Anti-Hallucination Strategy

One of the main challenges of LLMs is hallucination—the tendency to generate information that does not exist.

To minimize this behavior, ResuMazing combines several techniques:

- Semantic retrieval before generation
- Carefully engineered prompts
- Explicit instructions to answer only using retrieved content
- Timestamp-aware context
- Responses that acknowledge when the video does not contain the requested information

This keeps responses grounded in the original source material.

---

## 🤖 Tool-Calling Agent

One of the key features of ResuMazing is a **Tool-Calling Agent** implemented using LangChain.

Unlike a traditional chatbot, this type of agent can execute external tools to complete specialized tasks.

### Resume Optimization Tool

When the user uploads a PDF resume, the agent automatically executes a dedicated optimization tool.

The workflow is:

1. Extract text from the uploaded PDF.
2. Retrieve ATS-related recommendations from Pinecone.
3. Compare the resume with the retrieved knowledge.
4. Generate an improved version of the CV using GPT-4o-mini.

The system never invents professional experience or qualifications.

Instead, it:

- Improves wording
- Reorganizes sections
- Enhances readability
- Incorporates ATS-friendly recommendations extracted from the video

### Agent Configuration

The Tool-Calling Agent is executed using **AgentExecutor** with the following configuration:

- **max_iterations = 2**
  - Prevents unnecessary reasoning loops.
  - Reduces execution time and token consumption.

- **early_stopping_method = "force"**
  - Ensures the agent always returns a response, even if the iteration limit is reached.

- **verbose = True**
  - Displays every reasoning step during development, making debugging significantly easier.

---

## 💬 Conversational Memory

To maintain natural conversations, ResuMazing implements a hybrid memory strategy.

Instead of sending the entire conversation back to the model every time, the system combines:

- Recent conversation history
- Automatic conversation summaries

This compressed memory preserves important context while significantly reducing token consumption.

---

## 🎙️ Voice Interface

The application is built with **Streamlit** and supports both text and voice interaction.

When the user speaks:

1. Streamlit records the audio.
2. Whisper-1 transcribes the speech.
3. The resulting text enters exactly the same RAG pipeline used for typed questions.

From that point onward, voice and text follow an identical processing workflow.

---

## 🏗️ Technology Stack

### Large Language Model

- GPT-4o-mini

### Speech Recognition

- Whisper-1

### Embeddings

- text-embedding-3-small

### Framework

- LangChain
- AgentExecutor
- Tool-Calling Agent

### Vector Database

- Pinecone

### Frontend

- Streamlit

### Supporting Libraries

- yt-dlp
- PyPDF
- python-dotenv

---

## 🔮 Future Scalability

Because the application is based on a Tool-Calling Agent architecture, adding new capabilities requires only registering additional tools.

Potential future extensions include:

- Automatic cover letter generation
- LinkedIn profile optimization
- Interview preparation
- Personalized career coaching
- Multi-document analysis

---

## 🎯 Conclusion

ResuMazing demonstrates how modern AI technologies—including Large Language Models, Retrieval-Augmented Generation, semantic search, vector databases, and Tool-Calling Agents—can be combined into a practical application.

Rather than relying on generic AI knowledge, the system transforms YouTube videos into searchable private knowledge bases that users can interact with naturally through text, voice, and intelligent document analysis.

**ResuMazing — Turning video insights into professional opportunities.**
