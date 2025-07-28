# code/docgen_agent/ask.py

import json
import logging
import os
from typing import Annotated, Any, Sequence

from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from . import tools
from .prompts import askvision_prompt

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3

# Initialize LLM (always)
llm = ChatNVIDIA(
    model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
    temperature=0,
    base_url="https://integrate.api.nvidia.com/v1",
    headers={"x-api-key": os.environ["NVIDIA_API_KEY"]}
)


# ---------------------------
# STATE
# ---------------------------
class ResearcherState(BaseModel):
    topic: str
    document: str = ""
    number_of_queries: int = Field(default=0)
    messages: Annotated[Sequence[Any], add_messages] = []


# ---------------------------
# TOOL NODE
# ---------------------------
async def tool_node(state: ResearcherState):
    _LOGGER.info("Executing tool calls.")
    outputs = []
    for tool_call in state.messages[-1].tool_calls:
        _LOGGER.info("Executing tool call: %s", tool_call["name"])
        tool = getattr(tools, tool_call["name"])
        tool_result = await tool.ainvoke(tool_call["args"])
        outputs.append({
            "role": "tool",
            "content": json.dumps(tool_result),
            "name": tool_call["name"],
            "tool_call_id": tool_call["id"],
        })
    return {"messages": outputs}


# ---------------------------
# MODEL NODE
# ---------------------------
async def call_model(state: ResearcherState, config: RunnableConfig) -> dict[str, Any]:
    _LOGGER.info("Calling model.")
    system_prompt = askvision_prompt.format(
        document=state.document,
        question=state.topic
    )

    # Only bind tools if you allow queries
    model = llm.bind_tools([tools.search_tavily]) if state.number_of_queries > 0 else llm

    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}] + list(state.messages)
        response = await model.ainvoke(messages, config)
        if response:
            return {"messages": [response]}
        _LOGGER.debug("Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES)

    raise RuntimeError("Failed to call model after retries")


# ---------------------------
# TRANSITION CHECK
# ---------------------------
def has_tool_calls(state: ResearcherState) -> bool:
    messages = state.messages
    return bool(messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls)


# ---------------------------
# BUILD THE GRAPH
# ---------------------------
workflow = StateGraph(ResearcherState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", has_tool_calls, {True: "tools", False: END})
workflow.add_edge("tools", "agent")

graph = workflow.compile()
