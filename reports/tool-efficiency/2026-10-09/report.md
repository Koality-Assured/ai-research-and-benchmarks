---
doc_kind: result
canonical_id: context-efficiency-public-safe-headroom-benchmark
purpose: [process]
topics: [headroom, compression, synthetic-fixtures, reproducibility]
generated_at_utc: 2026-10-09T22:36:57Z
---

# Synthetic Headroom reproduction

The reproducible run measured Headroom 0.40.0 on 15 deterministic synthetic tool outputs. It found mean token reductions of 64.91% for JSON tool output, 97.52% for build logs, and 97.16% for grep-hit output. The exact marker oracle found all 25 markers after compression. The fixtures deliberately contain repeated synthetic padding and structure, so these results may overstate savings on less-repetitive inputs.

## Evidence

| Fixture family | Trials | Mean Headroom-reported token reduction | Range | Exact markers found |
| --- | ---: | ---: | ---: | ---: |
| JSON tool output | 5 | 64.91% | 64.79–65.00% | 10/10 |
| Build-log output | 5 | 97.52% | 97.07–97.90% | 5/5 |
| Grep-hit output | 5 | 97.16% | 96.54–97.67% | 10/10 |
| All synthetic trials | 15 | 86.53% | 64.79–97.90% | 25/25 |

Every trial returned a nonzero Headroom token count. A separate tiktoken count over compact JSON-serialized messages averaged 65.24%, 97.49%, and 97.14% savings for JSON, build logs, and grep hits respectively. These counts do not include provider-side message framing and are not billing estimates.

## Method and scope

The run used CPython 3.13.16, `uv 0.12.23`, `headroom-ai 0.40.0`, and `tiktoken 0.14.0` with `o200k_base`. Headroom's `compress()` API ran locally with model label `gpt-4o`, `protect_recent=0`, `compress_user_messages=False`, and `kompress_model="disabled"`. No provider API was called. The complete dependency lock is `scratch/whitepaper-drafts/context-efficiency-methods/2026-10-09/public-reproduction/uv.lock` (SHA-256 `c9577034979151b56d423bfe9d3570c3e58931a768be3b5141385384ce6573d7`).

The oracle checks only whether predetermined synthetic strings remain as exact substrings in the serialized messages. It does not measure semantic fidelity, other fact retention, task success, security, or behavior on real tool output. The overall 86.53% is the unweighted mean of the 15 per-trial Headroom ratios. These are descriptive results for the 15 public fixtures, not general performance bounds.

The runtime emitted a Headroom warning that Windows used the pure-Python detector because the native Magika/ONNX backend is unsafe by default there. The run completed without a timeout; the runtime note is not a confirmed software defect. See `private-run/runtime-diagnostics.json` for the classification.

## Reproduction and artifacts

Public candidate package: `public-candidate/`. Run it with:

```text
uv sync --locked --python 3.13.16
uv run --locked python run_benchmark.py --output-dir output
```

Full per-trial synthetic inputs and compressed outputs are in `private-run/trial-details.jsonl`. Sanitized per-trial measurements and aggregates are in `private-run/trial-metrics.json` and `private-run/summary.json`. The candidate subset contains only the fixture and runner code, lock/pyproject, method manifest, sanitized metrics, and hashes.
