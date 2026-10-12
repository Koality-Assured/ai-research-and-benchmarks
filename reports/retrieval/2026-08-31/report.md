---
doc_kind: result
canonical_id: retrieval-benchmark
purpose: [process]
topics: [benchmarks, qmd, retrieval, rag, mrr, precision]
generated_at_utc: 2026-08-31T15:27:10Z
---

# Corpus Retrieval Accuracy & Quality Benchmark

Empirical evaluation of Markdown retrieval quality measuring Mean Reciprocal Rank (MRR), Precision@K, and query latency across ground-truth repository topics.

## Overall Metrics

- Mean Reciprocal Rank (MRR): **1.0000**
- Precision@1: **100.0%**
- Precision@3: **95.2%**
- Precision@5: **91.4%**
- Average Search Latency: **667.34 ms**
- Total Benchmark Queries: **7**

## Query-Level Results

| Query | Category | MRR | P@1 | P@3 | P@5 | Latency | Top Match |
| --- | --- | --- | --- | --- | --- | --- | --- |
| "isolate work git worktree" | `routing` | 1.00 | 1.0 | 1.0 | 1.0 | 702.48ms | — |
| "cost layers headroom compression" | `cost-layers` | 1.00 | 1.0 | 1.0 | 1.0 | 677.01ms | — |
| "stride threat model assessment" | `security` | 1.00 | 1.0 | 1.0 | 1.0 | 655.47ms | — |
| "ast-grep structural pattern matching" | `cost-layers` | 1.00 | 1.0 | 1.0 | 1.0 | 663.59ms | — |
| "confluence cql document management" | `collaboration` | 1.00 | 1.0 | 1.0 | 1.0 | 615.77ms | — |
| "slack block kit webhook message" | `collaboration` | 1.00 | 1.0 | 1.0 | 1.0 | 751.12ms | — |
| "benchmark agent cost estimation" | `benchmarks` | 1.00 | 1.0 | 0.7 | 0.4 | 605.97ms | — |
