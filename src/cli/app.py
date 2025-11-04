"""
Main Typer application for SCM NLP Workflow CLI.
"""

import typer
from rich.console import Console

app = typer.Typer(
    name="scm-nlp",
    help="Natural Language interface for Strata Cloud Manager automation using LangGraph",
    add_completion=False,
)

console = Console()

# Import subcommands
from src.cli.commands.run import run_workflow  # noqa: E402
from src.cli.commands.studio import launch_studio  # noqa: E402
from src.cli.commands.tools import list_tools  # noqa: E402

# Register subcommands
app.command(name="run")(run_workflow)
app.command(name="studio")(launch_studio)
app.command(name="tools")(list_tools)


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from src import __version__

        console.print(
            f"[bold cyan]SCM NLP Workflow[/bold cyan] version [green]{__version__}[/green]"
        )
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    )
):
    """
    SCM Agent - Natural Language interface for Strata Cloud Manager.

    Run 'scm-agent COMMAND --help' for more information on a command.
    """
    pass


def main():
    """Entry point for the CLI."""
    app()
