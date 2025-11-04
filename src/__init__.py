"""
SCM NLP Workflow Package

A natural language interface for Strata Cloud Manager automation using LangGraph.

Features:
- Natural language SCM operations
- Batch operations with Pydantic validation
- Enhanced commit operations with job monitoring
- Interactive CLI and file-based execution
- LangGraph Studio integration
"""

__version__ = "0.1.0"
__author__ = "Calvin Remsburg"

from src.main import get_compiled_app, main

__all__ = ["get_compiled_app", "main"]
