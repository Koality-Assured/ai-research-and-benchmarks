---
title: "Local Models: Frontier-to-Local Deferral Architecture & Harness Integration"
status: active
topics: [local-models, deferral-architecture, harness, harness-cli, frontier-agents, a2a, cost-layers]
date: 2026-10-09
---

# Local Models: Frontier-to-Local Deferral Architecture & Harness Integration

Architectural specification for enabling frontier coding agents (Gemini 3 Flash/Pro, Claude 3.7 Sonnet, GPT-4o/5) to defer bounded, mechanical, or high-volume tasks to locally served models via the Harness control plane and Harness CLI.

---

## 1. Problem Statement & Economics

Frontier model APIs (Claude 3.7 Sonnet, GPT-4o, Gemini 3 Pro) are expensive ($2.50–$15.00 per 1M output tokens) and subject to strict rolling window rate limits (`RESOURCE_EXHAUSTED` / 429 errors). Autonomous agent sessions frequently expend thousands of frontier tokens on trivial, deterministic, or bulky operations:
- Fixing markdownlint or formatting violations across 20 files.
- Generating unit test skeletons and boilerplate mocks.
- Synthesizing commit messages conforming to Conventional Commits.
- Distilling 500-line test failure outputs or OWASP Noir scan logs into structured JSON facts.

Expending frontier reasoning budgets on these tasks creates unnecessary API spend and exhausts token windows. Deferring this work to locally served models (75–120+ tok/s at **$0.00 marginal cost**) preserves cloud quotas for high-leverage architectural orchestration.

---

## 2. Work Taxonomy & Deferral Suitability Matrix

Tasks are classified into three operational categories:

| Work Category | Typical Tasks | Optimal Execution Model | Recommended Model |
| :--- | :--- | :--- | :--- |
| **Category 0: System 1 Decision & Triage** *(Instant Sub-50ms)* | Fast skill dispatch, mutation/isolation gating, intent classification, prompt-injection screening, tool output sanitization, deferral tier selection. | **Local System 1 Engine** (Non-autoregressive forward pass) | Laya (ModernBERT-large 421M) / ModernBERT-base (149M) |
| **Category 1: Frontier Orchestration** *(Do Not Defer)* | System design, cross-repo planning, security threat modeling (STRIDE), ambiguous requirement alignment, complex PR synthesis. | **Frontier Agent** (Parent orchestrator) | Claude 3.7 Sonnet / Gemini 3.8 Pro / GPT-5 |
| **Category 2: Bounded Autonomous Coding** *(Optional Deferral)* | Function implementation from detailed spec, single-file refactoring, writing complex algorithms, AST structure queries. | **Frontier OR Local Workhorse** | Qwen 2.5 Coder 14B (Q4_K_M) or Frontier Standard |
| **Category 3: Mechanical & High-Volume** *(Mandatory Deferral)* | Markdown linting fixes, docstring generation, boilerplate test cases, log summarization, JSON schema extraction, commit message drafting. | **Local Model** (Zero-cost worker) | Qwen 2.5 Coder 7B / 14B |
| **Category 4: Quota Fallback** *(Resilience Deferral)* | Secondary model exhaustion (429 recovery), offline air-gapped development, network degradation. | **Local Model** (Automatic failover) | Qwen 2.5 Coder 14B / 32B |

---

## 3. Deferral Mechanism & Interaction Flows

### 3.1 Architecture Overview

```text
+-----------------------------------------------------------------------------------------+
|                                  FRONTIER ORCHESTRATOR                                  |
|                 (Claude 3.7 Sonnet / Gemini 3.8 Flash / GPT-5 in Antigravity)           |
+-----------------------------------------------------------------------------------------+
       |                                                                           |
       | 1. High-level architecture,                                               | 2. Mechanical task
       |    planning, and verification                                             |    identified
       v                                                                           v
+-----------------------------+                             +-----------------------------+
|    Parent Context Window    |                             |      Harness CLI Deferral   |
|    (Cloud Frontier Model)   |                             |   `harness chat --provider  |
|                             |                             |    local -q "..."`          |
+-----------------------------+                             +-----------------------------+
                                                                           |
                                                                           v
                                                            +-----------------------------+
                                                            |   Local Model Runtime       |
                                                            |   (Ollama / llama-server    |
                                                            |    at 127.0.0.1:11434/v1)   |
                                                            |   Model: Qwen 2.5 Coder 14B |
                                                            +-----------------------------+
                                                                           |
                                                                           | 3. Execution:
                                                                           |    75-120 tok/s
                                                                           |    Zero cloud cost
                                                                           v
                                                            +-----------------------------+
                                                            | Structured Result Payload   |
                                                            | (Code Diff / JSON / Patch)  |
                                                            +-----------------------------+
                                                                           |
                                                                           v
                                                            +-----------------------------+
                                                            | Frontier Agent Validates    |
                                                            | & Integrates Patch          |
                                                            +-----------------------------+
```

### 3.2 Invocation Methods for Frontier Agents

Frontier agents can defer work through three distinct integration interfaces:

1. **Direct Shell / CLI Pipeline**:
   The frontier agent calls the Harness CLI via its standard command execution tool:
   ```bash
   harness chat --provider local --model qwen2.5-coder:14b -q "Fix markdownlint violations in this file: $(cat doc.md)"
   ```
2. **Harness Python Provider Client**:
   Within Python scripts or subagents, importing `cli.provider_client`:
   ```python
   from cli.provider_client import complete_result

   result = complete_result(
       provider="local",
       model="qwen2.5-coder:14b",
       messages=[{"role": "user", "content": prompt}],
       api_key="local",
   )
   print(result.text)
   ```
3. **Subagent Delegation (`invoke_subagent`)**:
   Invoking a dedicated subagent configured with `model_tier: local` (or host-local equivalent):
   ```python
   invoke_subagent(
       Role="Mechanical Code Worker",
       TypeName="self",
       Prompt="Run markdownlint auto-fix on docs/standards/ using local model.",
   )
   ```

---

## 4. Control Plane Configuration & Schema Updates

### 4.1 `config/harness.config.json` Extensions

Add the `local_model` configuration block under `adapters`:

```json
{
  "adapters": {
    "local_model": {
      "enabled": true,
      "provider": "local",
      "runtime": "ollama",
      "base_url": "http://127.0.0.1:11434/v1",
      "default_model": "qwen2.5-coder:14b",
      "fast_model": "qwen2.5-coder:7b",
      "reasoning_model": "deepseek-r1:14b",
      "timeout_sec": 120,
      "max_parallel_slots": 4
    }
  }
}
```

### 4.2 `scripts/cli/provider_client.py` Extensions

1. **Provider Registry**:
   - Add `"local"` to `SUPPORTED_PROVIDERS: tuple[str, ...] = ("anthropic", "openai", "gemini", "cursor", "local")`.
   - Add aliases: `"local": "local"`, `"ollama": "local"`, `"llamacpp": "local"`, `"llama-server": "local"`.
2. **Base URL Resolution**:
   - Environment variable: `HARNESS_LOCAL_BASE_URL` (default: `http://127.0.0.1:11434/v1`).
   - If `provider == "local"`, route requests to `{HARNESS_LOCAL_BASE_URL}/chat/completions` using the OpenAI-compatible JSON and SSE parser.
3. **Authentication Exemption**:
   - When `provider == "local"`, bypass external API key verification and default to a local token header (`Authorization: Bearer local`).

### 4.3 Model Tiers Mapping (`ai-tooling/agents/model-tiers.md`)

Update the model tiers catalog to document `tier: local`:

| Tier | Reasoning | Host Examples | Cloud Cost | Primary Use |
| :--- | :--- | :--- | :--- | :--- |
| `local` | mid / high | Qwen 2.5 Coder 14B / 7B | **$0.00** | Mechanical transformations, linting, docstrings, boilerplate, offline fallback |
| `fast` | low | Claude Haiku / Gemini Flash Lite / Qwen 7B | <$0.15/1M | Quick classifications, leaf subagent search |
| `standard`| mid | Gemini 3.8 Flash / Claude Sonnet / Qwen 32B | ~$0.50-$3.00/1M | General coding, PR creation, tool orchestration |
| `high` | high | Claude 3.7 Sonnet / Gemini 3.8 Pro / R1-14B | ~$3.00-$15.00/1M| Deep research, architectural refactors, adversarial review |
| `max` | max | GPT-5 / Claude Opus / Gemini Ultra | Premium | Strategic mission-critical alignment |

---

## 5. Verification & Performance Validation

1. **Latency & Throughput**:
   - Time-to-First-Token (TTFT): $<150\text{ ms}$ on local GPU acceleration (vs. $400$–$900\text{ ms}$ over cloud HTTPS).
   - Sustained Generation: $75$–$85\text{ tok/s}$ on 14B, $>120\text{ tok/s}$ on 7B.
2. **Quota Resilience**:
   - Architectural projection: across simulated 100-turn agent workloads, deferring Category 3 tasks to local models is projected to achieve a **40%–60% reduction in cloud API token consumption** and eliminate secondary 429 rate limit triggers.
