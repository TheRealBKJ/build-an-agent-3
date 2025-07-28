"""Content extraction workflow for webpage analysis."""

import json
import logging
from typing import Annotated, Any, Sequence
from bs4 import BeautifulSoup

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from . import tools
from .prompts import content_extraction_prompt

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3

llm = ChatNVIDIA(model="llama-3.3-nemotron-super-49b-v1.5", temperature=0)
llm_with_tools = llm.bind_tools([tools.extract_reviews, tools.extract_pricing, tools.extract_product_info])


class WebpageSection(BaseModel):
    name: str
    description: str
    content: str
    relevance_score: float


class ContentExtractorState(BaseModel):
    url: str
    html_content: str
    sections: list[WebpageSection] = []
    messages: Annotated[Sequence[Any], add_messages] = []


async def tool_node(state: ContentExtractorState):
    """Execute tool calls for content extraction."""
    _LOGGER.info("Executing content extraction tools for URL: %s", state.url)
    outputs = []
    for tool_call in state.messages[-1].tool_calls:
        _LOGGER.info("Executing tool call: %s", tool_call["name"])
        tool = getattr(tools, tool_call["name"])
        tool_result = await tool.ainvoke(tool_call["args"])
        outputs.append(
            {
                "role": "tool",
                "content": json.dumps(tool_result),
                "name": tool_call["name"],
                "tool_call_id": tool_call["id"],
            }
        )
    return {"messages": outputs}


async def extraction_model(
    state: ContentExtractorState,
    config: RunnableConfig,
) -> dict[str, Any]:
    """Call model for content extraction."""
    _LOGGER.info("Extracting content from webpage: %s", state.url)
    
    # Parse HTML content
    soup = BeautifulSoup(state.html_content, 'html.parser')
    
    system_prompt = content_extraction_prompt.format(
        url=state.url,
        html_content=str(soup)[:2000]  # Limit content for token efficiency
    )

    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}] + list(state.messages)
        response = await llm_with_tools.ainvoke(messages, config)

        if response:
            return {"messages": [response]}

        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    raise RuntimeError("Failed to call model after %d attempts.", _MAX_LLM_RETRIES)


def has_tool_calls(state: ContentExtractorState) -> bool:
    """Check if the last message has tool calls."""
    if not state.messages:
        return False
    last_message = state.messages[-1]
    return hasattr(last_message, 'tool_calls') and last_message.tool_calls


# Create the content extraction workflow
workflow = StateGraph(ContentExtractorState)

# Add nodes
workflow.add_node("extract", extraction_model)
workflow.add_node("tools", tool_node)

# Define the workflow
workflow.set_entry_point("extract")
workflow.add_conditional_edges(
    "extract",
    has_tool_calls,
    {
        True: "tools",
        False: END,
    },
)
workflow.add_edge("tools", END)

graph = workflow.compile() 