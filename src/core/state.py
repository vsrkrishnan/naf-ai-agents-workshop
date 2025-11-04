"""
State management for SCM NLP Workflow.

Defines the graph state used throughout the LangGraph workflow.
"""

from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    State for ReAct agent with automatic message management.

    The state contains a messages list that is automatically managed by LangGraph's
    add_messages reducer. This allows the graph to accumulate conversation history
    across multiple agent-tool cycles.

    Attributes:
        messages: Sequence of messages (user messages, AI responses, tool results)
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
