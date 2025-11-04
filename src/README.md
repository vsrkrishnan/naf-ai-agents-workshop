# SCM NLP Workflow Package

A portable Python package for natural language SCM automation using LangGraph.

## Current Structure

```
src/
├── __init__.py          # Package initialization
└── main.py              # Monolithic workflow (all components)
```

## Usage

### 1. Interactive Mode

```bash
# Using Python module
python -m src.main --interactive

# Using CLI wrapper
./scm-nlp --interactive
```

**Features**:
- Conversational interface
- Maintains conversation history
- Type 'exit' or 'quit' to end session

### 2. Single Prompt Mode

```bash
# Using Python module
python -m src.main --prompt "Create 3 tags in Texas: Dev, Test, Prod"

# Using CLI wrapper
./scm-nlp --prompt "List all addresses in Texas"
```

**Features**:
- Execute single command
- Quick operations
- No conversation history

### 3. File Input Mode (NEW!)

```bash
# Using Python module
python -m src.main --file instructions.txt

# Using CLI wrapper
./scm-nlp --file my_tasks.txt
```

**Features**:
- Execute multiple instructions from a file
- One instruction per line
- Sequential execution with session continuity

**Example file** (`instructions.txt`):
```
List all tags in Texas
Create 3 tags in Texas: Development (Blue), Staging (Green), Production (Red)
List all addresses in Texas
Commit changes to Texas with description "Added new tags"
```

### 4. LangGraph Studio

Studio requires the original workflow file structure:

```bash
cd workflows
uv run langgraph dev
# Or use make command
make studio
```

## Options

| Flag | Short | Description | Example |
|------|-------|-------------|---------|
| `--interactive` | `-i` | Interactive mode | `-i` |
| `--prompt` | `-p` | Single prompt | `-p "List tags"` |
| `--file` | `-f` | File input | `-f tasks.txt` |
| `--thread-id` | `-t` | Custom thread ID | `-t my-session` |
| `--recursion-limit` | `-r` | Max recursion | `-r 100` |

## Environment Variables

Required:
```bash
SCM_CLIENT_ID="your-client-id"
SCM_CLIENT_SECRET="your-secret"
SCM_TSG_ID="your-tsg-id"
ANTHROPIC_API_KEY="your-api-key"
```

Optional (LangSmith tracing):
```bash
LANGCHAIN_TRACING_V2=true
LANGSMITH_API_KEY="your-langsmith-key"
LANGSMITH_WORKSPACE_ID="your-workspace-id"
LANGCHAIN_PROJECT="your-project-name"
```

## Planned Modular Structure

The next phase will refactor `main.py` into a modular architecture:

```
src/
├── __init__.py
├── main.py                    # CLI entry point only
│
├── core/
│   ├── __init__.py
│   ├── client.py             # SCM client initialization
│   ├── state.py              # AgentState definition
│   └── config.py             # Configuration management
│
├── models/
│   ├── __init__.py
│   ├── tag.py                # Tag-related Pydantic models
│   ├── address.py            # Address-related models
│   ├── address_group.py      # Address group models
│   └── batch.py              # Batch request models
│
├── tools/
│   ├── __init__.py
│   ├── tags/
│   │   ├── __init__.py
│   │   ├── create.py         # tag_create, tag_create_batch
│   │   ├── read.py           # tag_read, tag_list
│   │   └── update.py         # tag_update (future)
│   │
│   ├── addresses/
│   │   ├── __init__.py
│   │   ├── create.py         # address_create, address_create_batch
│   │   ├── read.py           # address_read, address_list
│   │   └── update.py         # address_update
│   │
│   ├── address_groups/
│   │   ├── __init__.py
│   │   ├── create.py         # address_group_create, address_group_create_batch
│   │   └── read.py           # address_group_read, address_group_list
│   │
│   └── jobs/
│       ├── __init__.py
│       ├── commit.py         # commit_changes
│       └── status.py         # check_job_status
│
├── nodes/
│   ├── __init__.py
│   ├── agent.py              # call_agent node
│   └── routing.py            # should_continue routing logic
│
├── graph/
│   ├── __init__.py
│   ├── builder.py            # build_nlp_workflow
│   └── compiler.py           # get_compiled_app
│
└── cli/
    ├── __init__.py
    ├── interactive.py        # Interactive mode handler
    ├── prompt.py             # Single prompt handler
    └── file.py               # File input handler
```

### Benefits of Modular Structure

1. **Maintainability**
   - Each component in its own file
   - Clear separation of concerns
   - Easier to find and fix bugs

2. **Testability**
   - Individual functions can be unit tested
   - Mock dependencies easily
   - Clear test boundaries

3. **Extensibility**
   - Add new tools without touching existing code
   - Plugin architecture for future features
   - Easy to add new SCM object types

4. **Reusability**
   - Import specific tools in other projects
   - Use models independently
   - Share common utilities

5. **Collaboration**
   - Multiple developers can work on different modules
   - Clear ownership boundaries
   - Reduced merge conflicts

## Migration Plan

Phase 1: **Package Setup** ✅ (COMPLETE)
- [x] Create `src/` directory structure
- [x] Copy workflow to `src/main.py`
- [x] Add `__init__.py`
- [x] Create CLI wrapper script
- [x] Update `pyproject.toml`
- [x] Add file input mode
- [x] Test all execution modes

Phase 2: **Core Extraction** (NEXT)
- [ ] Extract `AgentState` to `core/state.py`
- [ ] Extract SCM client to `core/client.py`
- [ ] Create `core/config.py` for environment management
- [ ] Update imports in `main.py`

Phase 3: **Models Extraction**
- [ ] Extract Pydantic models to `models/`
- [ ] Separate by domain (tags, addresses, groups, batches)
- [ ] Create model exports in `models/__init__.py`

Phase 4: **Tools Extraction**
- [ ] Create `tools/` directory structure
- [ ] Extract tag tools to `tools/tags/`
- [ ] Extract address tools to `tools/addresses/`
- [ ] Extract address group tools to `tools/address_groups/`
- [ ] Extract job management to `tools/jobs/`
- [ ] Create tool registration system

Phase 5: **Nodes & Graph Extraction**
- [ ] Extract agent node to `nodes/agent.py`
- [ ] Extract routing to `nodes/routing.py`
- [ ] Extract graph builder to `graph/builder.py`
- [ ] Extract compiler to `graph/compiler.py`

Phase 6: **CLI Extraction**
- [ ] Extract interactive mode to `cli/interactive.py`
- [ ] Extract prompt mode to `cli/prompt.py`
- [ ] Extract file mode to `cli/file.py`
- [ ] Simplify `main.py` to just CLI routing

Phase 7: **Testing & Documentation**
- [ ] Write unit tests for each module
- [ ] Integration tests for full workflows
- [ ] Update documentation
- [ ] Create module-specific READMEs

Phase 8: **Advanced Features**
- [ ] Add tool discovery/registration system
- [ ] Implement plugin architecture
- [ ] Add configuration file support (YAML/JSON)
- [ ] Create workflow templates

## Development Workflow

### Current (Monolithic)

```python
# Everything in one file
from src.main import get_compiled_app, main

# Run CLI
main()

# Use in other code
app = get_compiled_app()
result = app.invoke({"messages": [...]})
```

### Future (Modular)

```python
# Import specific components
from src.core import get_scm_client
from src.models import BatchTagRequest, TagConfigForBatch
from src.tools.tags import create_tag_batch
from src.graph import get_compiled_app

# Use tools individually
client = get_scm_client()
request = BatchTagRequest(
    tags=[TagConfigForBatch(name="Dev", color="Blue")],
    folder="Texas"
)
result = create_tag_batch(request)

# Or use full workflow
app = get_compiled_app()
result = app.invoke({"messages": [...]})
```

## LangGraph Studio Integration

The modular structure will still support LangGraph Studio through a compatibility layer:

```json
// workflows/langgraph.json
{
  "dependencies": ["."],
  "graphs": {
    "scm_nlp_workflow": "../src/graph/builder.py:get_compiled_app"
  },
  "env": "../.env"
}
```

## Next Steps

1. **Start modularization** - Begin Phase 2 (Core Extraction)
2. **Maintain backward compatibility** - Keep `main.py` working during refactoring
3. **Add tests** - Write tests as modules are created
4. **Update documentation** - Keep this README current
5. **Iterate** - Refine structure based on usage patterns

---

**Current Status**: ✅ Phase 1 Complete - Package structure created and tested

**Ready for**: Phase 2 - Core module extraction
