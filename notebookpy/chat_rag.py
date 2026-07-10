from datetime import datetime
import os
from click import prompt
import tiktoken

from dotenv import load_dotenv
from pinecone import Pinecone

from langchain_openai import OpenAIEmbeddings, ChatOpenAI


# ============================================================
# Environment
# ============================================================

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found.")

if not PINECONE_INDEX_NAME:
    raise ValueError("PINECONE_INDEX_NAME not found.")


# ============================================================
# Clients
# ============================================================

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    PINECONE_INDEX_NAME
)


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


rewrite_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ============================================================
# Conversation Memory
# ============================================================

conversation_store = {}


def get_state(session_id: str):

    if session_id not in conversation_store:

        conversation_store[session_id] = {
            "chat_history": []
        }

    return conversation_store[session_id]



def add_message(
    session_id: str,
    role: str,
    message: str
):

    state = get_state(session_id)

    state["chat_history"].append(
        {
            "role": role,
            "message": message
        }
    )



def format_history(chat_history):

    return "\n".join(
        [
            f"{item['role']}: {item['message']}"
            for item in chat_history
        ]
    )



# ============================================================
# Question Rewriting
# ============================================================

def rewrite_question(
    question: str,
    chat_history: list
):

    if not chat_history:
        return question


    history_text = format_history(
        chat_history
    )


    prompt = f"""

Rewrite the user question into a standalone query.

Rules:

- If FIRST_MESSAGE is True, start with:
"Welcome to ResuMazing!"

- Be friendly and practical.
- Use conversation history when answering personal questions.
- Use video context for resume and ATS questions.
- When you use information from the Video Context, preserve and cite the timestamp exactly as provided.
- Never invent timestamps.
- Never invent information.
- If information is missing, explain that clearly.

Conversation history:

{history_text}


User question:

{question}


Standalone query:

"""


    response = rewrite_llm.invoke(
        prompt
    )


    return response.content.strip()



# ============================================================
# Retrieval
# ============================================================

def retrieve(
    query: str,
    video_id: str,
    top_k: int = 4
):

    query_embedding = embeddings.embed_query(
        query
    )


    return index.query(
        vector=query_embedding,
        namespace=video_id,
        top_k=top_k,
        include_metadata=True
    )



def build_context(results):

    if not results:
        return ""

    chunks = []

    for match in results.matches:

        metadata = match.metadata or {}

        text = metadata.get("text", "")

        timestamp = metadata.get("timestamp")

        if not timestamp:

            start = metadata.get("start")

            if start is not None:

                minutes = int(start // 60)
                seconds = int(start % 60)

                timestamp = f"{minutes:02}:{seconds:02}"

            else:

                timestamp = ""

        if text:

            if timestamp:
                chunks.append(
                    f"{timestamp} {text}"
                )
            else:
                chunks.append(text)

    return "\n\n".join(chunks)



# ============================================================
# Token counter
# ============================================================

encoder = tiktoken.encoding_for_model(
    "gpt-4o-mini"
)


def count_tokens(text: str):

    return len(
        encoder.encode(text)
    )



# ============================================================
# Main RAG Chat
# ============================================================

def chat(
    session_id: str,
    video_id: str,
    question: str
):

    state = get_state(
        session_id
    )


    history = state["chat_history"]


    first_message = len(history) == 0



    # -------------------------
    # Rewrite question
    # -------------------------

    standalone_query = rewrite_question(
        question,
        history
    )



    # -------------------------
    # Retrieve video context
    # -------------------------

    results = retrieve(
        standalone_query,
        video_id
    )

    print(type(results))
    print(results)

    # -------------------------
    # DEBUG: Print Pinecone metadata
    # -------------------------

    print("\n================ PINECONE RESULTS ================\n")

    for i, match in enumerate(results.matches, start=1):

        print(f"\n----- Match {i} -----")
        print(match.metadata)

    print("\n==================================================\n")

    context = build_context(
        results
    )


    # -------------------------
    # Save user message
    # -------------------------

    add_message(
        session_id,
        "user",
        question
    )


    history_text = format_history(
        get_state(session_id)["chat_history"]
    )



    # -------------------------
    # Prompt
    # -------------------------

    prompt = f"""

You are ResuMazing, an AI assistant specialized in resume writing,
CV optimization and ATS optimization.

Your goal is to help users improve their resumes using the video
knowledge base and conversation history.

Rules:

- If FIRST_MESSAGE is True, start with:
"Welcome to ResuMazing!"

- Be friendly and practical.
- Use conversation history when answering personal questions.
- Use video context for resume and ATS questions.
- Every factual statement based on the video context MUST include the corresponding timestamp.
- Preserve timestamps exactly as provided in the Video Context.
- Do not answer with information from the video without citing its timestamp.
- Never invent timestamps.
- Never invent information.
- If information is missing, explain that clearly.

FIRST_MESSAGE:

{first_message}


Conversation History:

{history_text}


Video Context:

{context}


User Question:

{question}

"""


    # -------------------------
    # LLM Response
    # -------------------------






    print("\n========== FINAL PROMPT ==========\n")
    print(prompt)
    print("\n==================================\n")

    answer = llm.invoke(
        prompt
    ).content.strip()



    # -------------------------
    # Save assistant message
    # -------------------------

    add_message(
        session_id,
        "assistant",
        answer
    )


    return answer