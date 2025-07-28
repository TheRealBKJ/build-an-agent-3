"""AskVision Agent - AI Accessibility Assistant for webpage analysis."""

import asyncio
from typing import Any, Dict

from .agent import AskVisionState, graph


async def async_analyze_webpage(
    url: str, question: str, html_content: str
) -> Any | dict[str, Any] | None:
    """Analyze a webpage and answer a question."""
    state = AskVisionState(url=url, question=question, html_content=html_content)
    result = await graph.ainvoke(state)
    return result


def analyze_webpage(url: str, question: str, html_content: str) -> Any | dict[str, Any] | None:
    """Analyze a webpage and answer a question."""
    return asyncio.run(async_analyze_webpage(url, question, html_content)) 