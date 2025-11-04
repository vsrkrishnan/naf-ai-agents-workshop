"""
Tools command - List available tools and examples.
"""

from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from typing_extensions import Annotated

console = Console()


def list_tools(
    examples: Annotated[
        bool,
        typer.Option(
            "--examples",
            "-e",
            help="Show detailed examples for each tool",
        ),
    ] = False,
    category: Annotated[
        Optional[str],
        typer.Option(
            "--category",
            "-c",
            help="Filter by category: batch, tags, addresses, groups, jobs",
        ),
    ] = None,
):
    """
    List available SCM tools and their usage.

    Shows all tools available in the workflow with descriptions and examples.

    Examples:

    \b
        # List all tools
        scm-agent tools

    \b
        # Show detailed examples
        scm-agent tools --examples

    \b
        # Filter by category
        scm-agent tools --category batch
    """
    # Define tools
    tools_data = {
        "batch": [
            {
                "name": "tag_create_batch",
                "description": "Create multiple tags in one batch operation",
                "params": "tags: list, folder: str",
                "example": "Create 3 tags in Texas: Development (Blue), Staging (Green), Production (Red)",
            },
            {
                "name": "address_create_batch",
                "description": "Create multiple address objects in batch",
                "params": "addresses: list, folder: str",
                "example": "Create 5 addresses with IPs 10.0.1.1/32 through 10.0.1.5/32 in Texas",
            },
            {
                "name": "address_group_create_batch",
                "description": "Create multiple address groups in batch",
                "params": "groups: list, folder: str",
                "example": "Create address groups for web, app, and db tiers in Texas",
            },
        ],
        "tags": [
            {
                "name": "tag_create",
                "description": "Create a single tag",
                "params": "name: str, color: str, folder: str, comments: str",
                "example": "Create tag named Production with Red color in Texas",
            },
            {
                "name": "tag_read",
                "description": "Get details of a specific tag",
                "params": "name: str, folder: str",
                "example": "Show me details of tag Production in Texas",
            },
            {
                "name": "tag_list",
                "description": "List all tags in a folder",
                "params": "folder: str, limit: int",
                "example": "List all tags in Texas",
            },
        ],
        "addresses": [
            {
                "name": "address_create",
                "description": "Create a single address object",
                "params": "name: str, ip_netmask: str, folder: str, description: str, tags: str",
                "example": "Create address web_server_01 with IP 10.0.1.10/32 in Texas",
            },
            {
                "name": "address_read",
                "description": "Get details of a specific address",
                "params": "name: str, folder: str",
                "example": "Show me details of address web_server_01 in Texas",
            },
            {
                "name": "address_update",
                "description": "Update an existing address (tags, description)",
                "params": "name: str, folder: str, new_description: str, add_tags: str, remove_tags: str",
                "example": "Add Production tag to web_server_01 in Texas",
            },
            {
                "name": "address_list",
                "description": "List all addresses in a folder",
                "params": "folder: str, limit: int",
                "example": "List all addresses in Texas",
            },
        ],
        "jobs": [
            {
                "name": "commit_changes",
                "description": "Commit configuration changes to SCM",
                "params": "folders: str, description: str, admin: str, sync: bool, timeout: int",
                "example": 'Commit changes to Texas with description "Added web servers"',
            },
            {
                "name": "check_job_status",
                "description": "Check the status of an SCM job",
                "params": "job_id: str",
                "example": "Check status of job abc-123-def-456",
            },
        ],
    }

    # Filter by category if specified
    if category:
        if category.lower() not in tools_data:
            console.print(f"[red]Error:[/red] Unknown category '{category}'")
            console.print(
                f"\n[yellow]Available categories:[/yellow] {', '.join(tools_data.keys())}"
            )
            raise typer.Exit(code=1)
        tools_data = {category.lower(): tools_data[category.lower()]}

    # Display tools
    console.print(
        Panel.fit(
            "[bold cyan]SCM NLP Workflow - Available Tools[/bold cyan]",
            border_style="cyan",
        )
    )

    for cat, tools in tools_data.items():
        console.print(f"\n[bold yellow]{cat.upper()} OPERATIONS[/bold yellow]")

        if examples:
            # Detailed view with examples
            for tool in tools:
                console.print(f"\n[bold cyan]• {tool['name']}[/bold cyan]")
                console.print(f"  [dim]{tool['description']}[/dim]")
                console.print(f"  [dim]Parameters:[/dim] {tool['params']}")
                console.print(f"  [green]Example:[/green] \"{tool['example']}\"")
        else:
            # Table view
            table = Table(
                show_header=True, header_style="bold magenta", border_style="dim"
            )
            table.add_column("Tool", style="cyan", no_wrap=True)
            table.add_column("Description")

            for tool in tools:
                table.add_row(tool["name"], tool["description"])

            console.print(table)

    # Usage tips
    console.print("\n[bold]Usage Tips:[/bold]")
    tips = """
• Use batch operations for 3+ objects to avoid recursion limits
• Always specify folder name (e.g., "Texas", "California")
• Tag colors: Red, Blue, Green, Yellow, Orange, etc.
• IP addresses must use CIDR notation (e.g., 10.0.1.1/32)
• Commit changes after creating/updating objects

Run [cyan]scm-agent tools --examples[/cyan] to see detailed examples
Run [cyan]scm-agent run --help[/cyan] to see how to execute workflows
    """
    console.print(Markdown(tips))

    # Quick examples
    if not examples:
        console.print("\n[bold]Quick Examples:[/bold]")
        console.print('  scm-agent run -p "List all tags in Texas"')
        console.print('  scm-agent run -p "Create 5 addresses in Texas"')
        console.print('  scm-agent run -p "Commit changes to Texas"')
        console.print()
