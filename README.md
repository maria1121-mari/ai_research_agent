# 🔬 ResearchMate AI — AI Research Agent

> **Research smarter. Discover faster.**
> An intelligent multi-agent system that turns a single research topic into a structured, citation-ready literature review — powered by **LangGraph**, **FastAPI**, **Groq LLM**, and academic search APIs.

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Why This Project?](#-why-this-project)
3. [Key Features](#-key-features)
4. [System Architecture](#-system-architecture)
5. [The Five AI Agents](#-the-five-ai-agents)
6. [Tech Stack](#-tech-stack)
7. [Project Structure](#-project-structure)
8. [How It Works (Workflow)](#-how-it-works-workflow)
9. [Frontend / UI](#-frontend--ui)
10. [API Endpoints](#-api-endpoints)
11. [Installation & Setup](#-installation--setup)
12. [Environment Variables](#-environment-variables)
13. [Usage](#-usage)
14. [Example Output](#-example-output)
15. [Limitations & Future Work](#-limitations--future-work)
16. [License](#-license)

---

## 🧠 Project Overview

**ResearchMate AI** is an autonomous **multi-agent research assistant** that performs the entire early-stage literature review workflow for a researcher or student in a single click.

Given a research topic (e.g., *"Retrieval-Augmented Generation for question answering"*), the system:

1. Searches **arXiv** and **Semantic Scholar** for relevant academic papers.
2. Summarizes each paper's contribution.
3. Compares methodologies across papers.
4. Identifies **research gaps** using fresh web context (Tavily).
5. Generates **BibTeX citations** and a final formatted report.

All of this is orchestrated by a **LangGraph state machine** with **SQLite-based checkpointing**, exposed through a **FastAPI** backend and a clean, modern web UI.

---

## 🎯 Why This Project?

Conducting a literature review is one of the most time-consuming parts of any research project. Researchers often spend **weeks** simply collecting, reading, comparing, and citing papers. ResearchMate AI compresses this workflow into **seconds** by:

- ⚡ **Automating discovery** across multiple academic databases.
- 🧩 **Decomposing** the research task into specialized AI agents.
- 📊 **Structuring** raw findings into academic-grade output.
- 🔗 **Generating ready-to-use citations** in BibTeX format.

It's not meant to replace a human researcher — it's meant to **accelerate** the discovery and synthesis phase.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔁 **Multi-Agent Pipeline** | 5 specialized AI agents working in sequence via LangGraph. |
| 📚 **Academic Search** | Pulls papers from arXiv + Semantic Scholar. |
| 🌐 **Web Augmentation** | Uses Tavily to enrich gap analysis with fresh web context. |
| 🧠 **LLM-Powered Synthesis** | Uses Groq-hosted `openai/gpt-oss-20b` for reasoning. |
| 📝 **Structured Reports** | Final output follows academic review structure (6 sections). |
| 📎 **BibTeX Citations** | Auto-generated citations for every referenced paper. |
| 💾 **Persistent Memory** | SQLite checkpoints allow thread-based state persistence. |
| 🌐 **Modern Web UI** | Glassmorphic, responsive frontend with progress tracking. |
| ⚡ **FastAPI Backend** | High-performance async API with proper error handling. |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER (Browser)                       │
│                  Templates / Static (JS + CSS)              │
└──────────────────────────┬──────────────────────────────────┘
                           │  POST /api/research
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       FastAPI (app.py)                      │
│   • Serves HTML / static files                              │
│   • Validates request payload                               │
│   • Returns structured JSON report                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              LangGraph Workflow (backend.py)                │
│                                                             │
│   START → Search → Summarize → Compare → Gaps → Cite → END │
│                                                             │
│   State persisted via SQLite Checkpointer (research.db)    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     TOOL LAYER (tools/)                     │
│                                                             │
│   • paper_search_tool.py  → arXiv + Semantic Scholar        │
│   • tavily_tool.py        → Web search (Tavily API)         │
│   • citation_tool.py      → BibTeX generation               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 The Five AI Agents

The core of the project is a **LangGraph state graph** with five sequential agents:

### 1️⃣ Paper Search Agent
- **Role:** Discovery.
- **Action:** Queries arXiv (primary) and Semantic Scholar (supplementary).
- **Output:** Formatted list of 6+ papers with title, authors, year, abstract, and URL.

### 2️⃣ Literature Summarizer Agent
- **Role:** Comprehension.
- **Action:** LLM generates a 2–3 sentence factual summary of each paper based on its abstract.
- **Output:** Concise per-paper summaries grounded in the source text.

### 3️⃣ Methodology Comparator Agent
- **Role:** Analysis.
- **Action:** Compares approaches, datasets, strengths, and limitations across the papers.
- **Output:** A structured methodology comparison (with optional table).

### 4️⃣ Research Gap Agent
- **Role:** Critical Insight.
- **Action:** Combines methodology comparison with **fresh Tavily web context** to surface emerging issues.
- **Output:** 4–6 actionable research gaps with reasoning.

### 5️⃣ Citation Agent (Final Report)
- **Role:** Synthesis.
- **Action:** Generates BibTeX entries and produces the final 6-section academic report.
- **Output:** Final research report + citations.

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** — Async web framework
- **Uvicorn** — ASGI server
- **LangGraph** — Stateful multi-agent orchestration
- **LangChain** — LLM tooling
- **LangChain-Groq** — LLM provider (`openai/gpt-oss-20b`)
- **SQLite** — Persistent checkpointer for graph state

### AI / Search
- **arXiv API** — Academic paper search
- **Semantic Scholar API** — Supplementary academic search
- **Tavily** — Real-time web search for gap analysis
- **Groq LLM** — Fast inference for agent reasoning

### Frontend
- **HTML5 + CSS3** (glassmorphic UI with `Inter` font)
- **Vanilla JavaScript** — Async research requests, progress tracking, copy-to-clipboard
- **Jinja2** — HTML templating

### Utilities
- **pydantic** — Request validation
- **python-dotenv** — Environment management
- **pypdf / pdfplumber** — PDF parsing (available for future enhancements)
- **bibtexparser / crossrefapi** — Citation tooling

---

## 📁 Project Structure

```
AI-Research-agent/
├── app.py                       # FastAPI application + endpoints
├── backend.py                   # LangGraph workflow + agents
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE
├── ai_research_agent_architecture.html   # Visual architecture diagram
│
├── templates/
│   └── index.html               # Main UI
│
├── static/
│   ├── style.css                # Glassmorphic styling
│   └── script.js                # Frontend interactions
│
└── tools/
    ├── paper_search_tool.py     # arXiv + Semantic Scholar search
    ├── tavily_tool.py           # Web search via Tavily
    └── citation_tool.py         # BibTeX generation
```

---

## 🔄 How It Works (Workflow)

```
User Input
   │
   ▼
[1] Paper Search Agent        → arXiv + Semantic Scholar
   │
   ▼
[2] Literature Summarizer     → LLM summaries per paper
   │
   ▼
[3] Methodology Comparator    → Cross-paper comparison
   │
   ▼
[4] Research Gap Agent        → Methodology + Tavily web context
   │
   ▼
[5] Citation Agent            → BibTeX + Final 6-section report
   │
   ▼
JSON Response → Frontend rendering
```

Each agent **appends** to a shared `ResearchState` (TypedDict), and the graph uses a **SQLite-based checkpointer** so conversations can be resumed by `thread_id`.

---

## 🖥️ Frontend / UI

The UI is a single-page interface (`templates/index.html`) with:

- ✨ **Animated background glows**
- 🧭 **Navigation bar** with "AI Agent Online" status indicator
- 📝 **Research topic input** with character counter
- 💡 **Example chips** for quick demo topics
- 🔄 **Live progress bar** with per-agent status updates
- 📊 **Result stats** (papers found, AI calls, gap analysis)
- 📋 **One-click copy** of the full report
- ⚠️ **Error handling** with dismissible error banners

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET`  | `/`              | Render the main UI |
| `POST` | `/api/research`  | Run the multi-agent research pipeline |
| `GET`  | `/health`        | Health check |
| `GET`  | `/favicon.ico`   | Favicon stub |

### `POST /api/research` — Request Body

```json
{
  "message": "Retrieval-Augmented Generation for question answering",
  "thread_id": "user_abc123"
}
```

### Response

```json
{
  "success": true,
  "thread_id": "user_abc123",
  "answer": "1. Research Overview ... 6. References ...",
  "papers_found": "[1] Title ... [2] Title ...",
  "summaries": "Paper 1: ... Paper 2: ...",
  "methodology_comparison": "Comparison table ...",
  "research_gaps": "Gap 1: ...",
  "citations": "@article{...} ...",
  "llm_calls": 5
}
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/maria2021831011/AI-Research-agent.git
cd AI-Research-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
SEMANTIC_SCHOLAR_API_KEY=optional_but_recommended
```

### 5. Run the server

```bash
python app.py
```

The app will be available at **http://127.0.0.1:8000**.

---

## 🔐 Environment Variables

| Variable | Required? | Purpose |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | LLM inference (Groq) |
| `TAVILY_API_KEY` | ✅ Yes | Web search for gap analysis |
| `SEMANTIC_SCHOLAR_API_KEY` | ❌ Optional | Higher rate limits on Semantic Scholar |

---

## 🚀 Usage

1. Open **http://127.0.0.1:8000** in your browser.
2. Enter a research topic (e.g., *"Large Language Model hallucination detection"*).
3. Click **"Run Research Agent"**.
4. Watch the agent progress bar tick through:
   - 🔍 Searching
   - 📄 Analyzing
   - ⚖️ Comparing
   - 💡 Finding gaps
5. Read the final structured report and copy it to your clipboard.

---

## 📄 Example Output

> **Topic:** `Explainable AI for healthcare prediction`

The system produces a report with the following sections:

1. **Research Overview** — High-level framing of the topic.
2. **Literature Summary** — Per-paper concise summaries.
3. **Methodology Comparison** — Table or list comparing approaches.
4. **Identified Research Gaps** — 4–6 actionable gaps.
5. **Suggested Next Steps** — Concrete follow-up ideas.
6. **References (BibTeX)** — Ready-to-use citations.

---

## 🔭 Limitations & Future Work

- **Citation metadata** is derived from paper abstracts and may need manual verification before formal publication.
- **PDF deep-parsing** is scaffolded but not yet integrated into the main pipeline.
- **No vector store** — searches are keyword-based; semantic retrieval could improve relevance.
- **Single-language output** — future versions could support multilingual reports.

### Planned Enhancements
- 📄 PDF upload + full-text analysis
- 🧠 Vector-based semantic retrieval (FAISS / Chroma)
- 📊 Citation graph visualization
- 🌍 Multi-language report generation
- ☁️ Cloud deployment (Docker + Render/Railway)

---

## 📜 License

This project is licensed under the terms specified in the [LICENSE](./LICENSE) file.

---

## 🙌 Acknowledgements

- **LangGraph** & **LangChain** for the agent orchestration framework.
- **Groq** for blazing-fast LLM inference.
- **arXiv**, **Semantic Scholar**, and **Tavily** for open data and search.
- **FastAPI** for the elegant backend framework.

---

> 💡 *Built with LangGraph + FastAPI • ResearchMate AI — Intelligent Literature Research Assistant*
