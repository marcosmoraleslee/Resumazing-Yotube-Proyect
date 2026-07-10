from dotenv import load_dotenv

from langchain.tools import tool
from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from notebookpy.cv_agent import optimize_cv


# ============================================================
# Environment
# ============================================================

load_dotenv()


# ============================================================
# LLM
# ============================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
)


# ============================================================
# Tool
# ============================================================

@tool
def optimize_resume_tool(
    pdf_path: str,
    video_id: str,
) -> str:
    """
    Optimize a resume using an uploaded PDF and the
    knowledge extracted from a YouTube video.
    """
    return optimize_cv(
        pdf_path=pdf_path,
        video_id=video_id,
    )


# ============================================================
# Prompt
# ============================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI Resume Retrieval Agent.

Your task is to optimize resumes.

When the user provides a PDF path and a YouTube video ID,
use the available tool.

Do not answer from your own knowledge.

Always use the tool.
"""
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


# ============================================================
# Agent
# ============================================================

agent = create_tool_calling_agent(
    llm=llm,
    tools=[optimize_resume_tool],
    prompt=prompt,
)


# ============================================================
# Executor
# ============================================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=[optimize_resume_tool],
    verbose=False,
    max_iterations=2, # MAX ITERATIONS SET TO 2 TO AVOID INFINITE LOOPING
    early_stopping_method="force",
)


# ============================================================
# Public Function
# ============================================================

def optimize_resume(
    pdf_path: str,
    video_id: str,
) -> str:
    """
    Execute the AI Retrieval Agent.
    """

    response = agent_executor.invoke(
        {
            "input": (
                f"Optimize the resume located at '{pdf_path}' "
                f"using the YouTube knowledge stored under "
                f"video ID '{video_id}'."
            )
        }
    )

    return response["output"]
