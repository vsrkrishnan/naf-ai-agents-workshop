"""
Core module for SCM NLP Workflow.

This module contains fundamental components:
- State management (AgentState)
- SCM client initialization
- Configuration management
"""

from src.core.client import get_scm_client
from src.core.state import AgentState

__all__ = ["get_scm_client", "AgentState"]
