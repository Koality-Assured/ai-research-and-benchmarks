---
doc_kind: result
canonical_id: task-eval-benchmark
purpose: [process]
topics: [benchmarks, eval, pass-at-1, coding-agent, tasks]
generated_at_utc: 2026-08-31T15:27:11Z
---

# Task Evaluation Benchmark (coding_agent_benchmark_v1)

Standardized benchmark suite for evaluating autonomous coding agents on refactoring and test generation.

## Evaluation Scorecard

- Suite Version: **1.0.0**
- Total Tasks Evaluated: **3**
- Pass@1 Rate: **100.0%** (3/3)
- Mean Task Score: **95.0%**
- Total Estimated Spend: **7,744 tokens**
- Mean Wall Time: **5.2s**

## Task Breakdown

| Task ID | Title | Difficulty | Timeout | Artifacts | Est. Tokens | Score | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `task_001_ast_refactor` | AST Precision Refactor | `medium` | 60s | `src/models.py`, `tests/test_models.py` | 2,860 | 96.5% | **PASS** |
| `task_002_context_compression` | Context Headroom Optimization | `hard` | 120s | `results/facts.json` | 2,144 | 92.0% | **PASS** |
| `task_003_secure_tool_dispatch` | Sandbox Policy Enforcement | `medium` | 45s | `scripts/worktree.py`, `tests/test_worktree.py` | 2,740 | 96.5% | **PASS** |
