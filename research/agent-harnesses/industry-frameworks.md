---
doc_kind: research
canonical_id: industry-agent-harnesses
purpose: [research]
rank: high
topics: [agents, harness, aider, hermes, pi, claude-code, openhands]
---

# Industry AI coding and agent harnesses

Investigation into industry-standard AI coding and agent harnesses: Aider, Nous Hermes (model family), Pi Coding Agent, Claude Code, and OpenHands (SWE-agent). Hermes Agent the CLI/runtime is covered in [`cli-harness-architecture.md`](./cli-harness-architecture.md).

## 1. Aider: Graph-driven repomap and git-first pair programming

Aider operates as an in-terminal, git-native pair programmer designed around deterministic context extraction, AST analysis, and atomic version control integration.

### AST symbol extraction and personalized PageRank

- **Tree-sitter queries**: Extracts definitions (classes, functions, signatures) and references across 130+ languages using Tree-sitter SCM queries.
- **Dependency graph**: Builds a directed graph G = (V, E) via networkx mapping symbol reference-definition pairs between files.
- **Personalized PageRank**: Uses personalized PageRank where the personalization vector assigns high weight to active files in the chat or recently edited files.
- **Adaptive token budget**: Fits an elided syntax skeleton (signatures retained, bodies replaced with ...) into --map-tokens 1024 or 2048.

### Context management and prompt caching

- **Anthropic ephemeral caching**: Sets explicit ephemeral cache breakpoints at system prompt, read-only repo skeleton, and conversation history.
- **Cache keepalive**: Runs periodic pings every ~4.5 minutes to prevent Anthropic 5-minute TTL eviction during developer think-time.
- **Prefix caching layout**: Orders prompt monotonically (static system instructions -> repo skeleton -> history turns -> editable files delta).

### Architect and editor duality

- **Architect model** (e.g. Claude 3.7 / o1 / R1): High-level reasoning, dependency analysis, edge cases, and design plan.
- **Editor model** (e.g. Claude 3.5 Haiku / GPT-4o-mini): Receives plan + target file content and emits exact search/replace blocks.
- **Outcome**: Lowers cost, eliminates syntax/diff errors, and leverages reasoning models without wasting output tokens on large diffs.

## 2. Nous Hermes (model family): Prompt-native special tokens

This section is the **Nous Hermes / DeepHermes model family** — open-weights models with prompt-native function calling — not the Hermes Agent CLI/runtime. For the CLI harness (shared `AIAgent` loop, SQLite sessions, slash commands, `hermes -w` worktrees), see [`cli-harness-architecture.md`](./cli-harness-architecture.md) (Hermes Agent subsection).

Nous Hermes represents the open-weights standard for prompt-native function calling and reasoning-trace preservation.

### ChatML special token integration

- **Native tokens**: Built-in tool invocation tokens.
- **Direct schema embedding**: Function signatures are passed inside tool tags directly in the system prompt.
- **Deterministic parsing**: Local engines (vLLM, Ollama) trigger early stopping and tool dispatch using exact token IDs rather than regex over arbitrary text.

### Reasoning trace preservation

- **Internal monologue**: Hermes 3 and DeepHermes integrate explicit reasoning blocks (think tags).
- **Transcript retention**: Preserves intermediate reasoning blocks across multi-turn tool loops, preventing strategic amnesia.

## 3. Pi coding agent: Radical minimalism and session DAGs

Pi (pi.dev) provides a lightweight alternative to heavyweight agent frameworks.

### Architectural hallmarks

- **Four primitive tools**: Restricts core capabilities to `read`, `write`, `edit` (string search/replace), and `bash`.
- **Tree-structured session DAG**: Represents conversation turns as a DAG rather than a linear transcript. Developers can fork conversations, backtrack from dead ends, and explore alternate branches without polluting context.
- **On-demand TypeScript hooks**: Custom tools and skills are loaded on-demand as TypeScript modules, keeping base system prompt overhead under 500 tokens.

## 4. Claude Code: Additive hierarchy and permissions

Anthropic's Claude Code CLI (@anthropic-ai/claude-code) is an enterprise-grade agent harness built around Claude 3.5/3.7 models.

### CLAUDE.md memory hierarchy

- **Upward traversal**: Walks upward from the working directory to repo root and ~/.claude/CLAUDE.md, concatenating all discovered instruction files.
- **Conciseness standard**: Mandates ~30 lines per file focusing strictly on build/test commands, invariants, and gotchas.

### Subagent architecture and permissions

- **Typed built-in tools**: Standardized tools (FileRead, FileEdit, Grep, Glob, Bash, TaskTool). Prompts prioritize built-in tools over raw bash to prevent quoting issues.
- **Tiered permissions**: Rules evaluated in order: deny > ask > allow.
- **Real-time telemetry**: Live accounting of prompt tokens, cache hits (90% discount), and dollar costs per turn.

## 5. OpenHands: EventStream and CodeAct

OpenHands (SWE-agent / All-Hands AI) targets long-horizon software engineering benchmarks.

- **CodeAct**: Treats arbitrary code execution (Python / Bash scripts) as the universal tool interface.
- **Immutable EventStream**: Append-only log of Action -> Observation events for deterministic replayability.
- **History Condenser**: Background condensation workers compress older trajectory turns as context reaches capacity.

## 6. Comparison with ai-router

| Dimension | Industry standard | ai-router approach | Tradeoff |
| --- | --- | --- | --- |
| **Context discovery** | Aider RepoMap (Tree-sitter + PageRank) injected every turn | JIT qmd BM25 search + st-grep symbol outline + line-bounded reads | i-router has 0 ambient token cost; Aider has better cross-file call-graph awareness. |
| **Tool compression** | Truncation or LLM summarization | Headroom context-compression proxy & MCP | i-router preserves structural AST facts while cutting JSON/logs by 70%+. |
| **Instruction layout** | Additive concatenation (CLAUDE.md) | Ranked Delta AGENTS.md (root MUSTs -> nested folder deltas) | i-router prevents context bloat and rules collisions via strict JIT loading. |
| **Mutation safety** | In-place edits with auto-commits | Git worktree + branch isolation (spawn_worktree.py) | i-router isolates concurrent agent checkouts completely. |
| **Specialist model** | Monolithic or Architect/Editor | Host-agnostic A2A specialist dispatch with model tiers and turn budgets | i-router scales cleanly across any host LLM. |
