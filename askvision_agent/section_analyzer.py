"""Section analysis workflow for determining relevance to user questions."""

import logging
from typing import Annotated, Any, Sequence

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from .prompts import section_analysis_prompt

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3

llm = ChatNVIDIA(model="llama-3.3-nemotron-super-49b-v1.5", temperature=0)


class WebpageSection(BaseModel):
    name: str
    description: str
    content: str
    relevance_score: float


class SectionAnalyzerState(BaseModel):
    question: str
    sections: list[WebpageSection] = []
    relevant_sections: list[WebpageSection] = []
    messages: Annotated[Sequence[Any], add_messages] = []


async def analysis_model(
    state: SectionAnalyzerState,
    config: RunnableConfig,
) -> dict[str, Any]:
    """Analyze which sections are relevant to the user's question."""
    _LOGGER.info("Analyzing question relevance: %s", state.question)
    
    # Create a summary of available sections
    sections_summary = "\n".join([
        f"- {section.name}: {section.description}" 
        for section in state.sections
    ])
    
    system_prompt = section_analysis_prompt.format(
        question=state.question,
        sections_summary=sections_summary
    )

    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}] + list(state.messages)
        response = await llm.ainvoke(messages, config)

        if response:
            return {"messages": [response]}

        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    raise RuntimeError("Failed to call model after %d attempts.", _MAX_LLM_RETRIES)


# Create the section analysis workflow
workflow = StateGraph(SectionAnalyzerState)

# Add nodes
workflow.add_node("analyze", analysis_model)

# Define the workflow
workflow.set_entry_point("analyze")
workflow.set_finish_point("analyze")

graph = workflow.compile() 