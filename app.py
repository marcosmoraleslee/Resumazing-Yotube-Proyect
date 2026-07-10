import sys
import os

import streamlit as st

from notebookpy.ingest import download_youtube_audio
from notebookpy.transcribe import transcribe_audio
from notebookpy.chunk_embed import embed_and_upsert
from notebookpy.chat_rag import chat
from notebookpy.summary import generate_video_summary
from notebookpy.retrieval_agent import optimize_resume
from notebookpy.audio_input import transcribe_user_audio

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="ResuMazing",
    page_icon="📄",
    layout="centered"
)


# ============================================================
# Session State Initialization
# ============================================================

if "video_id" not in st.session_state:
    st.session_state.video_id = None


if "youtube_url" not in st.session_state:
    st.session_state.youtube_url = None


if "session_id" not in st.session_state:
    st.session_state.session_id = "streamlit_user"


if "messages" not in st.session_state:
    st.session_state.messages = []


if "summary" not in st.session_state:
    st.session_state.summary = None


if "chat_interactions" not in st.session_state:
    st.session_state.chat_interactions = 0


if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0


if "cv_result" not in st.session_state:
    st.session_state.cv_result = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None



# ============================================================
# Header
# ============================================================


col1, col2, col3 = st.columns([2, 4, 2])


with col2:

    left, center, right = st.columns([1, 4, 1])

    with center:

        st.image(
            "logo.png",
            width=400
        )



st.markdown(
    """
    <div style="
        text-align: center;
        font-size: clamp(24px, 4vw, 32px);
        font-weight: 700;
        width: 100%;
        line-height: 1.2;
        padding: 0 10px;
    ">
        Stop being ignored by the filters
    </div>
    """,
    unsafe_allow_html=True
)



st.write("")




# ============================================================
# Video Analysis
# ============================================================

st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] label {
        width: 100%;
        text-align: center;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)


youtube_url = st.text_input(
    "Paste a CV-creation YouTube link and *resumazing turns it into your perfect resume."
)


if st.button(
    "Process Video",
    use_container_width=True
):


    if not youtube_url:

        st.warning(
            "Please enter a YouTube URL."
        )


    else:

        progress = st.progress(0)

        status = st.empty()


        try:


            status.info(
                "Downloading YouTube audio..."
            )


            video_id, audio_path = download_youtube_audio(
                youtube_url
            )


            progress.progress(25)



            status.info(
                "Transcribing audio..."
            )


            transcribe_audio(
                audio_path,
                video_id
            )


            progress.progress(50)



            status.info(
                "Creating embeddings and uploading to Pinecone..."
            )


            embed_and_upsert(
                transcript_path=f"data/{video_id}.txt",
                video_id=video_id
            )


            progress.progress(75)



            status.info(
                "Generating video summary..."
            )


            summary = generate_video_summary(
                video_id
            )


            st.session_state.summary = summary


            progress.progress(100)



            # Save pipeline state

            st.session_state.video_id = video_id

            st.session_state.youtube_url = youtube_url



            # Reset chat for new video

            st.session_state.messages = []

            st.session_state.chat_interactions = 0

            st.session_state.chat_count = 0

            st.session_state.cv_result = None



            status.success(
                "Video analyzed successfully!"
            )


            st.write(
                f"Active video: `{video_id}`"
            )



        except Exception as e:

            st.error(
                f"Pipeline failed: {e}"
            )



# ============================================================
# Video Preview & Summary
# ============================================================

if st.session_state.video_id:


    st.divider()


    st.subheader(
        "Video"
    )


    youtube_video_url = (
        f"https://www.youtube.com/watch?v={st.session_state.video_id}"
    )


    st.video(
        youtube_video_url
    )



    st.divider()


    
    if st.session_state.summary:

        st.write(
            st.session_state.summary
        )

    else:

        st.info(
            "Generating summary..."
        )



# ============================================================
# Chat Interface
# ============================================================


if st.session_state.video_id:


    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(
                message["content"]
            )



    # --------------------------------------------------------
    # Chat Input (Text + Voice)
    # --------------------------------------------------------

    question = None


    chat_input = st.chat_input(
        "Ask something about the video...",
        accept_audio=True,
        audio_sample_rate=16000,
    )



    if chat_input:


        # Text input

        if chat_input.text:

            question = chat_input.text



        # Voice input

        elif chat_input.audio:

            with st.spinner(
                "Transcribing voice..."
            ):

                question = transcribe_user_audio(
                    chat_input.audio
                )



    # --------------------------------------------------------
    # RAG Chat
    # --------------------------------------------------------

    if question:


        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # Count only user questions

        st.session_state.chat_count += 1



        with st.chat_message("user"):

            st.write(
                question
            )



        response = chat(
            session_id=st.session_state.session_id,
            video_id=st.session_state.video_id,
            question=question
        )



        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


        st.session_state.chat_interactions += 1



        with st.chat_message("assistant"):

            st.write(
                response
            )


# ============================================================
# CV Optimization Section
# ============================================================

if st.session_state.video_id and st.session_state.chat_count >= 5:


    st.divider()


    st.subheader(
        "Optimize your CV with this video"
    )


    st.write(
        """
After discussing the video, you can upload your current CV.

ResuMazing will analyze it against the video recommendations
and generate an optimized version.
        """
    )



    uploaded_cv = st.file_uploader(
        "Upload your CV (PDF)",
        type=["pdf"]
    )



    if uploaded_cv:


        if st.button("Analyze my CV"):


            with st.spinner(
                "Analyzing your CV..."
            ):


                result = optimize_resume(
                    uploaded_cv,
                    st.session_state.video_id
                )


                st.session_state.cv_result = result



    if st.session_state.cv_result:


        st.divider()


        st.subheader(
            "Here is your Optimized CV"
        )


        st.write(
            st.session_state.cv_result
        )
