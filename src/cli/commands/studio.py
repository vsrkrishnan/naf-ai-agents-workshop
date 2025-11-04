"""
Studio command - Launch LangGraph Studio with environment loaded.
"""

import os
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

console = Console()


def launch_studio(
    port: int = typer.Option(
        8123,
        "--port",
        "-p",
        help="Port to run LangGraph Studio on",
        min=1024,
        max=65535,
    ),
    check: bool = typer.Option(
        False,
        "--check",
        "-c",
        help="Check dependencies and configuration without launching",
    ),
):
    """
    Launch LangGraph Studio with environment loaded.

    This command:
    • Validates environment configuration (.env file)
    • Checks LangGraph Studio dependencies
    • Launches Studio with proper environment variables loaded
    • Opens browser to http://localhost:PORT

    Examples:

    \b
        # Launch Studio (default port 8123)
        scm-agent studio

    \b
        # Launch on custom port
        scm-agent studio --port 8000

    \b
        # Check dependencies without launching
        scm-agent studio --check
    """
    # Get project paths
    project_root = Path(__file__).parent.parent.parent.parent
    workflows_dir = project_root / "workflows"
    env_file = project_root / ".env"

    if check:
        _check_dependencies(workflows_dir, env_file)
        return

    # Validate environment file
    if not env_file.exists():
        console.print(f"[red]Error:[/red] .env file not found at {env_file}")
        console.print(
            "\n[yellow]Tip:[/yellow] Create a .env file with required credentials"
        )
        raise typer.Exit(code=1)

    # Check langgraph.json
    langgraph_json = workflows_dir / "langgraph.json"
    if not langgraph_json.exists():
        console.print(f"[red]Error:[/red] langgraph.json not found at {langgraph_json}")
        raise typer.Exit(code=1)

    # Check langgraph CLI
    try:
        subprocess.run(
            ["langgraph", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[red]Error:[/red] langgraph CLI not found")
        console.print(
            "\n[yellow]Install with:[/yellow] uv pip install -U 'langgraph-cli[inmem]'"
        )
        raise typer.Exit(code=1)

    # Launch Studio
    console.print(
        Panel.fit(
            "[bold cyan]Launching LangGraph Studio[/bold cyan]\n\n"
            f"[dim]Workflows:[/dim] {workflows_dir}\n"
            f"[dim]Environment:[/dim] {env_file}\n"
            f"[dim]Port:[/dim] {port}\n\n"
            f"[green]Studio will open at:[/green] http://localhost:{port}",
            border_style="cyan",
        )
    )

    console.print("\n[dim]Press Ctrl+C to stop Studio[/dim]\n")

    try:
        # Change to workflows directory and run Studio
        env = os.environ.copy()
        env["PORT"] = str(port)

        subprocess.run(
            ["langgraph", "dev", "--port", str(port)],
            cwd=workflows_dir,
            env=env,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        console.print(f"\n[red]Studio exited with error:[/red] {e}")
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Studio stopped[/yellow]")
        raise typer.Exit(code=0)


def _check_dependencies(workflows_dir: Path, env_file: Path):
    """Check Studio dependencies and configuration."""
    console.print(
        Panel.fit(
            "[bold cyan]LangGraph Studio - Dependency Check[/bold cyan]",
            border_style="cyan",
        )
    )

    all_good = True

    # Check langgraph CLI
    console.print("\n[bold]1. LangGraph CLI[/bold]")
    try:
        result = subprocess.run(
            ["langgraph", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        version = result.stdout.strip()
        console.print(f"   [green]✅ Installed:[/green] {version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("   [red]❌ Not installed[/red]")
        console.print(
            "   [yellow]Install:[/yellow] uv pip install -U 'langgraph-cli[inmem]'"
        )
        all_good = False

    # Check langgraph-api
    console.print("\n[bold]2. LangGraph API[/bold]")
    try:
        import langgraph_api  # type: ignore

        console.print(f"   [green]✅ Installed:[/green] {langgraph_api.__version__}")
    except ImportError:
        console.print("   [red]❌ Not installed[/red]")
        console.print(
            "   [yellow]Install:[/yellow] uv pip install -U 'langgraph-cli[inmem]'"
        )
        all_good = False

    # Check langgraph.json
    console.print("\n[bold]3. Configuration Files[/bold]")
    langgraph_json = workflows_dir / "langgraph.json"
    if langgraph_json.exists():
        console.print(f"   [green]✅ langgraph.json:[/green] {langgraph_json}")
    else:
        console.print("   [red]❌ langgraph.json:[/red] Not found")
        all_good = False

    # Check .env
    if env_file.exists():
        console.print(f"   [green]✅ .env file:[/green] {env_file}")
    else:
        console.print("   [red]❌ .env file:[/red] Not found")
        all_good = False

    # Check environment variables
    console.print("\n[bold]4. Environment Variables[/bold]")
    required_vars = [
        "SCM_CLIENT_ID",
        "SCM_CLIENT_SECRET",
        "SCM_TSG_ID",
        "ANTHROPIC_API_KEY",
    ]

    # Load .env if it exists
    if env_file.exists():
        from dotenv import load_dotenv

        load_dotenv(env_file)

    for var in required_vars:
        if os.getenv(var):
            console.print(f"   [green]✅ {var}:[/green] Set")
        else:
            console.print(f"   [yellow]⚠️  {var}:[/yellow] Not set")

    # Summary
    console.print("\n" + "=" * 50)
    if all_good:
        console.print("\n[bold green]✅ All dependencies satisfied![/bold green]")
        console.print("\nRun [cyan]scm-agent studio[/cyan] to launch LangGraph Studio")
    else:
        console.print("\n[bold yellow]⚠️  Some dependencies missing[/bold yellow]")
        console.print("\nInstall missing dependencies and try again")

    console.print()
