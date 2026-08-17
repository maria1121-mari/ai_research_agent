import re


def _to_bibtex(index: int, title: str, authors: list[str], year: str, url: str) -> str:
    first_author_last = authors[0].split()[-1] if authors else "Unknown"
    key = re.sub(r"[^a-zA-Z0-9]", "", f"{first_author_last}{year}")[:20] or f"ref{index}"

    author_field = " and ".join(authors) if authors else "Unknown"

    return (
        f"@article{{{key},\n"
        f"  title = {{{title}}},\n"
        f"  author = {{{author_field}}},\n"
        f"  year = {{{year}}},\n"
        f"  url = {{{url}}}\n"
        f"}}"
    )


def generate_citations(papers_text: str) -> str:
    """
    Parses the formatted papers_text produced by paper_search_tool.search_papers
    and generates a BibTeX entry for each paper. Falls back gracefully if
    parsing or CrossRef lookup fails for any individual entry.
    """
    entries = re.split(r"\n\n(?=\[\d+\])", papers_text.strip())
    citations = []

    for i, entry in enumerate(entries, start=1):
        title_match = re.search(r"\[\d+\]\s*(.+?)\s*\((\d{4}[-\d]*)\)", entry)
        authors_match = re.search(r"Authors:\s*(.+)", entry)
        url_match = re.search(r"URL:\s*(\S+)", entry)

        if not title_match:
            continue

        title = title_match.group(1).strip()
        year = title_match.group(2)[:4]
        authors = [a.strip() for a in authors_match.group(1).replace(" et al.", "").split(",")] if authors_match else []
        url = url_match.group(1) if url_match else ""

        citations.append(_to_bibtex(i, title, authors, year, url))

    if not citations:
        return "No citations could be generated from the retrieved papers."

    return "\n\n".join(citations)