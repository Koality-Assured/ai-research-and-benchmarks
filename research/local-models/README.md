# Local models research

Investigation, hardware constraint analysis, serving engine evaluation, and frontier-to-local agent deferral architecture for hosting open-weight models on host infrastructure.

## Research topic pages

- [hardware-and-model-matrix.md](./hardware-and-model-matrix.md) — Workstation hardware profile tiers (Tier A through Tier E), VRAM budget math, GQA memory scaling, model matrix (Qwen 2.5 Coder 7B/14B/32B, DeepSeek-R1 Distill 14B/32B, Llama 3.1/3.3), and benchmark comparisons.
- [runtime-serving-engine.md](./runtime-serving-engine.md) — Serving engine comparison (Ollama vs. llama.cpp `llama-server` vs. vLLM), Windows 11 setup, environment configuration, startup recipes, FlashAttention, and KV cache quantization.
- [deferral-architecture.md](./deferral-architecture.md) — Frontier-to-local deferral pattern, task taxonomy, Harness control plane configuration (`config/harness.config.json`), Harness CLI integration, and zero-cost local model tiering.
- [system-one-decision-models.md](./system-one-decision-models.md) — System 1 non-autoregressive decision models (Jev vs. open-source Laya/ModernBERT), sub-50ms routing, triage, mutation gating, and programmatic branching.

## Active initiatives

- Project Proposal: [../../projects/local-models/README.md](../../projects/local-models/README.md)
