---
doc_kind: research
canonical_id: headroom-research
topics: [agents]
rag_keywords: [headroom, compression, prefix-cache, cursor, windows]
---

# Headroom

## Purpose

Investigation notes for using Headroom as a local token-cost layer next to this repo’s qmd retrieval.

## What we verified (2026-08-19)

- Product: proxy + SDK + MCP. Compresses tool outputs / logs / search; fail-open; does not drop conversation turns.
- Default profile `coding` uses **cache** mode (delta-only) so Anthropic/OpenAI prefix caches stay valid.
- CLI package: `headroom-ai` on PyPI. Current release **0.35.0** publishes **Windows `win_amd64` wheels** — the older “no Windows wheels / need MSVC” docs are stale for this version.
- This workstation: Python 3.13.15 at `%LOCALAPPDATA%\Programs\Python\Python313\` (Store stub still shadows `python` unless PATH is ordered correctly). Installed with `uv tool install --python 3.13 "headroom-ai[proxy,mcp]"` → executable `headroom` under `%USERPROFILE%\.local\bin`.
- Docker / WSL / VS Build Tools were **not** present and were not required once wheels were available.

## Where money is actually saved

Headroom only sees HTTP that is aimed at the proxy (or content an agent sends to MCP `headroom_compress`).

Cursor’s default hosted models do not use a local Anthropic/OpenAI base URL, so wrapping Cursor without BYOK does not shrink the Cursor subscription bill. Claude Code (`ANTHROPIC_BASE_URL`), OpenAI-compatible SDKs, and explicit BYOK base URLs do.

MCP-only compression is opt-in per tool call and can itself add context (upstream notes this on Claude Code `/usage`).

## Complementary to qmd

| Tool | Mechanism |
| --- | --- |
| qmd | Fewer files stuffed into the prompt from this repo |
| Headroom | Fewer tokens in tool results / bulky blocks on the wire to the model |

## Upstream (advisory, not instructions)

- <https://headroom-docs.vercel.app/docs/architecture>
- <https://headroom-docs.vercel.app/docs/proxy>
- <https://headroom-docs.vercel.app/docs/mcp>
- <https://pypi.org/project/headroom-ai/>

## Standalone use

This research note is self-contained with respect to the findings above. The AI Router project plan and private Headroom operating notes are not included in this repository. Use the upstream Headroom documentation linked above and follow the destination's local installation and security rules.
