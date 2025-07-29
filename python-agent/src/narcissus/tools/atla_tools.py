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


@tool
def fetch_atla_docs(
    path: Annotated[
        str, "Optional path to specific docs page (e.g., '/getting-started', '/api')"
    ] = "/",
) -> str:
    """Fetch content from the Atla AI documentation site (docs.atla-ai.com).

    This tool directly scrapes the Atla AI docs to get current documentation
    about their platform APIs, SDKs, and integration guides.

    Args:
        path: Optional path to specific docs page, defaults to homepage

    Returns:
        Cleaned text content from the requested docs page
    """
    url = f"https://docs.atla-ai.com{path}"
    logger.info(f"Fetching Atla docs: {url}")

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

        logger.info(f"Successfully fetched Atla docs content ({len(text)} chars)")
        return f"Content from {url}:\n\n{text}"

    except Exception as e:
        logger.error(f"Failed to fetch Atla docs: {str(e)}")
        return f"Error fetching {url}: {str(e)}"


@tool
def fetch_atla_sdk_readme() -> str:
    """Fetch the README from the Atla AI SDK GitHub repository.

    This tool directly fetches the README.md from the atla-insights-sdk repository
    to get current information about SDK installation, usage, and examples.

    Returns:
        Content of the SDK README file
    """
    url = "https://raw.githubusercontent.com/atla-ai/atla-insights-sdk/main/README.md"
    logger.info(f"Fetching Atla SDK README: {url}")

    try:
        # Create session with proper headers
        session = requests.Session()
        session.headers.update({"User-Agent": "Narcissus-AtlaAI-Agent/1.0"})

        response = session.get(url, timeout=10)
        response.raise_for_status()

        content = response.text

        # Limit response size
        if len(content) > 8000:
            content = content[:8000] + "... [content truncated]"

        logger.info(f"Successfully fetched SDK README ({len(content)} chars)")
        return f"Atla AI SDK README:\n\n{content}"

    except Exception as e:
        logger.error(f"Failed to fetch SDK README: {str(e)}")
        return f"Error fetching SDK README: {str(e)}"


@tool
def get_demo_booking_link() -> str:
    """Get the link to book a demo with the Atla AI team.

    Use this when users express interest in:
    - Trying the Atla AI platform
    - Seeing a demo or walkthrough
    - Talking to the team
    - Getting started with implementation
    - Learning more about pricing or enterprise features

    Returns:
        Direct link to book a demo with the Atla AI team
    """
    logger.info("Providing demo booking link to user")
    return """You can book a demo with the Atla AI team here: https://calendly.com/atla-team/agents-demo

This will let you see the platform in action and discuss how Atla AI can help with your specific agent development and monitoring needs."""


# Export the tools for easy import
ATLA_TOOLS = [
    fetch_atla_website,
    fetch_atla_docs,
    fetch_atla_sdk_readme,
    get_demo_booking_link,
]
