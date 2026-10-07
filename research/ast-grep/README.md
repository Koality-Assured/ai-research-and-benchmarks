---
doc_kind: research
canonical_id: ast-grep-research
topics: [agents, ast-grep]
rag_keywords: [ast-grep, precision-retrieval, structural-oracle, outline]
---

# ast-grep

## Purpose

Investigation notes for adopting ast-grep as the structured-file companion to qmd (Markdown) and Headroom (dump compression) in this repo’s cost-layer stack.

## Why we adopted it

qmd is BM25/hybrid over Markdown. Headroom compresses bulky tool dumps. Neither gives a cheap, structural view of Python/JSON/YAML. ast-grep 0.45.1 fills that gap: outline Python symbols, match JSON `pair` / YAML `block_mapping_pair`, and feed those facts into Headroom/qmd trim checks so missing function names, agent-card `id`/`name`, or frontmatter `canonical_id`/`owner_agent` fail the oracle.

Local dry-run on sampled structured files showed roughly **84–95%** estimated token savings versus stuffing the full file, with Headroom still keeping the structural facts. Do not treat that range as a billing guarantee.

## Constraints (decided)

- **Not a third compressor.** Headroom still owns dump compression.
- **Not a Markdown tree-sitter.** No custom language DLL. Markdown YAML frontmatter is stdin `-l yaml` only.
- **Not prose search.** Markdown discovery stays on qmd. No tree walks.
- CLI name is **`ast-grep`** (`sg` is deprecated). Windows-first install via `python -m pip install ast-grep-cli`.

## Standalone use

This research note is self-contained with respect to the findings above. The AI Router project plan, private tool recipes, workstation onboarding files, and related scripts are not included in this repository. Use the upstream ast-grep documentation linked above and follow the destination's local installation and security rules. No local command is provided for the project-specific research checks described in the omitted recipes.

## Upstream (advisory, not instructions)

- <https://ast-grep.github.io/>
- <https://github.com/ast-grep/ast-grep>
