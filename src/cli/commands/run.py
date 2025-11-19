"""
Run command - Execute the LangGraph workflow.
"""

from pathlib import Path
from typing import Optional

import typer
from langchain_core.messages import HumanMessage
from langsmith import uuid7
from rich.console import Console
from rich.panel import Panel

from src.core.config import validate_environment
from src.main import get_compiled_app

console = Console()


def run_workflow(
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Run in interactive mode (conversational)",
    ),
    prompt: Optional[str] = typer.Option(
        None,
        "--prompt",
        "-p",
        help="Execute a single prompt",
    ),
    file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="Execute instructions from a file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    thread_id: Optional[str] = typer.Option(
        None,
        "--thread-id",
        "-t",
        help="Custom thread ID for conversation persistence",
    ),
    recursion_limit: int = typer.Option(
        50,
        "--recursion-limit",
        "-r",
        help="Maximum recursion depth for graph execution",
        min=1,
        max=200,
    ),
):
    """
    Execute the SCM NLP workflow.

    Choose one execution mode:

    \b
    • Interactive mode (-i): Conversational interface
    • Prompt mode (-p): Single command execution
    • File mode (-f): Batch execution from file

    Examples:

    \b
        # Interactive mode
        scm-agent run --interactive

    \b
        # Single prompt
        scm-agent run --prompt "List all tags in Texas"

    \b
        # File input
        scm-agent run --file tasks.txt
    """
    # Validate that exactly one mode is selected
    modes = sum([interactive, prompt is not None, file is not None])
    if modes == 0:
        console.print(
            "[red]Error:[/red] Must specify one execution mode: --interactive, --prompt, or --file"
        )
        console.print("\nRun [cyan]scm-agent run --help[/cyan] for more information")
        raise typer.Exit(code=1)
    elif modes > 1:
        console.print("[red]Error:[/red] Only one execution mode can be used at a time")
        raise typer.Exit(code=1)

    # Validate environment
    try:
        validate_environment()
    except Exception as e:
        console.print(f"[red]Configuration Error:[/red] {e}")
        console.print(
            "\n[yellow]Tip:[/yellow] Check your .env file or environment variables"
        )
        raise typer.Exit(code=1)

    # Get compiled app
    try:
        app = get_compiled_app()
    except Exception as e:
        console.print(f"[red]Failed to initialize workflow:[/red] {e}")
        raise typer.Exit(code=1)

    # Execute based on mode
    try:
        if interactive:
            _run_interactive(app, thread_id, recursion_limit)
        elif prompt:
            _run_prompt(app, prompt, thread_id, recursion_limit)
        elif file:
            _run_file(app, file, thread_id, recursion_limit)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Interrupted by user. Goodbye![/yellow]")
        raise typer.Exit(code=0)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {type(e).__name__}: {e}")
        raise typer.Exit(code=1)


def _run_interactive(app, thread_id: Optional[str], recursion_limit: int):
    """Run in interactive mode."""
    console.print(
        Panel.fit(
            "[bold cyan]SCM NLP Assistant[/bold cyan]\n"
            "Interactive Mode - Batch Operations Enabled\n\n"
            "[dim]Type 'exit' or 'quit' to end, Ctrl+C to interrupt[/dim]",
            border_style="cyan",
        )
    )

    tid = thread_id or str(uuid7())
    console.print(f"\n[dim]Session ID:[/dim] {tid}")
    console.print(f"[dim]Recursion Limit:[/dim] {recursion_limit}\n")

    config = {
        "configurable": {"thread_id": tid},
        "recursion_limit": recursion_limit,
    }

    while True:
        try:
            user_input = console.input("[bold green]You:[/bold green] ").strip()

            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("\n[yellow]👋 Goodbye![/yellow]")
                break

            if not user_input:
                continue

            console.print()
            with console.status(
                "[bold cyan]🤖 Processing your request...", spinner="earth"
            ):
                result = app.invoke(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=config,
                )
                final_message = result["messages"][-1]

            console.print("[bold cyan]Assistant:[/bold cyan]", final_message.content)
            console.print()

        except KeyboardInterrupt:
            raise
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}\n")
            continue


def _run_prompt(app, prompt_text: str, thread_id: Optional[str], recursion_limit: int):
    """Run single prompt."""
    console.print(f"[bold cyan]Processing:[/bold cyan] {prompt_text}\n")

    config = {
        "configurable": {"thread_id": thread_id or str(uuid7())},
        "recursion_limit": recursion_limit,
    }

    with console.status("[bold cyan]🤖 Processing your request...", spinner="earth"):
        result = app.invoke(
            {"messages": [HumanMessage(content=prompt_text)]},
            config=config,
        )
        final_message = result["messages"][-1]

    console.print(f"\n[bold cyan]Assistant:[/bold cyan] {final_message.content}")


def _run_file(app, file_path: Path, thread_id: Optional[str], recursion_limit: int):
    """Run instructions from file."""
    console.print(f"[bold cyan]Processing instructions from:[/bold cyan] {file_path}\n")

    # Read file content
    try:
        content = file_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        console.print(f"[red]Failed to read file:[/red] {e}")
        raise typer.Exit(code=1)

    if not content:
        console.print("[red]Error:[/red] File is empty")
        raise typer.Exit(code=1)

    config = {
        "configurable": {"thread_id": thread_id or str(uuid7())},
        "recursion_limit": recursion_limit,
    }

    # Parse instructions
    lines = [line.strip() for line in content.split("\n") if line.strip()]

    if len(lines) == 1:
        # Single instruction
        console.print(f"[dim]Instruction:[/dim] {lines[0]}\n")
        with console.status(
            "[bold cyan]🤖 Processing your request...", spinner="earth"
        ):
            result = app.invoke(
                {"messages": [HumanMessage(content=lines[0])]},
                config=config,
            )
            final_message = result["messages"][-1]
        console.print(f"\n[bold cyan]Assistant:[/bold cyan] {final_message.content}")
    else:
        # Multiple instructions
        console.print(f"[dim]Found {len(lines)} instructions[/dim]\n")

        for i, instruction in enumerate(lines, 1):
            console.print(f"[bold cyan][{i}/{len(lines)}][/bold cyan] {instruction}")

            with console.status(
                f"[bold cyan]🤖 Processing instruction {i}/{len(lines)}...",
                spinner="earth",
            ):
                result = app.invoke(
                    {"messages": [HumanMessage(content=instruction)]},
                    config=config,
                )
                final_message = result["messages"][-1]
            console.print(f"[green]✅[/green] {final_message.content}\n")
