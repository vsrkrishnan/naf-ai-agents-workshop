# Workshop Plan: LangGraph for Network Automation

**Duration:** 4 hours (fast paced)
**Format:** Instructor-led with demos, hands-on for key concepts, full materials for post-workshop self-study
**Target:** Network security engineers, Python basics assumed

---

## Overview

Fast-paced introduction to building AI agents for network automation using LangGraph and Palo Alto Networks SCM. Core concepts covered in session; attendees continue with complete notebook series afterward.

**Phase 1:** LangGraph foundations (no API key)
**Phase 2:** LLM integration with Claude AI
**Post-workshop:** Full 11-notebook series for self-study

---

## Workshop Flow & Timing

### Session 1: Foundations (0:00-2:00, 120 min)

**0:00-0:15 (15 min) - Welcome & Setup**

- Workshop overview and objectives
- **Codespaces users:** Open Codespace (ready in 2 min)
- **Local users:** Verify Python/Jupyter installations
- Quick environment check (Jupyter Lab access)
- Set expectations: fast pace, materials for later
- Note: Codespaces significantly reduces setup time

**0:15-0:35 (20 min) - Type Annotations & State (NB 101-102)**

- **Topics:** TypedDict, state schemas, graph basics
- **Activity:** Live code demo with SCM address objects
- **Key concept:** State is everything in LangGraph
- **Hands-on:** Quick lab - define state schema

**0:35-0:55 (20 min) - Building Graphs (NB 103-104)**

- **Topics:** Nodes, edges, compilation, execution
- **Activity:** Build first graph together (address validation)
- **Key concept:** Nodes are functions, edges control flow
- **Hands-on:** Create and run simple graph

**0:55-1:20 (25 min) - Sequential & Conditional (NB 105-106)**

- **Topics:** Multi-node pipelines, conditional routing
- **Activity:** Demo tag→address→group workflow
- **Activity:** Demo folder-based routing (prod/dev)
- **Key concept:** add_edge() vs add_conditional_edges()
- **Hands-on:** Add conditional logic to existing graph

**1:20-1:50 (30 min) - Looping & Patterns (NB 107)**

- **Topics:** Self-referencing edges, retry logic, pagination
- **Activity:** Build HA polling workflow
- **Activity:** API pagination pattern
- **Key concept:** Loop counters prevent infinite loops
- **Hands-on:** Implement retry logic
- **Phase 1 wrap:** Attendees can build production workflows without AI

**1:50-2:00 (10 min) - Phase 1 Q&A**

- Questions on foundations
- Preview Phase 2
- Mention: All Phase 1 notebooks available for deep dive

**2:00-2:15 (15 min) - BREAK**

- Obtain Anthropic API keys if needed
- Configure .env files
- Stretch, coffee, networking

---

### Session 2: LLM Integration (2:15-3:45, 90 min)

**2:15-2:30 (15 min) - First LLM Integration (NB 108)**

- **Topics:** Claude API, ChatAnthropic, messages
- **Activity:** Build simple PAN-OS query bot
- **Key concept:** llm.invoke() with HumanMessage
- **Demo:** Live API calls (~$0.01)
- **Quick hands-on:** Modify bot prompt

**2:30-2:50 (20 min) - Conversational Memory (NB 109)**

- **Topics:** Message history, AIMessage, multi-turn
- **Activity:** Build troubleshooting bot with context
- **Key concept:** State holds conversation history
- **Demo:** Memory in action
- **Discussion:** When to use memory vs. stateless

**2:50-3:25 (35 min) - ReAct Agents & Tools (NB 110)**

- **Topics:** add_messages reducer, StructuredTool, tool calling
- **Activity:** Build agent with SCM CRUD operations
- **Key concept:** LLM decides when to call tools
- **Demo:** Agent reasoning through address creation
- **Hands-on (time permitting):** Add custom tool
- **Discussion:** Tool design best practices

**3:25-3:40 (15 min) - Human-in-the-Loop (NB 111)**

- **Topics:** Approval workflows, interrupt patterns
- **Activity:** Demo NAT policy drafting with approval
- **Key concept:** Differential routing (tools vs. human)
- **Demo:** Interactive workflow
- **Discussion:** Production deployment patterns

**3:40-3:45 (5 min) - Phase 2 Wrap**

- Recap: From simple bot to production agent
- All notebooks available for exploration

---

### Wrap-Up (3:45-4:00, 15 min)

**3:45-3:55 (10 min) - Next Steps & Resources**

- **What you learned:** Core LangGraph patterns, AI integration
- **Continue learning:** 11 notebooks for deep study
- **Keep using Codespaces:** Your fork remains available for continued learning
- **Resources:**
  - `/summaries` - Quick references
  - `/docs/examples` - Production code
  - `.devcontainer` - Codespaces configuration for your projects
- **Capstone ideas:** Build your own SCM automation agent
- **Community:** GitHub issues/discussions

**3:55-4:00 (5 min) - Final Q&A**

- Open questions
- Workshop feedback
- Instructor contact for follow-up

---

## Break Schedule

**Scheduled:** 2:00-2:15 (15 min) between Phase 1 and Phase 2
**Flexible:** Instructor may add 5-min micro-breaks as needed based on pace

---

## Activities Summary

### Hands-On Labs (Attendees Code)

1. Define state schema (NB 101-102)
2. Build first graph (NB 103-104)
3. Add conditional routing (NB 106)
4. Implement retry logic (NB 107)
5. Modify bot prompt (NB 108)
6. Add custom tool (NB 110, time permitting)

### Instructor Demos (Attendees Observe)

1. Address validation workflow (NB 103)
2. Tag→address→group pipeline (NB 105)
3. Folder routing (NB 106)
4. HA polling (NB 107)
5. PAN-OS query bot (NB 108)
6. Memory troubleshooting bot (NB 109)
7. ReAct agent reasoning (NB 110)
8. NAT policy approval workflow (NB 111)

### Discussions

1. Phase 1 wrap - production workflows
2. When to use memory
3. Tool design best practices
4. Production deployment patterns

---

## Key Topics Covered

### Phase 1: Foundations

- Python type annotations (TypedDict, Union, Optional)
- LangGraph architecture (state, nodes, edges, graphs)
- State management and schemas
- Sequential workflows (add_edge)
- Conditional routing (add_conditional_edges)
- Looping patterns (self-referencing edges)
- Production patterns (error handling, retries, pagination)

### Phase 2: LLM Integration

- Claude API integration (ChatAnthropic)
- Message types (HumanMessage, AIMessage)
- Conversational memory management
- add_messages reducer pattern
- StructuredTool creation
- ReAct agent architecture
- Tool calling and reasoning
- Human-in-the-loop workflows
- Interactive approval patterns

### Cross-Cutting

- Palo Alto Networks SCM objects (addresses, rules, NAT policies, tags, groups)
- pan-scm-sdk patterns
- Error handling and validation
- Testing and debugging workflows
- Cost management for LLMs
- Observability (LangSmith optional)

---

## Materials Provided

**Pre-workshop:**

- Repository URL for forking
- GitHub Codespaces configuration (.devcontainer)
- .env.template
- WORKSHOP_FAQ.md with setup instructions

**During workshop:**

- Pre-configured cloud environment (Codespaces)
- Live coding examples
- Instructor solutions
- Real-time Q&A

**Post-workshop:**

- Complete 11-notebook series
- Markdown summaries (/summaries)
- Production examples (/docs/examples)
- Reusable code patterns (/src)

---

## Prerequisites

**Required (All attendees):**

- GitHub account (free)
- Stable internet connection
- Web browser

**Setup Option A - Codespaces (Recommended):**

- Just GitHub account + browser
- Zero local installation
- Works on any device
- Free tier: 60 hours/month

**Setup Option B - Local (Optional):**

- Python 3.11+
- Laptop with terminal access
- Text editor/IDE
- Git installed

**For Phase 2 (during workshop):**

- Anthropic API key (~$1 cost)
- Or observe instructor demos

**Knowledge:**

- Basic Python (functions, dicts)
- Network security concepts
- NO prior LangGraph/AI experience needed

---

## Success Criteria

**By end of workshop, attendees can:**

1. Build LangGraph state machines for automation
2. Design sequential and conditional workflows
3. Implement looping/retry patterns
4. Integrate Claude AI into graphs
5. Create tools for agent use
6. Understand production deployment patterns
7. Continue learning with full notebook series

**Post-workshop goals:**

- Complete all 11 notebooks independently
- Build custom AI automation agents
- Deploy production workflows

---

## Logistics Notes

**Pace:** Intensive - covers highlights of 14-18 hour curriculum in 4 hours
**Philosophy:** Foundation in session, mastery through self-study
**Setup:** GitHub Codespaces recommended for zero-install experience
**Support:** Instructor available post-workshop via GitHub/email
**API Costs:** ~$1 for Phase 2 demos (optional for attendees)
**Internet:** Required for Codespaces and API calls
**Codespaces:** Free tier sufficient (60 hrs/month, ~4 hrs used)
**Recording:** Check with organizers re: recording policy
**Accessibility:** Codespaces works on any device with browser
