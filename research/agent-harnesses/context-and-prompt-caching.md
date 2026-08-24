---
doc_kind: research
canonical_id: context-and-prompt-caching-research
purpose: [research]
rank: high
topics: [context, prompt-caching, markdown, xml, templatability, headroom, ast-grep]
---

# Context layering, prompt caching, and harness modularity

Research on LLM ingestion formats, prompt caching optimization across frontier models, 3-tier cost layers, and modular harness decoupling.

## 1. Information and documentation formats for LLMs

### Comparative analysis

- **Pure Markdown**: Lowest token overhead (1.00x), but prone to delimiter collisions and instruction bleed.
- **Pure XML Tags**: Highest boundary isolation and prompt injection resilience (+5% to +12% tokens).
- **YAML Frontmatter**: Native standard parsing via ast-grep without parsing file bodies.
- **Hybrid Structured Format** (YAML Frontmatter + XML Outer Tags + Markdown Inner Body): Optimal balance. Yields highest instruction adherence (>40% reduction in instruction drift) with minimal token overhead (+2% to +4%).

### Hybrid Structured Format for AGENTS.md and SKILL.md

Standardizing on YAML header + XML semantic tags (purpose, critical_constraints, execution_workflow, security_enforcement) eliminates delimiter ambiguity and enables instant AST filtering via st-grep.

## 2. Prompt caching and 5-Tier Ordered Context Hierarchy

Frontier models (Claude 3.5/3.7, Gemini 1.5/2.0/3.0, GPT-4o) rely on exact byte prefix matching for prompt caching.

### The 5-Tier Ordered Context Hierarchy (Target: 92-98% Cache Hits)

1. **Layer 1: Universal System Instructions & Critical MUSTs** (100% static across all sessions).
2. **Layer 2: Semi-Static Catalogs & Tool Schemas** (`skill-dispatch.md`, agent cards, tool schemas) [Cache Breakpoint 1].
3. **Layer 3: Monotonic Conversation History** (Turns 1 to N-1, append-only) [Cache Breakpoint 2].
4. **Layer 4: JIT Area Rules & Scoped Constraints** (nearest folder `AGENTS.md` injected dynamically at the turn tail).
5. **Layer 5: Dynamic Turn Delta** (Latest user prompt, current tool output compressed via Headroom).

> [!IMPORTANT]
> **Cache Invalidation Prevention**: Placing JIT Area Rules (Layer 4) in the dynamic turn tail rather than ahead of Conversation History (Layer 3) ensures that mid-session navigation between repository directories never invalidates the prefix cache of prior conversation turns.

### Cache anti-patterns and solutions

- **JIT rules ahead of history**: Invalidate history cache upon folder navigation. Solved by injecting JIT rules into the dynamic turn tail.
- **Dynamic timestamps in system prompt**: Invalidate entire cache. Move timestamps to Layer 5 or on-demand tool.
- **Unsorted dictionaries**: Enforce `json.dumps(obj, sort_keys=True)` across all schema generators.
- **In-place history rewriting**: Use monotonic append-only history; Headroom coding profile preserves prior turns byte-for-byte.

## 3. Cost layers: ai-router 3-Tier Layer vs alternatives

### Measured performance in ai-router

- **ast-grep Outline**: 93.6% token reduction on Python source files; 83.3% on JSON agent cards; 94.5% on YAML frontmatter.
- **Headroom Compression**: 72.2% token savings on JSON arrays; 30.8% on build/compiler logs; 0% loss of structural facts.
- **qmd BM25 Retrieval**: 0.895s average search latency with top-1 precision on distinctive tokens.

### Blind spots and upgrades

- **Blind spot**: Lack of ambient cross-file symbol call graphs (Aider Tree-sitter PageRank).
- **Upgrade path**: Add a lightweight, cached cross-reference index (compact symbol map) without paying a permanent per-turn token tax.

## 4. Harness modularity and templatability (ai-harness-core)

Decouple the system into three distinct layers:

1. **Tier 1: Core Harness Engine (.harness/)**: Generic routing, worktree isolation, retrieval adapters (qmd/ast-grep), Headroom compression proxy client, prompt cache manager, A2A protocol.
2. **Tier 2: Declarative Manifests (config/)**: reas.yaml, model-tiers.yaml, sgconfig.yml, harness.config.json.
3. **Tier 3: Domain Assets (i-tooling/, docs/, scripts/)**: Repo-specific skills, agents, standards, and automation scripts.

Allows scaffolding any new codebase via a single CLI invocation: python .harness/cli/harness_init.py.
