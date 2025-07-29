"""Custom tools for accessing Atla AI content directly."""

import logging
from typing import Annotated

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def fetch_atla_website(
    path: Annotated[
        str, "Optional path to specific page (e.g., '/about', '/pricing')"
    ] = "/",
) -> str:
    """Fetch content from the main Atla AI website (atla-ai.com).

    This tool directly scrapes the Atla AI website to get current information
    about their platform, products, and services without using rate-limited search.

    Args:
        path: Optional path to specific page, defaults to homepage

    Returns:
        Cleaned text content from the requested page
    """
    url = f"https://www.atla-ai.com{path}"
    logger.info(f"Fetching Atla website: {url}")

    try:
        # Create session with proper headers
        session = requests.Session()
        session.headers.update({"User-Agent": "Narcissus-AtlaAI-Agent/1.0"})

        response = session.get(url, timeout=10)
        response.raise_for_status()

        # Parse HTML and extract meaningful content
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)

        # Limit response size
        if len(text) > 5000:
            text = text[:5000] + "... [content truncated]"

        logger.info(f"Successfully fetched Atla website content ({len(text)} chars)")
        return f"Content from {url}:\n\n{text}"

    except Exception as e:
        logger.error(f"Failed to fetch Atla website: {str(e)}")
        return f"Error fetching {url}: {str(e)}"


# Export the tools for easy import
ATLA_TOOLS = [fetch_atla_website]
