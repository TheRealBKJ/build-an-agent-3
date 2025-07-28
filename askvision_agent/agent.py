"""
AskVision Agent - AI Accessibility Assistant for webpage analysis.
Adapts the existing Section Author pattern for intelligent webpage understanding.
"""

import asyncio
import logging
import os
from typing import Annotated, Any, Sequence, cast

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from . import section_analyzer, content_extractor
from .prompts import webpage_analyzer_instructions

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3

llm = ChatNVIDIA(model="llama-3.3-nemotron-super-49b-v1.5", temperature=0)


class WebpageSection(BaseModel):
    name: str
    description: str
    content: str
    relevance_score: float


class AskVisionState(BaseModel):
    url: str
    question: str
    html_content: str
    sections: list[WebpageSection] = []
    answer: str | None = None
    messages: Annotated[Sequence[Any], add_messages] = []


async def content_extraction(state: AskVisionState, config: RunnableConfig):
    """Extract structured content from the webpage."""
    _LOGGER.info("Extracting content from webpage: %s", state.url)

    extractor_state = content_extractor.ContentExtractorState(
        url=state.url,
        html_content=state.html_content,
        messages=state.messages,
    )

    extraction = await content_extractor.graph.ainvoke(extractor_state, config)
    
    # Update state with extracted sections
    if "sections" in extraction:
        state.sections = extraction["sections"]
    
    return {"messages": extraction.get("messages", [])}


async def question_analyzer(state: AskVisionState, config: RunnableConfig):
    """Analyze the user's question and determine what sections are relevant."""
    _LOGGER.info("Analyzing question: %s", state.question)

    analyzer_state = section_analyzer.SectionAnalyzerState(
        question=state.question,
        sections=state.sections,
        messages=state.messages,
    )

    analysis = await section_analyzer.graph.ainvoke(analyzer_state, config)
    
    return {"messages": analysis.get("messages", [])}


async def answer_generator(state: AskVisionState, config: RunnableConfig):
    """Generate the final answer based on relevant sections."""
    _LOGGER.info("Generating answer for question: %s", state.question)

    # Get the last message which should contain the analysis
    if not state.messages:
        raise ValueError("No messages available for answer generation")

    system_prompt = webpage_analyzer_instructions.format(
        url=state.url,
        question=state.question
    )

    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}] + list(state.messages)
        response = await llm.ainvoke(messages, config)
        
        if response:
            state.answer = response.content
            return state
        
        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    raise RuntimeError("Failed to call model after %d attempts.", _MAX_LLM_RETRIES)


# Create the AskVision workflow graph
workflow = StateGraph(AskVisionState)

# Add nodes
workflow.add_node("extract_content", content_extraction)
workflow.add_node("analyze_question", question_analyzer)
workflow.add_node("generate_answer", answer_generator)

# Define the workflow
workflow.set_entry_point("extract_content")
workflow.add_edge("extract_content", "analyze_question")
workflow.add_edge("analyze_question", "generate_answer")
workflow.set_finish_point("generate_answer")

graph = workflow.compile() 