import os
from langchain_tavily import TavilySearch

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing. Please add it to your .env file.")

_tavily = TavilySearch(max_results=5, api_key=TAVILY_API_KEY)


def tavily_search(query: str) -> str:
    """
    Runs a web search via Tavily and returns a compact formatted string.
    Used as a fallback / supplement to academic paper search sources.
    """
    try:
        results = _tavily.invoke({"query": query})
        items = results.get("results", []) if isinstance(results, dict) else results

        if not items:
            return "No web results found."

        formatted = []
        for i, item in enumerate(items, start=1):
            title = item.get("title", "")
            url = item.get("url", "")
            content = item.get("content", "")[:400]
            formatted.append(f"[{i}] {title}\n    URL: {url}\n    {content}")

        return "\n\n".join(formatted)
    except Exception as e:
        return f"Tavily search failed: {e}"