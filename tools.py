from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


# ==========================================
# Tavily Client
# ==========================================

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API")
)


# ==========================================
# TOOL 1: Web Search
# ==========================================

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information
    on a topic. Returns titles, URLs and snippets.
    """

    try:
        result = tavily.search(
            query=query,
            max_results=5
        )

        out = []

        for r in result["results"]:
            out.append(
                f"Title: {r.get('title', '')}\n"
                f"URL: {r.get('url', '')}\n"
                f"Snippet: {r.get('content', '')}"
            )

        return "\n\n-----\n\n".join(out)

    except Exception as e:
        return f"Web search failed: {str(e)}"


# ==========================================
# TOOL 2: URL Scraper
# ==========================================

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from
    a given URL for deeper reading.
    """

    try:

        response = requests.get(
            url,
            timeout=8,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary HTML elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:5000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"