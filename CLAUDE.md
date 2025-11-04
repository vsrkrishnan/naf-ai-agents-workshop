# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LangGraph workshop teaching network automation engineers to build AI agents for Palo Alto Networks Strata Cloud Manager using LangGraph and Claude AI. 11 progressive notebooks (101-111) covering state management, workflows, and AI integration.

**Target audience**: Network security engineers with basic Python knowledge
**Core tech**: LangGraph 0.2.50+, Claude AI (Anthropic), pan-scm-sdk, Python 3.11+

## CRITICAL: Git Commit Rules

**NEVER use Claude/Claude Code as commit author or co-author. This is non-negotiable.**

### Commit Authorship Rules
- **ALWAYS** use git config from user profile: Calvin Remsburg <calvin@cdot.io>
- **NEVER** add "Generated with Claude Code" to commit messages
- **NEVER** add "Co-Authored-By: Claude" to commit messages
- **NEVER** mention Claude/AI in commit messages at all
- Commits MUST appear as if written by the repository owner only

### Verification Before Committing
```bash
# Always check author before committing
git config user.name    # Must be: Calvin Remsburg
git config user.email   # Must be: calvin@cdot.io
```

### Commit Message Format
```bash
# ✅ CORRECT - Simple, clean, author from git config
git commit -m "Add notebook 101 exercises"

# ❌ WRONG - Contains Claude references
git commit -m "Add exercises

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Development Commands

### Setup & Environment
```bash
make setup              # Install deps with uv, configure git filters, create .env
make dev                # Install with dev dependencies
make jupyter            # Launch Jupyter Lab for interactive development
```

### Testing Notebooks
```bash
# Test individual notebooks
make test-101           # Through make test-111

# Test by phase
make test-phase1        # Notebooks 101-107 (no API key)
make test-phase2        # Notebooks 108-111 (requires ANTHROPIC_API_KEY)
make test-all           # All notebooks

# Clean outputs
make clean              # All notebooks
make clean-phase1       # Phase 1 only
make clean-phase2       # Phase 2 only
```

### LangGraph Studio
```bash
make studio-install     # Install LangGraph CLI
make studio-check       # Verify dependencies
make studio             # Launch at http://localhost:8123
```

### CLI Tools
```bash
# Run NLP workflow (from src/main.py)
python -m src.main --interactive
python -m src.main --prompt "List tags in Texas"
python -m src.main --file instructions.txt

# Or via script entry point
scm-agent --interactive
```

### Code Quality
```bash
make format             # Black formatting
make lint               # Flake8 linting
```

## Architecture

### Notebook Structure (Progressive Learning)
- **Phase 1 (101-107)**: LangGraph foundations, no LLM required
  - 101: TypedDict, Union, Optional
  - 102: State, Nodes, Edges, Graphs
  - 103: First single-node graph
  - 104: Complex state management
  - 105: Sequential multi-node workflows
  - 106: Conditional routing
  - 107: Looping with retry/pagination

- **Phase 2 (108-111)**: LLM integration (requires API key)
  - 108: First Claude integration
  - 109: Conversational memory
  - 110: ReAct agents with tools
  - 111: Human-in-the-loop patterns

### Source Code Structure
```
src/
├── main.py              # Monolithic NLP workflow (all-in-one)
├── core/
│   ├── state.py         # AgentState TypedDict with add_messages
│   ├── client.py        # SCM client singleton
│   └── config.py        # Environment validation
└── cli/
    ├── app.py           # Typer CLI application
    └── commands/        # CLI command modules
```

**Migration in progress**: Moving from monolithic `main.py` to modular structure with separate `tools/`, `models/`, `nodes/`, `graph/` directories. See `src/README.md` for migration plan.

### Key Patterns

**State Definition** (core/state.py):
```python
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

**Graph Construction**:
```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)
graph.add_node("node_name", node_function)
graph.add_edge(START, "node_name")
graph.add_edge("node_name", END)
app = graph.compile()
```

**Conditional Routing**:
```python
def router_func(state) -> Literal["path_a", "path_b"]:
    return "path_a" if condition else "path_b"

graph.add_conditional_edges(
    "router",
    router_func,
    {"path_a": "node_a", "path_b": "node_b"}
)
```

**ReAct Agent with Tools**:
```python
from langchain_core.tools import StructuredTool

@tool
def my_tool(param: str) -> str:
    """Tool docstring used by LLM for selection."""
    return result

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
model_with_tools = llm.bind_tools([my_tool])
```

## Environment Variables

Required in `.env` (copy from `.env.template`):
```bash
# Phase 2 notebooks (108-111)
ANTHROPIC_API_KEY=sk-...

# CLI/workflows (optional)
SCM_CLIENT_ID=
SCM_CLIENT_SECRET=
SCM_TSG_ID=

# LangSmith tracing (optional)
LANGCHAIN_TRACING_V2=true
LANGSMITH_API_KEY=
```

## Git Configuration

**Auto-stripping notebook outputs**: Git filters configured via `scripts/setup_git_filters.sh` (runs in `make setup`). Committed notebooks have clean outputs.

## Notebook Development Guidelines

### Educational Standards
- Progressive complexity: simple → complex
- Markdown explanations before code cells
- Working examples students can run immediately
- Exercises/challenges at section ends
- Network automation examples (routers, firewalls, SCM objects)

### Notebook Structure
1. **Title cell**: Metadata (title, duration, difficulty, objectives, prerequisites, TOC)
2. **Setup section**: Imports, env vars, dependency checks
3. **Content sections**: Alternating markdown/code with subsections (### N.1, ### N.2)
4. **Summary**: Key concepts recap
5. **Test**: Execute top to bottom without errors

### Code Cell Guidelines
- One concept per cell
- Show output/results
- Use network domain examples (addresses, rules, tags, policies)
- Include assertions for validation
- Visualize graphs: `display(Image(app.get_graph().draw_mermaid_png()))`

### Tone
- Conversational yet professional
- Active voice ("you will", "we'll")
- Explain "why" before "how"
- Problem → Solution pattern
- Use 💡 for tips, ✅/❌ for examples/anti-patterns

## SCM Integration

Workshop uses **pan-scm-sdk** for Palo Alto Networks Strata Cloud Manager automation:
- Address objects (IP/FQDN/Range)
- Security rules
- NAT policies
- Tags
- Address groups
- Services/Service groups

Pattern: Tag → Address → Group → Rule (sequential dependencies)

## Testing Approach

**Phase 1 (101-107)**: No API costs, pure LangGraph mechanics with mock data
**Phase 2 (108-111)**: Claude Haiku (~$0.25 per 1M tokens)

All notebooks tagged `skip-execution` for cells requiring human input.

## Common Tasks

### Creating New Notebooks
- Use VSCode/Cursor "New Jupyter Notebook" (never bash/cat)
- Follow numbering: `1NN_topic_name.ipynb`
- Match structure of existing notebooks
- Add to Makefile test targets
- Update README.md

### Modifying Workflows
- Main workflow: `src/main.py` (monolithic, being modularized)
- Tools use Pydantic validation
- Batch operations to avoid recursion limits
- Commit operations with job status monitoring

### Adding Tools
Current location: `src/main.py` (inline)
Future location: `src/tools/{domain}/` (planned)

Pattern:
```python
def _tool_name(param: Model) -> str:
    """Tool description for LLM."""
    client = get_scm_client()
    # Implementation
    return summary_string

tools.append(StructuredTool.from_function(
    func=_tool_name,
    name="tool_name",
    description="When to use this tool"
))
```

## Dependencies

Core (pyproject.toml):
- langgraph >= 0.2.50
- langchain-anthropic >= 0.3.0
- langchain-core >= 0.3.0
- pan-scm-sdk >= 0.3.44
- python-dotenv >= 1.0.0
- jupyter >= 1.1.1

Optional:
- langgraph-checkpoint-sqlite (persistence)
- langfuse (observability)
- playwright (web search examples)

## Known Issues

- Recursion limits: Use batch operations for bulk creates
- Job monitoring: Use `check_job_status` tool for async commits
- Memory management: Conversation history grows linearly with tokens

## Workshop Delivery

4-hour instructor-led format:
- **Session 1 (0:00-2:00)**: Phase 1 foundations + Q&A
- **Break (2:00-2:15)**: API key setup
- **Session 2 (2:15-3:45)**: Phase 2 LLM integration
- **Wrap-up (3:45-4:00)**: Next steps, resources

GitHub Codespaces preferred for zero-install experience.

## Contributing

See CONTRIBUTING.md for:
- PR workflow
- Code style (Black, PEP 8)
- Testing requirements
- Branch naming conventions

## Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Author: calvin@cdot.io
