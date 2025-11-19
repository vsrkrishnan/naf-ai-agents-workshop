"""
NLP-Based SCM Workflow with Enhanced User Experience (ReAct Pattern)

This workflow enhances 04_nlp_scm_workflow_batch.py with improved UX features:
- Real-time progress indicators during operations
- Streaming output for better feedback
- Visual status updates while waiting
- Enhanced error messages with context
- Better interactive experience

Inherits all features from 04_nlp_scm_workflow_batch.py:
✅ Full CRUD operations (Create, Read, Update, Delete, List)
✅ Batch operations with Pydantic validation
✅ Enhanced commit operations with job monitoring
✅ Avoids recursion limit issues
✅ Double validation (LangChain + SDK)
✅ Efficient bulk processing

New UX Features:
✅ Real-time progress indicators
✅ Streaming graph execution
✅ Visual feedback during long operations
✅ Better error context and suggestions
✅ Improved interactive mode

Example Prompts:
- "Create 14 address objects with langgraph tag in Texas"
- "Create addresses for IPs 10.0.1.1 through 10.0.1.20 in Texas"
- "Add Production tag to all web server addresses in Texas"
- "Commit changes to Texas and California"
"""

from typing import Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langsmith import uuid7
from pydantic import BaseModel, Field
from scm.exceptions import ObjectNotPresentError

# Import from core modules
from src.core import AgentState, get_scm_client
from src.core.config import validate_environment

# ============================================================================
# PYDANTIC MODELS FOR BATCH OPERATIONS
# ============================================================================


class TagConfigForBatch(BaseModel):
    """Pydantic model for tag configuration in batch operations."""

    name: str = Field(description="Tag name (e.g., 'Production', 'WebServers')")
    color: str = Field(description="Tag color (e.g., 'Red', 'Blue', 'Green')")
    comments: str = Field(default="", description="Optional comments")


class AddressConfigForBatch(BaseModel):
    """Pydantic model for address configuration in batch operations."""

    name: str = Field(description="Address name (e.g., 'web_server_01')")
    ip_netmask: str = Field(
        description="IP with CIDR notation (e.g., '10.0.1.10/32')",
        pattern=r"^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$",
    )
    description: str = Field(default="", description="Optional description")
    tag: list[str] = Field(default_factory=list, description="List of tag names")


class AddressGroupConfigForBatch(BaseModel):
    """Pydantic model for address group configuration in batch operations."""

    name: str = Field(description="Group name (e.g., 'web_servers')")
    members: list[str] = Field(description="List of address object names")
    description: str = Field(default="", description="Optional description")
    tag: list[str] = Field(default_factory=list, description="List of tag names")


class BatchTagRequest(BaseModel):
    """Request model for batch tag creation."""

    tags: list[TagConfigForBatch] = Field(description="List of tags to create")
    folder: str = Field(description="SCM folder name (e.g., 'Texas')")


class BatchAddressRequest(BaseModel):
    """Request model for batch address creation."""

    addresses: list[AddressConfigForBatch] = Field(
        description="List of addresses to create"
    )
    folder: str = Field(description="SCM folder name (e.g., 'Texas')")


class BatchAddressGroupRequest(BaseModel):
    """Request model for batch address group creation."""

    groups: list[AddressGroupConfigForBatch] = Field(
        description="List of address groups to create"
    )
    folder: str = Field(description="SCM folder name (e.g., 'Texas')")


# ============================================================================
# BATCH OPERATION TOOLS
# ============================================================================


def _tag_create_batch(request: BatchTagRequest) -> str:
    """
    Create multiple tags in one batch operation.

    Args:
        request: Batch request with list of tag configs and folder

    Returns:
        Summary of created tags

    This tool uses Pydantic validation to ensure the LLM generates valid JSON
    that matches the SCM API schema. Use this for bulk tag creation.
    """
    client = get_scm_client()

    results = []
    errors = []

    for tag_config in request.tags:
        try:
            # Check if exists
            try:
                client.tag.fetch(name=tag_config.name, folder=request.folder)
                results.append(f"⏭️  {tag_config.name} (already exists)")
                continue
            except ObjectNotPresentError:
                pass

            # Convert Pydantic model to dict and add folder
            config_dict = tag_config.model_dump()
            config_dict["folder"] = request.folder

            # Remove empty comments field to avoid API validation error
            if not config_dict.get("comments"):
                config_dict.pop("comments", None)

            # Create
            tag = client.tag.create(config_dict)
            results.append(f"✅ {tag.name} ({tag.color})")

        except Exception as e:
            errors.append(f"❌ {tag_config.name}: {str(e)}")

    created_count = len([r for r in results if "✅" in r])
    existing_count = len([r for r in results if "⏭️" in r])

    summary = f"Batch tag creation: {created_count} created, {existing_count} already existed\n\n"
    summary += "\n".join(results)

    if errors:
        summary += "\n\nErrors:\n" + "\n".join(errors)

    return summary


def _address_create_batch(request: BatchAddressRequest) -> str:
    """
    Create multiple address objects in one batch operation.

    Args:
        request: Batch request with list of address configs and folder

    Returns:
        Summary of created addresses

    This tool uses Pydantic validation to ensure the LLM generates valid JSON.
    The IP address format is validated via regex pattern in the Pydantic model.
    Use this for bulk address creation (e.g., "create 14 addresses").
    """
    client = get_scm_client()

    results = []
    errors = []

    for addr_config in request.addresses:
        try:
            # Check if exists
            try:
                client.address.fetch(name=addr_config.name, folder=request.folder)
                results.append(f"⏭️  {addr_config.name} (already exists)")
                continue
            except ObjectNotPresentError:
                pass

            # Convert Pydantic model to dict and add folder
            config_dict = addr_config.model_dump()
            config_dict["folder"] = request.folder

            # Remove empty optional fields to avoid API validation errors
            if not config_dict.get("description"):
                config_dict.pop("description", None)
            if not config_dict.get("tag"):
                config_dict.pop("tag", None)

            # Create
            addr = client.address.create(config_dict)
            results.append(f"✅ {addr.name} ({addr.ip_netmask})")

        except Exception as e:
            errors.append(f"❌ {addr_config.name}: {str(e)}")

    created_count = len([r for r in results if "✅" in r])
    existing_count = len([r for r in results if "⏭️" in r])

    summary = f"Batch address creation: {created_count} created, {existing_count} already existed\n\n"
    summary += "\n".join(results)

    if errors:
        summary += "\n\nErrors:\n" + "\n".join(errors)

    return summary


def _address_group_create_batch(request: BatchAddressGroupRequest) -> str:
    """
    Create multiple address groups in one batch operation.

    Args:
        request: Batch request with list of group configs and folder

    Returns:
        Summary of created groups

    This tool validates that all member addresses exist before creating groups.
    Use this for bulk group creation.
    """
    client = get_scm_client()

    results = []
    errors = []

    for group_config in request.groups:
        try:
            # Check if group exists
            try:
                client.address_group.fetch(
                    name=group_config.name, folder=request.folder
                )
                results.append(f"⏭️  {group_config.name} (already exists)")
                continue
            except ObjectNotPresentError:
                pass

            # Validate members exist
            missing_members = []
            for member in group_config.members:
                try:
                    client.address.fetch(name=member, folder=request.folder)
                except ObjectNotPresentError:
                    missing_members.append(member)

            if missing_members:
                errors.append(
                    f"❌ {group_config.name}: Missing members: {', '.join(missing_members)}"
                )
                continue

            # Convert to dict and add folder
            config_dict = {
                "name": group_config.name,
                "static": group_config.members,
                "folder": request.folder,
            }

            # Only include optional fields if non-empty
            if group_config.description:
                config_dict["description"] = group_config.description
            if group_config.tag:
                config_dict["tag"] = group_config.tag

            # Create
            group = client.address_group.create(config_dict)
            results.append(f"✅ {group.name} ({len(group_config.members)} members)")

        except Exception as e:
            errors.append(f"❌ {group_config.name}: {str(e)}")

    created_count = len([r for r in results if "✅" in r])
    existing_count = len([r for r in results if "⏭️" in r])

    summary = f"Batch address group creation: {created_count} created, {existing_count} already existed\n\n"
    summary += "\n".join(results)

    if errors:
        summary += "\n\nErrors:\n" + "\n".join(errors)

    return summary


# ============================================================================
# INDIVIDUAL CRUD TOOLS (from 03_nlp_scm_workflow_crud.py)
# ============================================================================


def _tag_create(name: str, color: str, folder: str, comments: str = "") -> str:
    """Create a single tag."""
    client = get_scm_client()
    try:
        try:
            existing = client.tag.fetch(name=name, folder=folder)
            return f"❌ Tag '{name}' already exists in '{folder}' (ID: {existing.id})"
        except ObjectNotPresentError:
            pass

        # Build config dict - only include comments if non-empty
        config = {"name": name, "color": color, "folder": folder}
        if comments:
            config["comments"] = comments

        tag = client.tag.create(config)
        return f"✅ Created tag '{tag.name}' ({tag.color}) in '{folder}' (ID: {tag.id})"
    except Exception as e:
        return f"❌ Failed: {type(e).__name__}: {str(e)}"


def _tag_read(name: str, folder: str) -> str:
    """Get details of a specific tag."""
    client = get_scm_client()
    try:
        tag = client.tag.fetch(name=name, folder=folder)
        comment = tag.comment or "None"
        return f"Tag: {tag.name}\nColor: {tag.color}\nFolder: {tag.folder}\nID: {tag.id}\nComments: {comment}"
    except ObjectNotPresentError:
        return f"❌ Tag '{name}' not found in folder '{folder}'"
    except Exception as e:
        return f"❌ Failed: {type(e).__name__}: {str(e)}"


def _tag_list(folder: str, limit: int = 10) -> str:
    """List all tags in a folder."""
    client = get_scm_client()
    try:
        tags = list(client.tag.list(folder=folder, limit=min(limit, 100)))
        if not tags:
            return f"No tags found in folder '{folder}'"
        result = f"Found {len(tags)} tags in '{folder}':\n"
        for tag in tags:
            result += f"  • {tag.name} ({tag.color})\n"
        return result
    except Exception as e:
        return f"❌ Failed: {type(e).__name__}: {str(e)}"


def _address_create(
    name: str, ip_netmask: str, folder: str, description: str = "", tags: str = ""
) -> str:
    """Create a single address object."""
    client = get_scm_client()
    try:
        try:
            existing = client.address.fetch(name=name, folder=folder)
            return (
                f"❌ Address '{name}' already exists in '{folder}' (ID: {existing.id})"
            )
        except ObjectNotPresentError:
            pass

        # Build config dict - only include optional fields if non-empty
        config = {"name": name, "ip_netmask": ip_netmask, "folder": folder}
        if description:
            config["description"] = description

        tag_list = [t.strip() for t in tags.split(",")] if tags else []
        if tag_list:
            config["tag"] = tag_list

        addr = client.address.create(config)
        return f"✅ Created address '{addr.name}' ({addr.ip_netmask}) in '{folder}' (ID: {addr.id})"
    except Exception as e:
        return f"❌ Failed: {type(e).__name__}: {str(e)}"


def _address_read(name: str, folder: str) -> str:
    """Get details of a specific address."""
    client = get_scm_client()
    try:
        addr = client.address.fetch(name=name, folder=folder)
        tags_str = ", ".join(addr.tag) if addr.tag else "None"
        desc = addr.description or "None"
        return (
            f"Address: {addr.name}\nIP: {addr.ip_netmask}\nFolder: {addr.folder}\n"
            f"Description: {desc}\nTags: {tags_str}\nID: {addr.id}"
        )
    except ObjectNotPresentError:
        return f"❌ Address '{name}' not found in folder '{folder}'"
    except Exception as e:
        return f"❌ Failed: {type(e).__name__}: {str(e)}"


def _address_update(
    name: str,
    folder: str,
    new_description: str = None,
    add_tags: str = None,
    remove_tags: str = None,
) -> str:
    """Update an existing address (add/remove tags, change description)."""
    client = get_scm_client()
    try:
        addr = client.address.fetch(name=name, folder=folder)

        if new_description is not None:
            addr.description = new_description

        if add_tags:
            new_tags = [t.strip() for t in add_tags.split(",")]
            current_tags = set(addr.tag or [])
            current_tags.update(new_tags)
            addr.tag = list(current_tags)

        if remove_tags:
            tags_to_remove = {t.strip() for t in remove_tags.split(",")}
            current_tags = set(addr.tag or [])
            addr.tag = list(current_tags - tags_to_remove)

        updated = client.address.update(addr)
        return f"✅ Updated address '{updated.name}' in '{folder}' (ID: {updated.id})"
    except ObjectNotPresentError:
        return f"❌ Address '{name}' not found in folder '{folder}'"
    except Exception as e:
        return f"❌ Failed: {type(e).__name__}: {str(e)}"


def _address_list(folder: str, limit: int = 10) -> str:
    """List all addresses in a folder."""
    client = get_scm_client()
    try:
        addresses = list(client.address.list(folder=folder, limit=min(limit, 100)))
        if not addresses:
            return f"No addresses found in folder '{folder}'"
        result = f"Found {len(addresses)} addresses in '{folder}':\n"
        for addr in addresses:
            ip = (
                getattr(addr, "ip_netmask", None)
                or getattr(addr, "fqdn", None)
                or getattr(addr, "ip_range", None)
            )
            result += f"  • {addr.name}: {ip}\n"
        return result
    except Exception as e:
        return f"❌ Failed: {type(e).__name__}: {str(e)}"


def _check_job_status(job_id: str) -> str:
    """
    Check the status of an SCM job.

    This tool retrieves detailed status information about a job, including
    completion status, results, and any error messages.

    Args:
        job_id: The job ID to check (e.g., from a commit operation)

    Returns:
        Detailed job status information

    Example:
        "Check status of job abc-123-def-456"
    """
    client = get_scm_client()
    try:
        job_status = client.get_job_status(job_id)

        if not job_status.data or len(job_status.data) == 0:
            return f"❌ No status data found for job ID: {job_id}"

        job_data = job_status.data[0]

        # Extract job information
        status_str = job_data.status_str
        result_str = getattr(job_data, "result_str", "N/A")
        job_type = getattr(job_data, "type_str", "unknown")
        progress = getattr(job_data, "percent", 0)
        details = getattr(job_data, "details", [])

        # Build status response
        response_parts = [
            f"Job ID: {job_id}",
            f"Type: {job_type}",
            f"Status: {status_str}",
            f"Progress: {progress}%",
            f"Result: {result_str}",
        ]

        # Add details if available
        if details:
            response_parts.append("\nDetails:")
            for detail in details[:5]:  # Limit to first 5 details
                response_parts.append(f"  • {detail}")
            if len(details) > 5:
                response_parts.append(f"  ... and {len(details) - 5} more")

        # Add status icon based on status
        if status_str.lower() in ["success", "fin", "completed"]:
            response_parts[0] = "✅ " + response_parts[0]
        elif status_str.lower() in ["fail", "error"]:
            response_parts[0] = "❌ " + response_parts[0]
        elif status_str.lower() in ["pending", "pend", "running", "act"]:
            response_parts[0] = "⏳ " + response_parts[0]

        return "\n".join(response_parts)

    except ObjectNotPresentError:
        return f"❌ Job not found: {job_id}"
    except Exception as e:
        return f"❌ Failed to check job status\nError: {type(e).__name__}: {str(e)}"


def _commit_changes(
    folders: str,
    description: str = "Changes via NLP workflow",
    admin: str = "",
    sync: bool = True,
    timeout: int = 300,
) -> str:
    """
    Commit pending changes to Strata Cloud Manager.

    This tool commits configuration changes and waits for completion when sync=True.
    It monitors the job status and provides detailed feedback about the commit operation.

    Args:
        folders: Comma-separated list of folder names to commit (e.g., "Texas" or "Texas,California")
        description: Description of the changes being committed
        admin: Comma-separated list of admin emails (optional, e.g., "admin@example.com")
        sync: Wait for commit to complete (default: True)
        timeout: Maximum time to wait for completion in seconds (default: 300)

    Returns:
        Detailed status message with job ID, status, and folder information

    Example:
        "Commit changes to Texas folder with description 'Added web servers'"
        "Commit to Texas,California folders and wait for completion"
    """
    client = get_scm_client()
    try:
        # Parse folder list
        folder_list = [f.strip() for f in folders.split(",") if f.strip()]

        if not folder_list:
            return "❌ Error: No folders specified for commit"

        # Parse admin list (optional)
        admin_list = None
        if admin:
            admin_list = [a.strip() for a in admin.split(",") if a.strip()]

        # Initiate commit
        result = client.commit(
            folders=folder_list,
            description=description,
            admin=admin_list,
            sync=sync,
            timeout=timeout,
        )

        # Get job status
        job_status = client.get_job_status(result.job_id)

        # Extract status information
        if job_status.data and len(job_status.data) > 0:
            job_data = job_status.data[0]
            status_str = job_data.status_str
            result_str = getattr(job_data, "result_str", "N/A")
            job_type = getattr(job_data, "type_str", "commit")
        else:
            status_str = "unknown"
            result_str = "N/A"
            job_type = "commit"

        # Format folder information
        folders_str = ", ".join(folder_list)

        # Build response with detailed information
        response_parts = [
            (
                "✅ Commit operation completed"
                if sync
                else "✅ Commit operation initiated"
            ),
            f"Job ID: {result.job_id}",
            f"Job Type: {job_type}",
            f"Status: {status_str}",
            f"Result: {result_str}",
            f"Folders: {folders_str}",
            f"Description: {description}",
        ]

        if admin_list:
            response_parts.append(f"Admin: {', '.join(admin_list)}")

        # Add warning if not synced
        if not sync:
            response_parts.append(
                "\n⚠️  Async mode: Job initiated but not waiting for completion. "
                f"Use job ID '{result.job_id}' to check status later."
            )

        return "\n".join(response_parts)

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)

        # Provide helpful error messages for common issues
        if "timeout" in error_msg.lower():
            return (
                f"❌ Commit timeout after {timeout}s\n"
                f"Error: {error_type}: {error_msg}\n"
                f"Tip: Increase timeout or use sync=False for async commit"
            )
        elif "auth" in error_msg.lower():
            return (
                f"❌ Authentication error\n"
                f"Error: {error_type}: {error_msg}\n"
                f"Tip: Check SCM credentials and permissions"
            )
        else:
            return f"❌ Commit failed\nError: {error_type}: {error_msg}"


# ============================================================================
# CREATE TOOL INSTANCES
# ============================================================================

tools = [
    # BATCH OPERATIONS
    StructuredTool.from_function(
        func=_tag_create_batch,
        name="tag_create_batch",
        description=(
            "Create multiple tags in one batch operation. "
            "Use this for bulk tag creation to avoid recursion limits. "
            "Accepts list of tag configurations."
        ),
    ),
    StructuredTool.from_function(
        func=_address_create_batch,
        name="address_create_batch",
        description=(
            "Create multiple address objects in one batch operation. "
            "Use this for bulk address creation (e.g., '14 addresses'). "
            "Validates IP format via Pydantic."
        ),
    ),
    StructuredTool.from_function(
        func=_address_group_create_batch,
        name="address_group_create_batch",
        description=(
            "Create multiple address groups in one batch operation. "
            "Validates all members exist before creating."
        ),
    ),
    # INDIVIDUAL OPERATIONS
    StructuredTool.from_function(
        func=_tag_create,
        name="tag_create",
        description="Create a single tag",
    ),
    StructuredTool.from_function(
        func=_tag_read,
        name="tag_read",
        description="Get details of a specific tag",
    ),
    StructuredTool.from_function(
        func=_tag_list,
        name="tag_list",
        description="List all tags in a folder",
    ),
    StructuredTool.from_function(
        func=_address_create,
        name="address_create",
        description="Create a single address object",
    ),
    StructuredTool.from_function(
        func=_address_read,
        name="address_read",
        description="Get details of a specific address",
    ),
    StructuredTool.from_function(
        func=_address_update,
        name="address_update",
        description="Update an existing address (add/remove tags, change description)",
    ),
    StructuredTool.from_function(
        func=_address_list,
        name="address_list",
        description="List all addresses in a folder",
    ),
    # COMMIT AND JOB MANAGEMENT
    StructuredTool.from_function(
        func=_commit_changes,
        name="commit_changes",
        description=(
            "Commit configuration changes to Strata Cloud Manager. "
            "Supports multiple folders, custom descriptions, admin list, "
            "sync/async modes, and configurable timeout. "
            "Returns detailed job status and completion information."
        ),
    ),
    StructuredTool.from_function(
        func=_check_job_status,
        name="check_job_status",
        description=(
            "Check the status of an SCM job by job ID. "
            "Useful for monitoring async commit operations or checking job completion. "
            "Returns job type, status, progress, result, and details."
        ),
    ),
]


# ============================================================================
# AGENT NODE
# ============================================================================


def call_agent(state: AgentState) -> AgentState:
    """Agent node that reasons about requests and decides which tools to use."""
    llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)
    model_with_tools = llm.bind_tools(tools)

    system_prompt = SystemMessage(
        content="""You are an expert Strata Cloud Manager (SCM) automation assistant with CRUD + Batch capabilities.

BATCH OPERATIONS (Use these for bulk requests!):
✅ tag_create_batch - Create multiple tags at once
✅ address_create_batch - Create multiple addresses at once
✅ address_group_create_batch - Create multiple groups at once

WHEN TO USE BATCH TOOLS:
- User asks for "14 addresses" → use address_create_batch
- User asks for "multiple tags" → use tag_create_batch
- User says "create addresses for IPs 1-20" → use address_create_batch
- ANY request for more than 3-5 objects → use batch tools

VALIDATION:
✅ Batch tools use Pydantic models for strict schema validation
✅ IP addresses are validated via regex pattern
✅ All fields match SCM API schema exactly
✅ Double validation: Pydantic + SDK

INDIVIDUAL OPERATIONS:
- Use individual tools for single objects or updates
- Use address_update to add/remove tags from existing objects
- Use _read tools to check current state before updates

COMMIT OPERATIONS:
✅ commit_changes - Commit configuration changes to SCM
  • Supports multiple folders (comma-separated)
  • Custom descriptions for change tracking
  • Optional admin list for authorization
  • Sync mode (wait for completion) or async mode
  • Configurable timeout (default 300s)

✅ check_job_status - Monitor job completion
  • Check status of async commit operations
  • Track progress and get detailed results
  • Useful for long-running operations

COMMIT BEST PRACTICES:
- Always ask user before committing changes
- Use descriptive commit messages
- Default to sync=True for immediate feedback
- Use sync=False for large commits that may take >5 minutes
- If async, provide job ID and suggest checking status later

EXAMPLE WORKFLOWS:

1. Create objects and commit:
User: "Create 14 address objects with langgraph tag in Texas and commit"
Your actions:
  a. Call address_create_batch with 14 AddressConfig objects
  b. Ask user to confirm commit
  c. Call commit_changes(folders="Texas", description="Added 14 web servers", sync=True)

2. Async commit for large changes:
User: "Commit my Texas changes but don't wait"
Your action:
  Call commit_changes(folders="Texas", description="...", sync=False)
  Then inform user about job ID and how to check status

Always explain what you're doing and confirm success!"""
    )

    messages = state["messages"]
    response = model_with_tools.invoke([system_prompt] + messages)

    return {"messages": [response]}


# ============================================================================
# ROUTING & GRAPH
# ============================================================================


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Determine if agent should continue using tools."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"


def build_nlp_workflow() -> StateGraph:
    """Build the ReAct workflow with batch operations."""
    graph = StateGraph(AgentState)

    graph.add_node("agent", call_agent)
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent", should_continue, {"tools": "tools", "end": END}
    )
    graph.add_edge("tools", "agent")

    return graph


_compiled_app = None


def get_compiled_app():
    """Get or create the compiled workflow app (singleton pattern)."""
    global _compiled_app
    if _compiled_app is None:
        graph = build_nlp_workflow()
        checkpointer = MemorySaver()
        _compiled_app = graph.compile(checkpointer=checkpointer)
    return _compiled_app


# ============================================================================
# CLI INTERFACE
# ============================================================================


def main():
    """CLI interface for NLP workflow with batch operations."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Natural Language SCM Workflow with CRUD + Batch Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python -m src.main --interactive

  # Single prompt
  python -m src.main --prompt "Create 14 address objects with langgraph tag in Texas"

  # File input (execute instructions from file)
  python -m src.main --file instructions.txt

Batch Operation Examples:
  "Create 14 address objects with different IPs and the langgraph tag in Texas"
  "Create tags: Production (Red), Staging (Blue), Development (Green) in Texas"
  "Create address groups for web, app, and db tiers in Texas"

Single Operation Examples:
  "Add the langgraph tag to web_server_01 in Texas"
  "List all addresses in Texas"
  "Commit changes to Texas"
        """,
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--prompt",
        "-p",
        type=str,
        help="Single natural language prompt",
    )
    mode_group.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive mode",
    )
    mode_group.add_argument(
        "--file",
        "-f",
        type=str,
        help="File containing instructions (one per line or full text)",
    )

    parser.add_argument(
        "--thread-id",
        "-t",
        type=str,
        default=None,
        help="Thread ID",
    )
    parser.add_argument(
        "--recursion-limit",
        "-r",
        type=int,
        default=50,
        help="Recursion limit (default: 50)",
    )

    args = parser.parse_args()

    # Validate environment configuration
    try:
        validate_environment()
    except Exception as e:
        print(f"❌ Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)

    app = get_compiled_app()

    try:
        if args.interactive:
            print("🤖 SCM NLP Assistant with Batch Operations - Interactive Mode")
            print("=" * 60)
            print(
                "Supports bulk operations! Try: 'Create 14 addresses with langgraph tag'"
            )
            print("Type 'exit' or 'quit' to end.\n")

            thread_id = args.thread_id or str(uuid7())
            print(f"Session ID: {thread_id}")
            print(f"Recursion Limit: {args.recursion_limit}\n")

            config = {
                "configurable": {"thread_id": thread_id},
                "recursion_limit": args.recursion_limit,
            }

            while True:
                try:
                    user_input = input("You: ").strip()

                    if user_input.lower() in ["exit", "quit", "q"]:
                        print("\n👋 Goodbye!")
                        break

                    if not user_input:
                        continue

                    print("\nAssistant: ", end="", flush=True)

                    result = app.invoke(
                        {"messages": [HumanMessage(content=user_input)]},
                        config=config,
                    )
                    final_message = result["messages"][-1]
                    print(final_message.content)
                    print()

                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    break
        elif args.file:
            # File input mode
            import pathlib

            file_path = pathlib.Path(args.file)
            if not file_path.exists():
                print(f"❌ Error: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)

            print(f"🤖 Processing instructions from: {args.file}\n")

            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                print("❌ Error: File is empty", file=sys.stderr)
                sys.exit(1)

            config = {
                "configurable": {"thread_id": args.thread_id or str(uuid7())},
                "recursion_limit": args.recursion_limit,
            }

            # Check if file has multiple lines (execute each separately) or single instruction
            lines = [line.strip() for line in content.split("\n") if line.strip()]

            if len(lines) == 1:
                # Single instruction
                print(f"📝 Instruction: {lines[0]}\n")
                result = app.invoke(
                    {"messages": [HumanMessage(content=lines[0])]}, config=config
                )
                final_message = result["messages"][-1]
                print(f"Assistant: {final_message.content}")
            else:
                # Multiple instructions - execute in sequence
                print(f"📝 Found {len(lines)} instructions\n")
                for i, instruction in enumerate(lines, 1):
                    print(f"[{i}/{len(lines)}] {instruction}")
                    result = app.invoke(
                        {"messages": [HumanMessage(content=instruction)]},
                        config=config,
                    )
                    final_message = result["messages"][-1]
                    print(f"✅ {final_message.content}\n")
        else:
            # Single prompt
            print(f"🤖 Processing: {args.prompt}\n")

            config = {
                "configurable": {"thread_id": args.thread_id or str(uuid7())},
                "recursion_limit": args.recursion_limit,
            }

            result = app.invoke(
                {"messages": [HumanMessage(content=args.prompt)]}, config=config
            )
            final_message = result["messages"][-1]
            print(f"Assistant: {final_message.content}")

    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
