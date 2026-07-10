import os

from dotenv import load_dotenv
from prompt_toolkit import prompt
from pypdf import PdfReader

from pinecone import Pinecone

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel, Field
from typing import List

load_dotenv()


# ============================================================
# Clients
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


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
    temperature=0.2,
    max_tokens=2000
)



# ============================================================
# Extract CV
# ============================================================

def extract_cv_text(uploaded_file):
    """
    Extract text from a PDF uploaded through Streamlit.
    """

    reader = PdfReader(uploaded_file)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)



# ============================================================
# Retrieve video knowledge
# ============================================================

def retrieve_cv_context(
        query,
        video_id,
        top_k=5
):

    query_embedding = embeddings.embed_query(
        query
    )


    results = index.query(
        vector=query_embedding,
        namespace=video_id,
        top_k=top_k,
        include_metadata=True
    )


    contexts = []


    for match in results["matches"]:

        metadata = match.get(
            "metadata",
            {}
        )

        text = metadata.get(
            "text",
            ""
        )

        if text:
            contexts.append(text)


    return "\n\n".join(contexts)


# ============================================================
# Resume Generation
# ============================================================

def generate_resume(
        cv_text,
        context
):

    prompt = f"""

You are ResuMazing CV Optimization System.

Your task is to improve the user's resume using
knowledge extracted from the analyzed video.

RULES:

- Never invent experience.
- Never add fake skills.
- Preserve the user's background.
- Improve wording and ATS compatibility.
- Use only retrieved knowledge.


USER CV:

{cv_text}


VIDEO KNOWLEDGE:

{context}


Generate an optimized resume with this structure:

1. Professional Summary

2. Skills

3. Experience

4. Education

5. ATS Improvements

"""

    response = llm.invoke(
        prompt
    )

    return response.content


# ============================================================
# CV Optimization
# ============================================================

def optimize_cv(
        pdf_path,
        video_id
):

    cv_text = extract_cv_text(
        pdf_path
    )

    context = retrieve_cv_context(
        query="CV optimization ATS resume improvements keywords",
        video_id=video_id
    )

    return generate_resume(
        cv_text,
        context
    )