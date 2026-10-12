---
doc_kind: result
canonical_id: tool-efficiency-benchmark
purpose: [process]
topics: [benchmarks, cost-layers, headroom, ast-grep, compression, tokens]
generated_at_utc: 2026-08-31T15:27:10Z
---

# Tool Output Compression & Efficiency Benchmark

Empirical evaluation of tool payload compression (Headroom, ast-grep symbol tables, and log distillation), measuring token reduction ratios, fact retention fidelity, and serialization latency.

## Summary Metrics

- Total Fixtures Evaluated: **4**
- Total Raw Tokens: **2,147**
- Total Compressed Tokens: **2,037**
- Overall Token Reduction: **5.1%** (Saved 110 tokens)
- Gold Fact Preservation: **100.0%**
- Average Processing Latency: **72.7 ms**

## Fixture Breakdown

| Fixture | Category | Raw (Tokens) | Compressed (Tokens) | Reduction | Fact Retention | Latency |
| --- | --- | --- | --- | --- | --- | --- |
| `verbose_pytest_log` | `command_output` | 597 | 566 | **5.2%** | 100.0% (2/2) | 101.4ms |
| `large_git_diff` | `git_diff` | 559 | 531 | **5.0%** | 100.0% (3/3) | 51.83ms |
| `ast_symbol_dump` | `ast_grep` | 843 | 800 | **5.1%** | 100.0% (3/3) | 60.89ms |
| `raw_html_payload` | `web_fetch` | 148 | 140 | **5.4%** | 100.0% (3/3) | 76.7ms |
