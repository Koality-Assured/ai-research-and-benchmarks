---
doc_kind: result
canonical_id: agent-fleet-benchmark
purpose: [process]
topics: [benchmarks, fleet, dry-run, headroom, cache-invariance]
generated_at_utc: 2026-08-31T15:27:05Z
---

# Agent Fleet Benchmark & Dry-Run Simulation

Empirical dry-run validation and simulation sweep across all registered agents and skills, auditing prompt cache invariance, delegation graphs, tool schema footprints, and context ceiling headroom.

## Fleet Summary

- Total Agents Audited: **24**
- Total Skills Mapped: **83**
- Fleet Pass Rate: **100.0%** (24/24)
- Median Static Prefix: **1694 tokens**
- Average Headroom Remaining: **93.9%**
- Total Benchmark Wall Time: **4657.99 ms**

## Agent Breakdown

| Agent | Tier | Tools | Owned Skills | Static Prefix | 5-Turn Context | Headroom | Cache Invariant | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ai-tooling-ops` | `standard` | 6 | 7 | 1,591 | 5,991 | 94.0% | Yes | **PASS** |
| `artifact-agent` | `standard` | 6 | 13 | 1,921 | 6,321 | 95.8% | Yes | **PASS** |
| `as-code-agent` | `high` | 6 | 1 | 1,492 | 5,892 | 95.1% | Yes | **PASS** |
| `assessment-agent` | `standard` | 6 | 1 | 1,654 | 6,054 | 95.0% | Yes | **PASS** |
| `benchmark-agent` | `standard` | 6 | 5 | 2,028 | 6,428 | 94.6% | Yes | **PASS** |
| `chat-collab-agent` | `standard` | 6 | 4 | 2,078 | 6,478 | 93.5% | Yes | **PASS** |
| `cloud-admin-agent` | `standard` | 6 | 1 | 1,768 | 6,168 | 93.8% | Yes | **PASS** |
| `cloud-operator` | `standard` | 4 | 9 | 1,407 | 5,807 | 94.2% | Yes | **PASS** |
| `community-analyst` | `standard` | 6 | 8 | 2,024 | 6,424 | 94.6% | Yes | **PASS** |
| `detailed-activity` | `high` | 6 | 5 | 2,103 | 6,503 | 95.7% | Yes | **PASS** |
| `docs-collab-agent` | `standard` | 6 | 4 | 2,219 | 6,619 | 93.4% | Yes | **PASS** |
| `documentation-ops` | `standard` | 6 | 4 | 1,694 | 6,094 | 93.9% | Yes | **PASS** |
| `git-fast-operator` | `fast` | 2 | 1 | 835 | 5,235 | 89.5% | Yes | **PASS** |
| `github-ops` | `standard` | 4 | 2 | 1,305 | 5,705 | 94.3% | Yes | **PASS** |
| `google-suite-admin` | `standard` | 6 | 1 | 1,783 | 6,183 | 93.8% | Yes | **PASS** |
| `google-suite-operator` | `standard` | 6 | 3 | 1,917 | 6,317 | 93.7% | Yes | **PASS** |
| `memory-operator` | `standard` | 5 | 1 | 1,599 | 5,999 | 94.0% | Yes | **PASS** |
| `public-llm-admin` | `standard` | 6 | 1 | 1,832 | 6,232 | 93.8% | Yes | **PASS** |
| `qmd-ops` | `standard` | 4 | 2 | 1,208 | 5,608 | 93.0% | Yes | **PASS** |
| `reference-ops` | `standard` | 6 | 2 | 1,660 | 6,060 | 93.9% | Yes | **PASS** |
| `repo-sync-ops` | `standard` | 4 | 2 | 1,538 | 5,938 | 94.1% | Yes | **PASS** |
| `router` | `standard` | 8 | 1 | 4,032 | 8,432 | 91.6% | Yes | **PASS** |
| `router-maintenance` | `standard` | 6 | 4 | 1,673 | 6,073 | 93.9% | Yes | **PASS** |
| `script-ops` | `standard` | 6 | 1 | 1,432 | 5,832 | 94.2% | Yes | **PASS** |
