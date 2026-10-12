---
doc_kind: result
canonical_id: benchmark-suite-combined
purpose: [process]
topics: [benchmarks, fleet, cost-layers, retrieval, tool-efficiency, task-eval]
generated_at_utc: 2026-08-31T15:27:11Z
---

# Unified Benchmark Suite Execution Report

Consolidated benchmark across agent cost estimation, fleet dry-run simulation, corpus retrieval accuracy, tool output compression, and autonomous coding agent task evaluations.

## Executive Summary

- Run Date: **2026-08-31**
- Overall Status: **PASS**
- Fleet Pass Rate: **100.0%**
- Retrieval MRR: **1.0000**
- Tool Compression Ratio: **5.1%**
- Task Eval Pass@1: **100.0%**

## Benchmark Modules

| Module | Script | Status | Key Metric |
| --- | --- | --- | --- |
| Agent Cost Estimator | `estimate_agent_costs.py` | **PASS** | 24 agents priced |
| Fleet Dry-Run Benchmark | `benchmark_agent_fleet.py` | **PASS** | Pass rate: 100.0% |
| Corpus Retrieval Benchmark | `benchmark_retrieval.py` | **PASS** | MRR: 1.0000 |
| Tool Efficiency Benchmark | `benchmark_tool_efficiency.py` | **PASS** | Reduction: 5.1% |
| Task Evaluation Benchmark | `benchmark_task_eval.py` | **PASS** | Pass@1: 100.0% |

## Sub-Reports

- [Agent Cost Estimates](file:///[REPO_ROOT]/results/cost-layers/agent-estimates/report.md)
- [Fleet Dry-Run Simulation](file:///[REPO_ROOT]/results/benchmarks/fleet/2026-08-31/report.md)
- [Corpus Retrieval Accuracy](file:///[REPO_ROOT]/results/benchmarks/retrieval/2026-08-31/report.md)
- [Tool Compression Efficiency](file:///[REPO_ROOT]/results/benchmarks/tool-efficiency/2026-08-31/report.md)
- [Coding Task Evaluation](file:///[REPO_ROOT]/results/benchmarks/task-eval/2026-08-31/report.md)
