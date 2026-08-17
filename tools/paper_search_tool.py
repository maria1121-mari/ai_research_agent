import os
import arxiv

SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")  # optional


def search_papers_arxiv(topic: str, max_results: int = 6) -> list[dict]:
    """
    Search arXiv for papers matching the topic.
    No API key required.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []
    for result in client.results(search):
        papers.append({
            "title": result.title.strip(),
            "authors": [a.name for a in result.authors],
            "published": result.published.strftime("%Y-%m-%d") if result.published else "",
            "summary": result.summary.strip().replace("\n", " "),
            "url": result.entry_id,
            "pdf_url": result.pdf_url,
            "source": "arXiv",
        })
    return papers


def search_papers_semantic_scholar(topic: str, max_results: int = 6) -> list[dict]:
    """
    Search Semantic Scholar for papers matching the topic.
    Works without an API key (lower rate limit); set SEMANTIC_SCHOLAR_API_KEY to raise limits.
    """
    try:
        from semanticscholar import SemanticScholar
        sch = SemanticScholar(api_key=SEMANTIC_SCHOLAR_API_KEY) if SEMANTIC_SCHOLAR_API_KEY else SemanticScholar()
        results = sch.search_paper(topic, limit=max_results)

        papers = []
        for r in results[:max_results]:
            papers.append({
                "title": r.title or "",
                "authors": [a["name"] for a in (r.authors or [])],
                "published": str(r.year) if r.year else "",
                "summary": (r.abstract or "").replace("\n", " "),
                "url": r.url or "",
                "pdf_url": (r.openAccessPdf or {}).get("url", "") if r.openAccessPdf else "",
                "source": "Semantic Scholar",
            })
        return papers
    except Exception as e:
        print(f"[Semantic Scholar] search failed: {e}")
        return []


def search_papers(topic: str, max_results: int = 6) -> str:
    """
    Combines arXiv + Semantic Scholar results into a single formatted
    string that is easy to feed into the LLM downstream.
    """
    papers = search_papers_arxiv(topic, max_results=max_results)

    if not papers:
        papers = search_papers_semantic_scholar(topic, max_results=max_results)
    else:
        papers += search_papers_semantic_scholar(topic, max_results=max(2, max_results // 2))

    if not papers:
        return "No papers found for this topic."

    formatted = []
    for i, p in enumerate(papers, start=1):
        authors = ", ".join(p["authors"][:4]) + (" et al." if len(p["authors"]) > 4 else "")
        formatted.append(
            f"[{i}] {p['title']} ({p['published']}) - {p['source']}\n"
            f"    Authors: {authors}\n"
            f"    URL: {p['url']}\n"
            f"    Abstract: {p['summary'][:600]}"
        )

    return "\n\n".join(formatted)