"""
CLI module for SCM NLP Workflow.

Provides Typer-based command-line interface with subcommands:
- run: Execute the workflow (interactive, prompt, or file)
- studio: Launch LangGraph Studio
- tools: List available tools and examples
"""


def get_app():
    """Get the Typer app instance."""
    from src.cli.app import app

    return app


# For entry point
app = get_app()
