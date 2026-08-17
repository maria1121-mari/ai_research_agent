import os
import certifi
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from typing import TypedDict, Annotated
import operator
import uuid
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from tools.tavily_tool import tavily_search
from tools.paper_search_tool import search_papers
from tools.citation_tool import generate_citations

import sqlite3


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")


# =========================
# LLM
# =========================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


class ResearchState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    research_topic: str
    papers_found: str
    summaries: str
    methodology_comparison: str
    research_gaps: str
    citations: str
    llm_calls: int


# =========================
# 1. Paper Search Agent
# =========================

def paper_search_agent(state: ResearchState):
    topic = state["research_topic"]
    papers = search_papers(topic)

    return {
        "papers_found": papers,
        "messages": [
            AIMessage(content="Papers retrieved from arXiv / Semantic Scholar.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# =========================
# 2. Literature Summarizer Agent
# =========================

def literature_summarizer_agent(state: ResearchState):
    prompt = f"""
Summarize the key findings of the literature below for the research topic:
"{state['research_topic']}"

Papers:
{state['papers_found']}

For each paper, give a concise 2-3 sentence summary of its core contribution,
approach, and result. Keep the summaries factual and grounded in the abstracts provided.
"""

    response = llm.invoke([
        SystemMessage(content="You are an expert research literature reviewer."),
        HumanMessage(content=prompt)
    ])

    return {
        "summaries": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# =========================
# 3. Methodology Comparator Agent
# =========================

def methodology_comparator_agent(state: ResearchState):
    prompt = f"""
Compare the methodologies used across the papers below for the topic:
"{state['research_topic']}"

Paper Summaries:
{state['summaries']}

Produce a structured comparison covering:
- Approach / technique used by each paper
- Datasets or benchmarks (if mentioned)
- Strengths and limitations
- How the methodologies differ from one another

Present this as a clear comparison, using a table if useful.
"""

    response = llm.invoke([
        SystemMessage(content="You are an expert at comparing research methodologies."),
        HumanMessage(content=prompt)
    ])

    return {
        "methodology_comparison": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# =========================
# 4. Research Gap Agent
# =========================

def research_gap_agent(state: ResearchState):
    # Pull in a bit of fresh web context to help spot recent/emerging gaps
    web_context = tavily_search(f"open research problems and future work in {state['research_topic']}")

    prompt = f"""
Based on the methodology comparison and additional web context below, identify
research gaps and under-explored areas for the topic:
"{state['research_topic']}"

Methodology Comparison:
{state['methodology_comparison']}

Additional Web Context:
{web_context}

List 4-6 specific, actionable research gaps. For each gap, briefly explain
why it matters and what a follow-up study could investigate.
"""

    response = llm.invoke([
        SystemMessage(content="You are an expert research advisor identifying novel research directions."),
        HumanMessage(content=prompt)
    ])

    return {
        "research_gaps": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# =========================
# 5. Citation Agent (+ Final Report)
# =========================

def citation_agent(state: ResearchState):
    citations = generate_citations(state["papers_found"])

    final_prompt = f"""
Generate the final research report for the user.

Research Topic:
{state['research_topic']}

Literature Summaries:
{state['summaries']}

Methodology Comparison:
{state['methodology_comparison']}

Research Gaps:
{state['research_gaps']}

Citations (BibTeX):
{citations}

Format the final answer using these sections:

1. Research Overview
2. Literature Summary
3. Methodology Comparison
4. Identified Research Gaps
5. Suggested Next Steps
6. References (BibTeX)

Important:
- Be clear, structured, and academically rigorous.
- Note that citation metadata is derived from paper abstracts and may need verification before formal use.
"""

    response = llm.invoke([
        SystemMessage(content="You are a professional AI research assistant producing a literature review report."),
        HumanMessage(content=final_prompt)
    ])

    return {
        "citations": citations,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# Checkpointer
conn = sqlite3.connect(database="research.db", check_same_thread=False)
checkpoint = SqliteSaver(conn)


# =========================
# Build Graph
# =========================

graph = StateGraph(ResearchState)

graph.add_node("paper_search_agent", paper_search_agent)
graph.add_node("literature_summarizer_agent", literature_summarizer_agent)
graph.add_node("methodology_comparator_agent", methodology_comparator_agent)
graph.add_node("research_gap_agent", research_gap_agent)
graph.add_node("citation_agent", citation_agent)

graph.add_edge(START, "paper_search_agent")
graph.add_edge("paper_search_agent", "literature_summarizer_agent")
graph.add_edge("literature_summarizer_agent", "methodology_comparator_agent")
graph.add_edge("methodology_comparator_agent", "research_gap_agent")
graph.add_edge("research_gap_agent", "citation_agent")
graph.add_edge("citation_agent", END)


research_graph = graph.compile(checkpointer=checkpoint)


# =========================
# Function for FastAPI
# =========================

def run_research_agent(user_input: str, thread_id: str | None = None):
    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = research_graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "research_topic": user_input,
            "papers_found": "",
            "summaries": "",
            "methodology_comparison": "",
            "research_gaps": "",
            "citations": "",
            "llm_calls": 0
        },
        config=config
    )

    final_answer = result["messages"][-1].content

    return {
        "thread_id": thread_id,
        "answer": final_answer,
        "papers_found": result.get("papers_found", ""),
        "summaries": result.get("summaries", ""),
        "methodology_comparison": result.get("methodology_comparison", ""),
        "research_gaps": result.get("research_gaps", ""),
        "citations": result.get("citations", ""),
        "llm_calls": result.get("llm_calls", 0),
    }


# response = run_research_agent("Retrieval-Augmented Generation for question answering")
# print(response)