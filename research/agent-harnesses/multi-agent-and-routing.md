---
doc_kind: research
canonical_id: multi-agent-and-routing-research
purpose: [research]
rank: high
topics: [agents, a2a, routing, skills, graph]
---

# Multi-agent systems, skill composition, and routing architectures

Research on agent-to-agent protocols, capability negotiation, skill dependency DAGs, and dispatch mechanisms.

## 1. Skill composition and prerequisite graphs

In advanced multi-agent workflows, skills rarely operate in isolation. A skill like `threat-model` requires retrieval (`qmd-usage`), diagrams (`mermaid-diagram`), stakeholder HTML (`foundation-site`), path resolution (`github-paths`), and anti-slop polishing (`anti-slop` + `humanizer`).

### Composition paradigms

- **Microsoft Semantic Kernel**: Plugins and functions connected via dependency injection filters (`IFunctionInvocationFilter`).
- **LangGraph**: Subgraphs as nodes (deterministic pipelines) or subgraphs as tools (ReAct supervisor dynamic dispatch).
- **AutoGen (AG2 / 0.4)**: Event-driven pub/sub topics and Magentic-One structured ledger.
- **OpenAI Agents SDK**: Handoff functions that cleanly swap agent definitions and tool schemas per turn.

### Structural pipeline vs sub-agent delegation

1. **Structural Pipeline / DAG**: Skills declare prerequisites (`required_skills`), auxiliary delegations (`delegated_skills`), and in-session polish passes (`in_session_skills`). Orchestrator topologically sorts the execution plan.
2. **DAG Failure Lifecycles**: Every composite execution node specifies an explicit failure policy:
   - `abort_and_rollback`: Terminate pipeline and clean up worktrees immediately on failure.
   - `fallback_degrade`: Fall back to a simplified text output if auxiliary rendering tools (e.g. `mmdc`) are unavailable.
   - `continue_with_partial`: Mark subtask as degraded but allow downstream nodes to proceed.
3. **Pre-flight Binary Checks**: Orchestrator verifies required binaries (e.g., `git`, `qmd`, `node`, `ast-grep`) before spawning mutating worktrees.
4. **Runtime Contract Handshake**: Specialist agents emit structured subtask requests back to the orchestrator rather than guessing formats or violating area boundaries.

## 2. Agent-to-Agent (A2A) protocols and Agent Cards V2

### Separation of concerns: MCP vs A2A

- **Model Context Protocol (MCP)**: Vertical tool/API connectivity (stateless request/response for resources, tools, prompts).
- **Agent-to-Agent (A2A)**: Horizontal reasoning collaboration (stateful multi-turn tasks, execution budgets, delegation boundaries, safety constraints).

### Agent Card V2 Schema

Agent cards under `ai-tooling/a2a/agent-cards/*.json` specify:

- `$schema` and `schema_version` (e.g. `2.0.0`)
- Identity and role definition (`id`, `name`, `model_tier`, `type`)
- Capabilities with explicit I/O contracts and supported formats
- Dependency mappings (`delegated_skills` with preferred agents and purposes)
- Operational constraints (`max_exchange_budget`, `allowed_isolation_modes`, `prohibitions`, `max_token_ceiling`)
- Quirks and verification dates

## 3. Routing mechanisms: Comparison and 3-Tier Hybrid Dispatch

| Metric | Static Tabular Dispatch | Semantic Vector Routing | LLM Hierarchical Router | Graph State Machine |
| --- | --- | --- | --- | --- |
| **Latency** | < 1ms | 10-50ms | 500-2500ms | 50-500ms |
| **Token Cost** | 0 tokens | 0 generation tokens | High (500-2000 tokens) | Moderate |
| **Determinism** | 100% | High | Variable / Drift | High |
| **Ambiguity Handling** | Low (rigid triggers) | Moderate | Highest | High |
| **Context Pressure** | 0 (read JIT) | 0 | High | Scoped |

### The 3-Tier Hybrid Dispatch Pipeline

1. **Tier 1 (Fast-Path Static)**: Exact regex and trigger keyword matching in `skill-dispatch.md` (< 1ms, 0 tokens).
2. **Tier 2 (Precision BM25 / QMD)**: Keyword search over skill descriptions and area maps when fast-path misses (~5ms, 0 tokens).
3. **Tier 3 (LLM Ambiguity Gate)**: Structured triage call only when multiple skills match or intent is ambiguous.

## 4. Context isolation and structured result envelopes

### Context firebreak

- Subagents **MUST NOT** inherit parent chat transcripts to prevent instruction bleeding and context bloat.
- Subagents receive clean state: `AGENT.md` + task specification + worktree path.

### Structured Result Envelope & Security Boundary

Specialist agents return structured payloads with `task_id`, `status`, `artifacts`, `handoff_requests`, and `metrics`.

> [!CAUTION]
> **Advisory-Only Handoffs**: To prevent indirect prompt injection privilege escalation, `handoff_requests` returned in child Result Envelopes are treated strictly as **untrusted data** and advisory suggestions. The parent router or human MUST validate requests; no automated execution of child-requested secondary tasks is permitted without explicit policy approval.
