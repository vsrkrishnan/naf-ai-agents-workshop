# LangGraph Workshop for Network Security Engineers

## Comprehensive Outline: Teaching LangGraph with Palo Alto Networks Strata Cloud Manager

**Target Audience:** Network security engineers and administrators
**Prerequisites:** Basic Python knowledge, familiarity with PAN-OS/SCM concepts
**Total Duration:** 14-18 hours for complete mastery
**Teaching Philosophy:** Problem-first, hands-on learning, progressive complexity
**Focus:** Real-world network automation using pan-scm-sdk
**Last Updated:** 2025-10-20

---

## Table of Contents

1. [Workshop Overview](#workshop-overview)
2. [Workshop Structure](#workshop-structure)
3. [Phase 1: Foundations (Notebooks 101-107)](#phase-1-foundations-notebooks-101-107)
4. [Phase 2: LLM Integration (Notebooks 108-111)](#phase-2-llm-integration-notebooks-108-111)
5. [Learning Path and Dependencies](#learning-path-and-dependencies)
6. [Teaching Guidelines](#teaching-guidelines)
7. [Appendices](#appendices)

---

## Workshop Overview

### Learning Path Architecture

```
Phase 1: Foundations (No LLM Required)
    101 → 102 → 103 → 104 → 105 → 106 → 107
    Type  Core   First Complex Sequential Conditional Looping
    Annot Concept Graph  State  Workflows  Routing    Workflows

Phase 2: LLM Integration (API Keys Required)
    108 → 109 → 110 → 111
    Simple Conversa- ReAct  Human-in-
    Bot   tional   Agents  the-Loop
          Memory   +Tools  
```

### Workshop Status

**All notebooks COMPLETE:** ✅

- **Phase 1 (101-107):** 7 notebooks - Pure workflow mechanics
- **Phase 2 (108-111):** 4 notebooks - AI-powered agents
- **Total:** 11 notebooks ready for delivery

### Core Principles

**Network Administrator Perspective:**

- Use networking analogies (ACLs, routing protocols, configuration modes)
- Reference familiar CLI workflows and configuration patterns
- Emphasize safety, validation, and change management
- Show practical production scenarios from real firewall operations

**Progressive Complexity:**

- Start simple with 1-2 concepts per notebook
- Build incrementally on previous learnings
- Provide real examples before introducing abstractions
- Hands-on practice before diving into theory

**Code Patterns:**

- Consistent structure across all notebooks
- Real SCM operations using actual pan-scm-sdk code
- Production-ready error handling included
- Reference actual code from `docs/examples/*.py`

---

## Workshop Structure

### Phase 1: Foundations (Notebooks 101-107)

**Duration:** 8-10 hours | **No API Keys Required**

Builds core LangGraph skills without requiring LLM integration. Students learn:

- Type safety and state management
- Graph construction patterns
- Node and edge mechanics
- Conditional routing and loops
- SCM workflow automation

### Phase 2: LLM Integration (Notebooks 108-111)

**Duration:** 6-8 hours | **Anthropic API Key Required**

Adds AI capabilities to workflows. Students learn:

- LLM integration with Claude
- Conversation memory management
- Tool creation and binding
- ReAct pattern implementation
- Human-in-the-loop collaboration

---

## Phase 1: Foundations (Notebooks 101-107)

### Notebook 101: Type Annotations and TypedDict

**Status:** ✅ COMPLETE
**Duration:** ~5 minutes
**Difficulty:** Beginner
**Prerequisites:** Basic Python syntax

#### Learning Objectives

- Understand Python dictionaries as flexible data containers
- Learn TypedDict for structured dictionary schemas with type safety
- Master Union types for handling multiple possible types
- Use Optional for representing nullable values
- Understand Any for dynamic typing scenarios
- Apply Lambda functions for inline operations

#### Key Concepts Introduced

- **State Management Foundation:** TypedDict is how LangGraph defines state schemas
- **Type Safety:** Prevents configuration errors before runtime
- **IDE Support:** TypedDict enables autocomplete and error checking
- **SCM Integration:** Applied to real address object and security rule structures

#### SCM/Pan-SDK Examples

**Reference:** `docs/examples/address_objects.py` (lines 9-37), `docs/examples/security_policy.py`

- **Address Objects:** IP/Netmask, FQDN, and IP Range configurations
- **Security Rules:** Complete firewall rule structures with logging
- **Validation Patterns:** Error-checking logic for configuration safety
- **Lambda Processing:** Filtering rules by action, tags, and zones

#### Code Patterns

```python
from typing import TypedDict, Optional, Union

# TypedDict for SCM Address Object
class AddressObjectNetmask(TypedDict):
    name: str
    ip_netmask: str
    folder: str
    description: Optional[str]
    tag: Optional[list[str]]

# Security Rule with Union types
class SecurityRuleFull(TypedDict):
    name: str
    from_: list[str]
    to_: list[str]
    source: list[str]
    destination: list[str]
    application: list[str]
    service: list[str]
    action: str  # "allow", "deny", "drop"
    tag: Optional[list[str]]
    log_end: Optional[bool]

# Lambda for filtering
allow_rules = list(filter(lambda rule: rule["action"] == "allow", all_rules))
```

#### Hands-On Exercises

1. Build address object TypedDict with 4 fields
2. Create security policy state schema with validation
3. Add error handling demonstration
4. Build progressive complexity levels (4 stages)

#### Dependencies

- **Builds on:** Basic Python knowledge
- **Required for:** All subsequent notebooks (foundation for state management)

---

### Notebook 102: Core Concepts - State, Nodes, and Graphs

**Status:** ✅ COMPLETE
**Duration:** ~30 minutes
**Difficulty:** Beginner
**Prerequisites:** Notebook 101 (Type Annotations)

#### Learning Objectives

- Understand State and how it flows through LangGraph applications
- Learn to create Nodes that process and update state
- Master Graph construction with StateGraph
- Use Edges to define workflow connections
- Implement basic graph patterns with START and END
- Preview Conditional Edges and Tools for future notebooks

#### Key Concepts Introduced

- **State Persistence:** How state accumulates through workflow (like tracking SCM object creation)
- **Node Functions:** Standard Python functions that take state, return dict with updates
- **Partial State Updates:** Nodes only return fields they modify, not entire state
- **Graph Compilation:** `.compile()` transforms StateGraph into executable Runnable
- **Sequential Execution:** Using `add_edge()` to connect nodes in specific order

#### SCM/Pan-SDK Examples

**Reference:** `docs/examples/address_objects.py`, `docs/examples/address_groups.py`

- **Complete SCM Address Creation Workflow:** validate → prepare → create → verify pipeline
- **3-Node Pipeline:** parse → validate → format for API-ready configurations
- **Tag → Address → Group Workflow:** Demonstrates dependencies
- **Real API Patterns:** Simulates client.address.create(), client.address.get()

#### Code Patterns

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional

class SCMAddressState(TypedDict):
    name: str
    ip_netmask: str
    folder: str
    validated: bool
    created: bool
    object_id: Optional[str]
    workflow_log: str

def validate_address(state: SCMAddressState) -> dict:
    """Validate address object configuration."""
    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$', state['ip_netmask']):
        return {"validated": False, "errors": ["Invalid IP format"]}
    return {"validated": True, "errors": []}

# Build Graph
graph = StateGraph(SCMAddressState)
graph.add_node("validate", validate_address)
graph.add_node("create", create_in_scm)
graph.add_edge(START, "validate")
graph.add_edge("validate", "create")
graph.add_edge("create", END)
app = graph.compile()

# Execute
result = app.invoke(initial_state)
```

#### Hands-On Exercises

1. Build 3-node address object pipeline (parse → validate → format)
2. Design security policy state schema with 10+ fields
3. Add error handling node to workflow
4. Build progressive complexity levels (1-4)

#### Dependencies

- **Builds on:** Notebook 101 (TypedDict fundamentals)
- **Required for:** Notebooks 103-111 (foundation for all graph patterns)

---

### Notebook 103: Your First Graph - Foundation

**Status:** ✅ COMPLETE
**Duration:** ~20 minutes
**Difficulty:** Beginner
**Prerequisites:** Notebooks 101 (Type Annotations), 102 (Core Concepts)

#### Learning Objectives

- Define agent state structure using TypedDict
- Create simple node functions that process and update state
- Build your first basic LangGraph structure
- Understand how to compile and invoke graphs
- See how data flows through a single node in LangGraph
- Apply these concepts to validate SCM address objects

#### Key Concepts Introduced

- **The "Hello World" Graph:** Simplest possible LangGraph structure (START → node → END)
- **State Definition:** Creating TypedDict schemas for workflow data
- **Node Creation:** Writing Python functions that process state
- **Graph Building:** Using StateGraph to assemble nodes and edges
- **Compilation:** Converting graph definition to executable application
- **Execution:** Invoking graphs with initial state values

#### SCM/Pan-SDK Examples

**Reference:** `docs/examples/address_objects.py`

- **Address Object Validation:** Simple validation workflow for SCM address objects
- **Extended Address State:** Three-field state tracking (name, folder, validation_status)
- **Production Pattern:** Simulates real address object validation before SCM API calls

#### Code Patterns

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AddressObjectState(TypedDict):
    name: str
    status: str

def validate_address_object(state: AddressObjectState) -> dict:
    """Validate SCM address object configuration."""
    address_name = state["name"]
    result = f"Address object '{address_name}' validated successfully"
    return {"status": result}  # Partial update

# Build Graph
graph = StateGraph(AddressObjectState)
graph.add_node("validate", validate_address_object)
graph.add_edge(START, "validate")
graph.add_edge("validate", END)
app = graph.compile()

# Execute
result = app.invoke({"name": "web_server_01", "status": ""})
```

#### Hands-On Exercises

1. Build extended address validation workflow with 3 fields
2. Add folder validation to workflow
3. Create multi-field state with validation tracking

#### Dependencies

- **Builds on:** Notebooks 101 (TypedDict), 102 (Core Concepts)
- **Required for:** Notebooks 104-111 (foundation for all multi-node patterns)

---

### Notebook 104: State Management - Complex Data

**Status:** ✅ COMPLETE
**Duration:** ~20 minutes
**Difficulty:** Beginner
**Prerequisites:** Notebook 103 (Your First Graph)

#### Learning Objectives

- Design multi-field state schemas with TypedDict
- Work with diverse data types (strings, lists, integers, booleans, dictionaries)
- Implement safe state access patterns
- Handle optional fields and defaults
- Build complex SCM object structures

#### Key Concepts Introduced

- **Multi-Field State Schemas:** Tracking multiple related pieces of information
- **Type Diversity in State:** Single state can hold multiple data types simultaneously
- **List Processing:** Handling zone lists, tag lists, application lists in security rules
- **State Safety:** Only read fields that were provided as input or set by previous nodes
- **Progressive Complexity:** Starting simple (2-3 fields) and scaling up (10+ fields)

#### SCM/Pan-SDK Examples

**Reference:** `docs/examples/security_policy.py`, `docs/examples/address_objects.py`

- **Security Rule Validation:** Multi-zone, multi-application rule structures
- **Address Type Operations:** Handling different address types (IP/FQDN/Range)
- **Complete SCM Workflow:** Tag → Address → Group creation with dependencies
- **Real API Structures:** Matching pan-scm-sdk configuration formats

#### Code Patterns

```python
from typing import TypedDict, List

class SecurityRuleState(TypedDict):
    rule_name: str                  # String
    source_zones: List[str]         # List of strings
    destination_zones: List[str]    # List of strings
    validated: bool                 # Boolean
    result: str                     # String

def validate_security_rule(state: SecurityRuleState) -> dict:
    rule_name = state["rule_name"]
    source_zones = state["source_zones"]
    dest_zones = state["destination_zones"]
    
    total_zones = len(source_zones) + len(dest_zones)
    result = f"Rule '{rule_name}': {len(source_zones)} source, {len(dest_zones)} dest zones"
    
    return {"validated": True, "result": result}

# Safe State Access Pattern
def safe_node(state: MyState) -> dict:
    # Read fields you KNOW were provided
    hostname = state["hostname"]
    metrics = state["interface_metrics"]
    
    # Compute NEW value (don't read uninitialized)
    result = f"Report for {hostname}: {sum(metrics)}%"
    return {"result": result}  # Only assign, don't read uninitialized fields
```

#### Hands-On Exercises

1. Build address type validator supporting IP/FQDN/Range types
2. Create advanced metrics calculator with sum/average operations
3. Design complete SCM workflow state with 10+ fields

#### Dependencies

- **Builds on:** Notebook 103 (basic state and graphs)
- **Required for:** Notebook 105 (sequential workflows need complex state)

---

### Notebook 105: Sequential Workflows - Multi-Node Graphs

**Status:** ✅ COMPLETE
**Duration:** ~30 minutes
**Difficulty:** Intermediate
**Prerequisites:** Notebooks 103 (First Graph), 104 (Complex State)

#### Learning Objectives

- Build multi-node graphs with sequential execution
- Chain nodes together using add_edge()
- Implement error handling across workflow steps
- Understand state transformation through pipelines
- Create complete SCM workflows
- Visualize complex graph structures

#### Key Concepts Introduced

- **Multi-Node Sequential Graphs:** Building workflows with 2-3+ processing steps
- **Node Chaining:** Using `add_edge()` to connect nodes in specific order
- **State Accumulation:** How state builds up through multiple nodes
- **Error Handling Patterns:** Try/except blocks and error state tracking
- **Production SCM Workflows:** Complete Tag → Address → Group creation pipelines
- **Dependency Management:** Ensuring prerequisite steps complete before dependent steps

#### SCM/Pan-SDK Examples

**Reference:** `docs/examples/address_objects.py`, `docs/examples/address_groups.py`

- **2-Node Address Creation:** validate → create pipeline
- **3-Node Complete Workflow:** create_tag → create_address → create_group
- **Error Handling:** InvalidObjectError, NameNotUniqueError, ObjectNotPresentError patterns
- **API Simulation:** Matches real client.tag.create(), client.address.create(), client.address_group.create()

#### Code Patterns

```python
from typing import TypedDict, List

class CompleteSCMConfigState(TypedDict):
    folder: str
    tag_name: str
    address_name: str
    ip_netmask: str
    group_name: str
    tag_created: bool
    address_created: bool
    group_created: bool
    workflow_log: str

# Node 1: Create Tag
def create_tag_node(state: CompleteSCMConfigState) -> dict:
    tag_id = f"tag-{uuid.uuid4().hex[:8]}"
    log = f"Created tag '{state['tag_name']}' with ID={tag_id}\n"
    return {"tag_created": True, "tag_id": tag_id, "workflow_log": log}

# Node 2: Create Address (with dependency check)
def create_address_node(state: CompleteSCMConfigState) -> dict:
    if not state["tag_created"]:
        raise ValueError("Cannot create address: tag must be created first!")
    # ... create address logic
    return {"address_created": True, "workflow_log": updated_log}

# Build Sequential Graph
graph = StateGraph(CompleteSCMConfigState)
graph.add_node("create_tag", create_tag_node)
graph.add_node("create_address", create_address_node)
graph.add_node("create_group", create_group_node)

graph.add_edge(START, "create_tag")
graph.add_edge("create_tag", "create_address")
graph.add_edge("create_address", "create_group")
graph.add_edge("create_group", END)

app = graph.compile()
```

#### Hands-On Exercises

1. Build 3-node SCM address object workflow
2. Add comprehensive error handling
3. Create batch processing workflow
4. Implement retry logic for failed API calls

#### Dependencies

- **Builds on:** Notebooks 103 (basic graphs), 104 (complex state)
- **Required for:** Notebook 106 (conditional routing builds on sequential patterns)

---

### Notebook 106: Conditional Routing - Decision-Making Graphs

**Status:** ✅ COMPLETE
**Duration:** ~20 minutes
**Difficulty:** Intermediate
**Prerequisites:** Notebooks 103-105 (Graph patterns)

#### Learning Objectives

- Understand `add_conditional_edges()` API for dynamic routing
- Create router functions with `Literal` return types for type-safe routing
- Implement branching workflows based on state conditions
- Master lambda passthrough pattern for router nodes
- Route SCM workflows based on address types
- Apply network ACL match logic analogy to conditional routing
- Build decision trees similar to firewall rule processing

#### Key Concepts Introduced

- **Network ACL Analogy:** Routing works like firewall rule matching (condition → action)
- **Conditional Routing:** Making decisions about which path to take based on state
- **Router Functions:** Examine state and return edge name (string, not dict!)
- **Lambda Passthrough Pattern:** `lambda state: state` for router nodes
- **Literal Return Types:** Type-safe edge name declarations
- **Multi-Way Routing:** 2-way, 3-way, or N-way branching

#### SCM/Pan-SDK Examples

**Reference:** `docs/examples/address_objects.py`

- **Folder-Based Routing:** Production requires approval, Development allows direct creation
- **Address Type Routing:** Route IP/netmask → CIDR validator, FQDN → DNS validator, Range → Range validator
- **Configuration Change Router:** Route different change types to appropriate handlers
- **Environment-Specific Logic:** Different paths for dev/staging/prod folders

#### Code Patterns

```python
from typing import Literal, TypedDict

class ConditionalFolderState(TypedDict):
    folder: str
    requires_approval: bool

# Router Function with Literal Return Type
def decide_creation_path(state: ConditionalFolderState) -> Literal["approval_path", "direct_path"]:
    """Router: Decide which creation path based on approval requirement."""
    if state["requires_approval"]:
        return "approval_path"
    else:
        return "direct_path"

# Build Graph with Conditional Routing
graph = StateGraph(ConditionalFolderState)

# Add router node with lambda passthrough (CRITICAL!)
graph.add_node("router", lambda state: state)

# Add processing nodes
graph.add_node("create_with_approval", create_with_approval)
graph.add_node("create_direct", create_without_approval)

# Set entry point
graph.add_edge(START, "router")

# Add conditional edges (THE MAGIC!)
graph.add_conditional_edges(
    source="router",
    path=decide_creation_path,
    path_map={
        "approval_path": "create_with_approval",
        "direct_path": "create_direct"
    }
)

# Connect to END
graph.add_edge("create_with_approval", END)
graph.add_edge("create_direct", END)

app = graph.compile()
```

#### Hands-On Exercises

1. Build configuration change type router (3-way routing)
2. Implement environment-based routing (dev/stage/prod)
3. Create validation router with success/failure paths
4. Build address type validator with 3 validation paths

#### Dependencies

- **Builds on:** Notebooks 103-105 (sequential graph patterns)
- **Required for:** Notebook 107 (looping combines conditional routing)

---

### Notebook 107: Looping Workflows - Retry and Iteration

**Status:** ✅ COMPLETE
**Duration:** ~25 minutes
**Difficulty:** Intermediate
**Prerequisites:** Notebooks 103-106 (all graph patterns)

#### Learning Objectives

- Create self-referencing edges that loop back to previous nodes
- Implement retry logic with counter-based termination
- Build iteration patterns for pagination, batching, data processing
- Design termination conditions that safely exit loops
- Apply looping workflows to SCM list pagination
- Understand when to use loops vs sequential chains
- Recognize and prevent infinite loop pitfalls

#### Key Concepts Introduced

- **Self-Referencing Edges:** Creating cycles in graphs (node → process → check → back to process)
- **Loop Counters:** Tracking iterations with counter fields in state
- **Termination Conditions:** Maximum iteration limits preventing infinite loops
- **Retry Patterns:** Try operation up to N times before failing
- **Pagination Patterns:** Fetching data in chunks until complete (SCM list APIs)
- **Safety Rules:** Five critical rules for preventing infinite loops
- **Network Analogies:** TCP retransmission, BGP route chunks, IP TTL

#### SCM/Pan-SDK Examples

**Reference:** `docs/examples/address_objects.py` (pagination patterns)

- **API Connection Retry:** Retry SCM API connection up to 3 times
- **Address List Pagination:** Fetch address objects in 200-item pages (simulates real API)
- **HA Status Polling:** Check HA sync status repeatedly until synced
- **Batch Object Creation:** Process list of objects one at a time

#### Code Patterns

```python
from typing import TypedDict, Literal

# State with Loop Counter (REQUIRED!)
class ConnectionRetryState(TypedDict):
    retry_count: int          # Current attempt (starts at 0)
    max_retries: int          # Hard limit
    connected: bool           # Success condition
    result: str

# Processing Node (MUST increment counter!)
def attempt_connection(state: ConnectionRetryState) -> dict:
    new_count = state["retry_count"] + 1  # ⚠️ CRITICAL: Increment!
    success = random.random() < 0.7
    return {"retry_count": new_count, "connected": success}

# Router (CHECK MAX FIRST!)
def should_retry(state: ConnectionRetryState) -> Literal["success", "retry", "max_reached"]:
    # ⚠️ CRITICAL: Check max FIRST!
    if state["retry_count"] >= state["max_retries"]:
        return "max_reached"  # Safety exit
    if state["connected"]:
        return "success"  # Success exit
    return "retry"  # Loop back

# Build Graph with Loop
graph = StateGraph(ConnectionRetryState)
graph.add_node("attempt", attempt_connection)
graph.add_node("check", lambda s: s)

graph.add_edge(START, "attempt")
graph.add_edge("attempt", "check")

graph.add_conditional_edges(
    source="check",
    path=should_retry,
    path_map={
        "success": END,
        "max_reached": END,
        "retry": "attempt"  # ← Loop back!
    }
)

app = graph.compile()
```

#### Hands-On Exercises

1. Build SCM address list pagination workflow
2. Implement retry logic with exponential backoff
3. Create polling workflow for HA sync status
4. Build batch processing with error recovery

#### Dependencies

- **Builds on:** Notebooks 103-106 (all foundational patterns)
- **Required for:** Advanced patterns combining loops with tools (110-111)

---

## Phase 2: LLM Integration (Notebooks 108-111)

### Notebook 108: First LLM Integration (Simple Bot)

**Status:** ✅ COMPLETE
**Duration:** ~30 minutes
**Difficulty:** Intermediate
**Prerequisites:** Notebooks 101-107 (Graph foundations), Anthropic API key

#### Learning Objectives

- Integrate an LLM (Claude) into LangGraph workflows
- Define state structures for handling AI messages
- Initialize and invoke Anthropic models using LangChain
- Build a simple AI bot for PAN-OS firewall queries
- Understand difference between simple bot and conversational agent
- Discover limitations of stateless AI interactions

#### Key Concepts Introduced

- **LangChain + LangGraph Together:** How they complement each other
- **HumanMessage Objects:** Structured representation of user messages
- **ChatAnthropic Integration:** Connecting to Anthropic's Claude API
- **Simple Bot Pattern:** Single-node graph with LLM
- **The invoke() Pattern:** Consistent across LangChain/LangGraph
- **The Memory Problem:** Why simple bots don't remember context

#### SCM/Pan-SDK Examples

- **PAN-OS Query Bot:** Answers questions about firewalls, upgrades, configurations
- **Configuration Queries:** CLI commands, error codes, best practices
- **Upgrade Path Recommendations:** Based on training data, not real-time tool calls

#### Code Patterns

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from typing import TypedDict, List

# State with Messages
class AgentState(TypedDict):
    messages: List[HumanMessage]  # Only human messages (no memory)

# Initialize LLM
llm = ChatAnthropic(model="claude-3-5-haiku-20241022")

# Create Processing Node
def process_query(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = llm.invoke(messages)  # Call the LLM
    print(response.content)
    return state  # ❌ Doesn't save AI response (no memory)

# Build Simple Bot Graph
graph = StateGraph(AgentState)
graph.add_node("process_query", process_query)
graph.add_edge(START, "process_query")
graph.add_edge("process_query", END)
app = graph.compile()

# Use it
app.invoke({"messages": [HumanMessage(content="What is PAN-OS?")]})
```

#### Hands-On Exercises

1. Test bot with various PAN-OS questions
2. Demonstrate the memory problem (two-message test)
3. Build interactive loop with multiple queries
4. Explore cost implications with token counting

#### Dependencies

- **Builds on:** Notebooks 101-107 (graph foundations)
- **Required for:** Notebook 109 (conversational memory builds on this)

---

### Notebook 109: Conversational Memory (Manual Management)

**Status:** ✅ COMPLETE
**Duration:** ~45 minutes
**Difficulty:** Intermediate
**Prerequisites:** Notebook 108 (First LLM Integration)

#### Learning Objectives

- Use both HumanMessage and AIMessage types for conversation tracking
- Implement conversation memory using manual history management
- Understand Union type for handling multiple message types
- Build stateful conversation loop that remembers context
- Learn about conversation persistence (saving to files/databases)
- Discover cost implications of growing conversation history
- Implement conversation history trimming strategies

#### Key Concepts Introduced

- **AIMessage Type:** Representing messages FROM the AI
- **Union Types for Messages:** `Union[HumanMessage, AIMessage]` for mixed lists
- **Manual Memory Management:** Appending AI responses to state manually
- **History Synchronization:** Maintaining conversation_history variable across invocations
- **Conversation Persistence:** JSON files, databases, checkpointing preview
- **Token Cost Growth:** Linear growth problem with conversation length
- **Trimming Strategies:** Window, summarization, smart truncation, token-based

#### SCM/Pan-SDK Examples

- **Multi-Turn Troubleshooting:** Context-aware firewall debugging
- **Configuration Assistance:** Remembering previous configuration details
- **Upgrade Planning:** Maintaining context across multiple questions

#### Code Patterns

```python
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage

# State with Both Message Types
class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]  # BOTH types!

# Node that SAVES AI Response (KEY DIFFERENCE!)
def process_query(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = llm.invoke(messages)
    
    # ⭐ KEY: Append AI response to state
    state["messages"].append(AIMessage(content=response.content))
    print(response.content)
    return state

# External History Management
conversation_history = []

def chat(user_message: str):
    global conversation_history
    
    # Add human message
    conversation_history.append(HumanMessage(content=user_message))
    
    # Invoke agent
    result = agent.invoke({"messages": conversation_history})
    
    # ⭐ CRITICAL: Sync history
    conversation_history = result["messages"]

# Persistence: Save to JSON
def save_conversation(filename="conversation.json"):
    messages_data = [
        {"type": "human" if isinstance(m, HumanMessage) else "ai",
         "content": m.content}
        for m in conversation_history
    ]
    with open(filename, 'w') as f:
        json.dump(messages_data, f, indent=2)

# Trimming: Keep last N messages
def chat_with_trimming(user_message: str, max_history: int = 10):
    conversation_history.append(HumanMessage(content=user_message))
    trimmed_history = conversation_history[-max_history:]  # Trim
    result = agent.invoke({"messages": trimmed_history})
    conversation_history.append(result["messages"][-1])  # Save AI response
```

#### Hands-On Exercises

1. Build multi-turn conversation with context retention
2. Implement JSON persistence and loading
3. Add window trimming with configurable size
4. Calculate token costs for long conversations
5. Build summarization-based trimming

#### Dependencies

- **Builds on:** Notebook 108 (simple bot foundation)
- **Required for:** Notebook 110 (reducers eliminate manual management)

---

### Notebook 110: ReAct Agents with Tools and Reducers

**Status:** ✅ COMPLETE
**Duration:** ~60 minutes
**Difficulty:** Advanced
**Prerequisites:** Notebooks 108-109 (LLM Integration, Memory)

#### Learning Objectives

- Understand ReAct (Reasoning and Acting) agent pattern
- Master `add_messages` reducer for automatic state management
- Learn advanced type annotations: Annotated and Sequence
- Create custom tools for PAN-OS firewall operations
- Build tool-calling agent that makes intelligent decisions
- Implement conditional edges for tool routing
- Understand multiple message types: SystemMessage, ToolMessage, BaseMessage

#### Key Concepts Introduced

- **ReAct Pattern:** Reasoning (LLM decides) + Acting (tools execute) loop
- **Annotated Type:** Adding metadata to type hints
- **Sequence[BaseMessage]:** Ordered collection accepting any message type
- **add_messages Reducer:** Automatic state merging (no manual append!)
- **StructuredTool Pattern:** Converting Python functions to LangGraph tools (stable for notebooks)
- **ToolNode:** Prebuilt node managing all tools
- **BaseMessage Hierarchy:** Parent class for all message types
- **Tool Docstrings:** Critical for LLM tool selection decisions

#### SCM/Pan-SDK Examples

**Reference:** Simulated PAN-OS operations

- **check_panos_version:** Query firewall version (simulates API call)
- **calculate_upgrade_downtime:** Estimate upgrade duration
- **check_upgrade_compatibility:** Validate upgrade path
- **Multi-Step Query:** "Check fw-prod-01's version, then calculate downtime to 11.0.0"

#### Code Patterns

```python
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import StructuredTool

# State with Reducer (THE GAME CHANGER!)
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    #         ^^^^^^^^^           ^^^^^^^^^^^^^  ^^^^^^^^^^^^
    #         Metadata            Any msg type   Auto-append reducer

# Create Tool with StructuredTool (stable for notebooks!)
def _check_panos_version(hostname: str) -> str:
    """
    Check the current PAN-OS version for a given firewall.
    
    Args:
        hostname: The firewall hostname (e.g., 'fw-prod-01')
    
    Returns:
        The current PAN-OS version
    
    Use this when the user asks about current firewall versions.
    """
    versions = {"fw-prod-01": "10.1.0", "fw-prod-02": "10.2.5"}
    return f"Firewall {hostname} is running {versions.get(hostname, 'unknown')}"

check_panos_version = StructuredTool.from_function(
    func=_check_panos_version,
    name="check_panos_version",
    description="Check the current PAN-OS version for a firewall"
)

# Bind Tools to LLM
tools = [check_panos_version]
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
model_with_tools = llm.bind_tools(tools)

# Agent Node (with automatic state management!)
def call_model(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are a PAN-OS expert...")
    messages = [system_prompt] + list(state["messages"])
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}  # Reducer auto-appends!

# Router for Tool Calls
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Build ReAct Graph
from langgraph.prebuilt import ToolNode

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")  # Loop back!
app = graph.compile()
```

#### Hands-On Exercises

1. Add tool to validate IP addresses
2. Create tool for security policy checking
3. Build configuration snippet generator tool
4. Implement error handling in tools
5. Add more PAN-OS operations (NAT, interfaces, routing)

#### Dependencies

- **Builds on:** Notebooks 108-109 (LLM integration, memory)
- **Required for:** Notebook 111 (human-in-the-loop uses tools + reducers)

---

### Notebook 111: Human-in-the-Loop Patterns

**Status:** ✅ COMPLETE
**Duration:** ~45 minutes
**Difficulty:** Advanced
**Prerequisites:** Notebooks 108-110 (LLM integration, tools, reducers)

#### Learning Objectives

- Implement human-in-the-loop patterns for AI collaboration
- Build interactive configuration drafting assistant
- Create tools that modify and save configurations
- Use conditional edges to route between human feedback and completion
- Understand when to end vs. continue collaboration loop
- Apply all LangGraph concepts learned in previous notebooks

#### Key Concepts Introduced

- **Human-in-the-Loop (HITL) Pattern:** Iterative AI-human collaboration workflow
- **Interactive Input in Nodes:** Using `input()` within node functions
- **Tool-Based Routing:** Different tools route to different destinations
- **Global State Management:** Using global variables for shared configuration (learning pattern)
- **Iterative Refinement:** Continuous feedback loop until human approves
- **Approval Workflow:** Human decides when to save and complete

#### SCM/Pan-SDK Examples

- **NAT Policy Drafting:** Create NAT policy, refine zones/addresses, save when approved
- **Configuration Assistant:** Interactive SCM configuration creation and refinement
- **Multi-Turn Collaboration:** "Create NAT policy" → "Change source zone" → "Add description" → "Save it"

#### Code Patterns

```python
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END

# Global Configuration Storage (for learning)
configuration_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Tool 1: Update Configuration (loops back to agent)
def update_configuration_func(content: str) -> str:
    """Update the PAN-OS configuration with provided content."""
    global configuration_content
    configuration_content = content
    return f"Configuration updated:\n{configuration_content}"

update_configuration = StructuredTool.from_function(
    func=update_configuration_func,
    name="update_configuration",
    description="Update the PAN-OS configuration with new content"
)

# Tool 2: Save Configuration (goes to END)
def save_configuration_func(filename: str) -> str:
    """Save configuration to file and finish the process."""
    global configuration_content
    if not filename.endswith('.txt'):
        filename += '.txt'
    with open(filename, 'w') as f:
        f.write(configuration_content)
    return f"Configuration saved to {filename}"

save_configuration = StructuredTool.from_function(
    func=save_configuration_func,
    name="save_configuration",
    description="Save the current configuration to a file and complete the process"
)

# Agent Node with Interactive Input
def call_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content="You are ConfigAssist, a PAN-OS configuration assistant..."
    )
    
    # Prompt user for input
    if not state["messages"]:
        user_input = input("\nWhat config would you like to create?\nYou: ")
    else:
        user_input = input("\nHow to modify?\nYou: ")
    
    user_message = HumanMessage(content=user_input)
    
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    model_with_tools = llm.bind_tools([update_configuration, save_configuration])
    
    messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = model_with_tools.invoke(messages)
    
    print(f"\nAI: {response.content}")
    return {"messages": [user_message, response]}

# Router: Check which tool was called
def should_continue(state: AgentState) -> str:
    """Route based on tool used: save → END, other → agent"""
    for msg in reversed(state["messages"]):
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc["name"] == "save_configuration":
                    return END
            return "agent"
    return "agent"

# Build HITL Graph
graph = StateGraph(AgentState)
graph.add_node("agent", call_agent)
graph.add_node("tools", ToolNode([update_configuration, save_configuration]))
graph.add_edge(START, "agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges("tools", should_continue, {"agent": "agent", END: END})
app = graph.compile()
```

#### Hands-On Exercises

1. Add validation before saving configurations
2. Create configuration templates
3. Build multi-step configuration wizard
4. Add error detection and suggestions
5. Implement configuration versioning

#### Dependencies

- **Builds on:** Notebooks 108-110 (all LLM and tool patterns)
- **Required for:** Production AI agent deployments

---

## Learning Path and Dependencies

### Dependency Graph

```
101: Type Annotations (Foundation for all)
  ↓
102: Core Concepts (State, Nodes, Graphs)
  ↓
103: Your First Graph
  ↓
104: State Management - Complex Data
  ↓
105: Sequential Workflows
  ↓
106: Conditional Routing
  ↓
107: Looping Workflows
  ↓ (Phase 1 Complete - No LLM Required)
  ↓
108: First LLM Integration
  ↓
109: Conversational Memory
  ↓
110: ReAct Agents with Tools
  ↓
111: Human-in-the-Loop
```

### Prerequisites by Notebook

| Notebook | Python Level | LangGraph Experience | API Key Required | Duration |
|----------|-------------|---------------------|------------------|----------|
| 101 | Basic | None | No | ~5 min |
| 102 | Basic | None | No | ~30 min |
| 103 | Basic | None | No | ~20 min |
| 104 | Basic | 101-103 | No | ~20 min |
| 105 | Intermediate | 101-104 | No | ~30 min |
| 106 | Intermediate | 101-105 | No | ~20 min |
| 107 | Intermediate | 101-106 | No | ~25 min |
| 108 | Intermediate | 101-107 | Yes (Anthropic) | ~30 min |
| 109 | Intermediate | 101-108 | Yes (Anthropic) | ~45 min |
| 110 | Advanced | 101-109 | Yes (Anthropic) | ~60 min |
| 111 | Advanced | 101-110 | Yes (Anthropic) | ~45 min |

### Total Time Allocation

- **Beginner Track (101-107):** 8-10 hours
- **Advanced Track (108-111):** 6-8 hours  
- **Complete Workshop:** 14-18 hours for mastery

---

## Teaching Guidelines

### For Each Notebook

**Review Checklist:**

- ✅ Learning objectives clearly stated
- ✅ SCM examples appropriate for complexity level
- ✅ Code patterns match established standards
- ✅ Prerequisites satisfied
- ✅ Hands-on exercises included
- ✅ Progressive complexity maintained

**Code Quality Standards:**

- Use `StructuredTool.from_function()` in notebooks 110-111 (not `@tool` decorator)
- TypedDict for all state definitions
- Anthropic/Claude for all LLM operations
- Comprehensive docstrings
- Production-ready error handling

**SCM Integration Standards:**

- Reference actual `docs/examples/*.py` code
- Use realistic pan-scm-sdk operations
- Match API patterns from SDK
- Include proper exception handling

### Common Pain Points

**Notebook 101:** Students skip TypedDict thinking it's optional

- **Solution:** Emphasize it's CRITICAL for all LangGraph state definitions

**Notebook 102:** Confusion between State, Node, and Graph

- **Solution:** Use SCM workflow analogy (data = state, step = node, playbook = graph)

**Notebook 106:** Forgetting `lambda state: state` for router nodes

- **Solution:** Emphasize this is ALWAYS required for router nodes

**Notebook 107:** Infinite loops due to missing counter checks

- **Solution:** Teach the 5 safety rules BEFORE building loops

**Notebook 109:** Forgetting to sync conversation_history

- **Solution:** Show what happens when you forget (context loss)

**Notebook 110:** Tool docstrings not detailed enough

- **Solution:** Show LLM decision-making relies on docstrings

---

## Appendices

### Appendix A: Key Patterns Summary

**1. Basic Graph (103)**

```python
graph = StateGraph(State)
graph.add_node("process", process_function)
graph.add_edge(START, "process")
graph.add_edge("process", END)
app = graph.compile()
```

**2. Sequential Pipeline (105)**

```python
graph.add_edge(START, "validate")
graph.add_edge("validate", "create")
graph.add_edge("create", "verify")
graph.add_edge("verify", END)
```

**3. Conditional Routing (106)**

```python
graph.add_node("router", lambda state: state)
graph.add_conditional_edges(
    source="router",
    path=router_function,
    path_map={"path_a": "node_a", "path_b": "node_b"}
)
```

**4. Looping (107)**

```python
def should_continue(state) -> Literal["loop", "exit"]:
    if state["counter"] >= state["max"]:
        return "exit"  # Safety!
    return "loop"

graph.add_conditional_edges("check", should_continue,
    {"loop": "process", "exit": END})
```

**5. ReAct Agent (110)**

```python
messages: Annotated[Sequence[BaseMessage], add_messages]

def _my_tool(param: str) -> str:
    """Docstring critical for LLM!"""
    return result

my_tool = StructuredTool.from_function(
    func=_my_tool,
    name="my_tool",
    description="Clear description for LLM"
)

model_with_tools = llm.bind_tools([my_tool])
```

**6. Human-in-the-Loop (111)**

```python
def should_continue(state):
    if save_tool_called:
        return END
    return "agent"  # Continue feedback loop
```

### Appendix B: SCM SDK Reference

**Common Operations from `docs/examples/`:**

**Address Objects** (`address_objects.py`):

- Create: IP/netmask, FQDN, IP range
- Fetch by name and folder
- Update existing objects
- List with filtering
- Delete by ID

**Address Groups** (`address_groups.py`):

- Create static/dynamic groups
- Update membership
- List with filters

**Security Policies** (`security_policy.py`):

- Create allow/deny/drop rules
- Configure security profiles
- Rule positioning
- List with filters

**NAT Policies** (`nat_policy.py`):

- Source NAT (dynamic/static)
- Destination NAT
- Bulk operations

### Appendix C: Workshop Delivery

**Self-Paced:** 4-5 hours, complete notebooks independently

**Instructor-Led (1 day):**

- 09:00-12:00: Notebooks 101-105 (Foundations)
- 13:00-17:00: Notebooks 106-111 (Advanced + LLM)

**Multi-Day Deep Dive (3 days):**

- Day 1: Foundations (101-104)
- Day 2: Agents and Tools (105-107)
- Day 3: Advanced Topics (108-111) + Capstone

---

## Summary

This workshop provides a complete learning path from Python type annotations to advanced AI agents for Strata Cloud Manager automation.

**Workshop Strengths:**

- ✅ All 11 notebooks complete and tested
- ✅ Progressive complexity from beginner to advanced
- ✅ Real-world SCM automation focus
- ✅ Hands-on exercises in every notebook
- ✅ Production-ready patterns throughout
- ✅ Clear prerequisite dependencies

**Learning Outcomes:**
After completion, network security engineers can:

1. Design TypedDict schemas for complex configurations
2. Build stateful workflows with LangGraph
3. Integrate Claude LLM for natural language interfaces
4. Implement memory and state management
5. Create tools that interact with SCM API
6. Build autonomous ReAct agents
7. Implement human-in-the-loop patterns
8. Deploy production-ready AI agents

**Status:** Ready for delivery! All notebooks complete.
