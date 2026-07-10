import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone


# ============================================================
# Environment Setup
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found.")

if not INDEX_NAME:
    raise ValueError("PINECONE_INDEX_NAME not found.")


client = OpenAI(
    api_key=OPENAI_API_KEY
)

pc = Pinecone(
    api_key=PINECONE_API_KEY
)


# ============================================================
# Chunking
# ============================================================

TIMESTAMP_PATTERN = re.compile(
    r"^\[([\d:]+)\]\s*(.*)$"
)


def chunk_transcript_with_timestamps(
    file_path: str,
    video_id: str,
    chunk_size_chars: int = 800,
    overlap_words: int = 15,
):
    """
    Split timestamped transcript into chunks.

    Keeps:
    - text
    - timestamp
    - video_id
    """


    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()


    chunks = []

    current_chunk_text = ""
    current_chunk_timestamp = None


    for line in lines:

        line = line.strip()

        if not line:
            continue


        match = TIMESTAMP_PATTERN.match(line)


        if match:

            timestamp = f"[{match.group(1)}]"
            text = match.group(2)

        else:

            timestamp = None
            text = line


        if timestamp:
            current_chunk_timestamp = timestamp


        current_chunk_text = (
            f"{current_chunk_text} {text}"
        ).strip()


        if len(current_chunk_text) >= chunk_size_chars:

            chunks.append(
                {
                    "text": current_chunk_text,
                    "metadata": {
                        "video_id": video_id,
                        "timestamp": current_chunk_timestamp or "[00:00]",
                        "char_count": len(current_chunk_text),
                    },
                }
            )


            words = current_chunk_text.split()

            current_chunk_text = " ".join(
                words[-overlap_words:]
            )


    if current_chunk_text:

        chunks.append(
            {
                "text": current_chunk_text,
                "metadata": {
                    "video_id": video_id,
                    "timestamp": current_chunk_timestamp or "[00:00]",
                    "char_count": len(current_chunk_text),
                },
            }
        )


    return chunks



# ============================================================
# Embeddings + Pinecone
# ============================================================


def embed_and_upsert(
    transcript_path: str,
    video_id: str
):
    """
    Complete embedding pipeline:

    transcript
        |
        chunks
        |
        embeddings
        |
        Pinecone namespace = video_id
    """


    print("📄 Creating chunks...")


    chunks = chunk_transcript_with_timestamps(
        transcript_path,
        video_id
    )


    print(
        f"✅ Created {len(chunks)} chunks."
    )


    vectors = []


    print("🧠 Generating embeddings...")


    for idx, chunk in enumerate(chunks):

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["text"]
        )


        embedding = response.data[0].embedding


        vector_id = (
            f"{video_id}_chunk_{idx}"
        )


        metadata = {
            "video_id": video_id,
            "timestamp": chunk["metadata"]["timestamp"],
            "text": chunk["text"]
        }


        vectors.append(
            (
                vector_id,
                embedding,
                metadata
            )
        )


    print(
        f"✅ Generated {len(vectors)} embeddings."
    )


    available_indexes = [
        idx.name
        for idx in pc.list_indexes()
    ]


    if INDEX_NAME not in available_indexes:

        raise ValueError(
            f"Pinecone index '{INDEX_NAME}' not found."
        )


    index = pc.Index(INDEX_NAME)


    print(
        f"📤 Uploading vectors..."
    )

    print(
        f"Namespace: {video_id}"
    )


    result = index.upsert(
        vectors=vectors,
        namespace=video_id
    )


    print(
        f"🎉 Uploaded {result.upserted_count} vectors."
    )


    return {
        "video_id": video_id,
        "namespace": video_id,
        "chunks": len(chunks),
        "vectors": result.upserted_count
    }