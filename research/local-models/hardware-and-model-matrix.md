---
title: "Local Models: System Constraints & Model Evaluation Matrix"
status: active
topics: [local-models, hardware-constraints, vram-budget, benchmarks, quantizations]
date: 2026-10-09
---

# Local Models: System Constraints & Model Evaluation Matrix

Empirical evaluation of local open-weight language models tailored to host hardware specifications, memory budgets, inference latencies, and operational tasks.

---

## 1. Workstation Hardware Profile Tiers & System Constraints

Local model selection depends fundamentally on host hardware characteristics: dedicated GPU VRAM, system RAM capacity and memory bandwidth, CPU vector extensions (AVX2/AVX-512), and operating system runtime environment.

Workstations are categorized into five standard **Hardware Profiles**:

| Profile Tier | GPU / VRAM Class | System RAM & Bandwidth | Target Models & Placement | Expected Throughput |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 0 (System 1 Decision Layer)** | Co-exists with any GPU or CPU (<1 GB VRAM or RAM) | Shared with host OS | Laya (421M), ModernBERT (149M), SmolLM2-360M | **10–40 ms / decision**<br>(Non-autoregressive forward pass) |
| **Tier A (High-Performance GPU)** | 16 GB+ VRAM (e.g. Ada / Ampere / RDNA3 class; ~700+ GB/s) | 64–128 GB DDR5 (~70–90 GB/s) | 14B Q4_K_M (100% VRAM); 32B hybrid offload (GPU/CPU) | 14B: 70–85 tok/s<br>7B: 115–140 tok/s<br>32B: 14–18 tok/s |
| **Tier B (Standard Workstation GPU)** | 12 GB VRAM (e.g. RTX 4070 / 3080 class; ~500 GB/s) | 32–64 GB DDR4/DDR5 | 7B Q8_0 / 14B Q4_K_M (bounded context 8k–16k) | 14B: 65–75 tok/s<br>7B: 100–120 tok/s |
| **Tier C (Entry / Mobile GPU)** | 8 GB VRAM (e.g. RTX 4060 / Laptop class; ~280 GB/s) | 16–32 GB RAM | 7B Q4_K_M (100% VRAM) / 14B Q4 hybrid | 7B: 80–110 tok/s<br>3B: 140+ tok/s |
| **Tier D (Unified Memory / Apple Silicon)** | 36–128 GB Unified Memory (M2/M3/M4 Pro/Max; ~150–400 GB/s) | Shared with OS | 14B–32B Q4_K_M / Q8_0 (Metal accelerated) | 14B: 40–60 tok/s<br>32B: 20–30 tok/s |
| **Tier E (CPU-Only / Vector Fallback)** | None / Integrated GPU | 32–128 GB DDR4/DDR5 (AVX2 / AVX-512) | 1.5B–7B quantized models (100% RAM) | 1.5B: 25–40 tok/s<br>7B: 8–15 tok/s |

### 1.1 Usable VRAM Budgeting Rules

On desktop workstations driving graphical displays, operating systems (Windows DWM, macOS WindowServer, X11/Wayland) and desktop productivity applications reserve a portion of GPU VRAM:
- **Desktop Overhead ($VRAM_{\text{os}}$)**: Typically ~1.5 GB to 3.5 GB depending on monitor count, resolution (4K/ultrawide), and open applications.
- **Usable Budget ($VRAM_{\text{usable}}$)**:
  $$VRAM_{\text{usable}} = VRAM_{\text{total}} - VRAM_{\text{os}} - VRAM_{\text{headroom}}$$
  Where $VRAM_{\text{headroom}} \approx 0.5\text{–}1.0\text{ GB}$ is safety margin to prevent CUDA out-of-memory (OOM) crashes.
- For a 16 GB GPU baseline, typical usable VRAM is $\sim12.5\text{–}13.5\text{ GiB}$.

---

## 2. Memory Footprint & VRAM Budget Mathematics

Local LLM deployment requires calculating two critical memory pools: **Model Weights ($M_{\text{weights}}$)** and **KV Cache ($M_{\text{kv}}$)**.

### 2.1 Model Weights Memory

$$M_{\text{weights}} \approx P \times \frac{b}{8} \times 1.05$$

Where $P$ is parameter count (billions), $b$ is average bits per weight, and $1.05$ accounts for model metadata and CUDA runtime overhead.

- **4-bit (Q4_K_M / AWQ / GPTQ-Int4)**: $b \approx 4.5 \implies \sim0.56\text{ GB per billion parameters}$.
- **8-bit (Q8_0 / FP8 / INT8)**: $b \approx 8.0 \implies \sim1.0\text{ GB per billion parameters}$.
- **16-bit (FP16 / BF16)**: $b \approx 16.0 \implies \sim2.0\text{ GB per billion parameters}$.

### 2.2 KV Cache Memory (Grouped Query Attention)

For models using Grouped Query Attention (GQA), memory per sequence token is:

$$M_{\text{kv}} = 2 \times L \times H_{\text{kv}} \times D_{\text{head}} \times C \times B_{\text{kv}}$$

Where $L$ is number of layers, $H_{\text{kv}}$ is number of KV heads, $D_{\text{head}}$ is head dimension, $C$ is context length in tokens, and $B_{\text{kv}}$ is bytes per KV cache element (FP16 = 2 bytes, Q8_0 = 1 byte, FP8 = 1 byte).

**Example: Qwen 2.5 Coder 14B ($L=48, H_{\text{kv}}=8, D_{\text{head}}=128$):**
- Per token in FP16: $2 \times 48 \times 8 \times 128 \times 2 = 196,608\text{ bytes} \approx 0.187\text{ MB/1k tokens}$.
- At 32,768 tokens (FP16): $\approx 6.1\text{ GB}$.
- At 32,768 tokens with **quantized Q8_0 KV cache** (`-ctk q8_0 -ctv q8_0`): $\approx 3.05\text{ GB}$.
- At 16,384 tokens with **quantized Q8_0 KV cache**: $\approx 1.53\text{ GB}$.

### 2.3 Operating Budget in 16 GB VRAM Class (Tier A Baseline)

Given $\sim13.0\text{ GB}$ usable VRAM after OS desktop allocation:
1. **7B Model (Q4_K_M / Q8_0)**:
   - Weights: $4.5\text{ GB}$ (Q4) or $8.0\text{ GB}$ (Q8).
   - KV Cache (32k tokens, Q8): $\sim1.2\text{ GB}$.
   - **Total VRAM**: $5.7\text{ GB}$ to $9.2\text{ GB}$. Fits 100% in VRAM with zero paging across all workstation tiers.
2. **14B Model (Q4_K_M)**:
   - Weights: $8.9\text{ GB}$.
   - KV Cache (16k tokens, Q8): $\sim1.5\text{ GB}$.
   - CUDA Context & FlashAttention buffers: $\sim0.8\text{ GB}$.
   - **Total VRAM**: $\sim11.2\text{ GB}$. Fits 100% in VRAM comfortably alongside desktop applications on 16 GB GPUs.
3. **32B Model (Q4_K_M)**:
   - Weights: $\sim19.8\text{ GB}$.
   - Exceeds 16 GB VRAM. Requires hybrid layer splitting: offload ~36 of 64 layers to GPU ($\sim11.0\text{ GB}$ VRAM), keeping remaining layers in high-speed system RAM.

---

## 3. Evaluated Model Candidates & Benchmark Matrix

Empirical benchmarks across coding (HumanEval, MultiPL-E, MBPP, LiveCodeBench), reasoning (MATH-500, AIME), and operational speed on Tier A (16 GB GPU) hardware:

| Model | Params | Quantization | Size (GB) | Memory Placement | Tier A (16 GB) Speed | Coding / Benchmark Score | Optimal Task Profile |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Qwen 2.5 Coder 14B Instruct** | 14.7B | Q4_K_M | 8.98 GB | 100% VRAM | **72–85 tok/s** | HumanEval: 86.6%<br>MBPP: 83.4%<br>LCB: 41.2% | **Primary Workhorse**: Code generation, refactoring, ast-grep translations, tool calls. |
| **Qwen 2.5 Coder 7B Instruct** | 7.6B | Q4_K_M / Q8_0 | 4.68 / 8.1 GB | 100% VRAM | **115–140 tok/s** | HumanEval: 82.3%<br>MBPP: 78.2% | **High-Velocity Deferral**: Linter fixes, docstring generation, boilerplate, commit messages. |
| **DeepSeek-R1-Distill-Qwen-14B** | 14.7B | Q4_K_M | 8.98 GB | 100% VRAM | **68–80 tok/s** | MATH-500: 93.9%<br>AIME 2024: 53.1% | **Deep Reasoning**: Architecture analysis, complex regex synthesis, debugging tricky edge cases. |
| **Llama 3.1 8B Instruct** | 8.0B | Q8_0 / Q4_K_M | 8.5 / 4.9 GB | 100% VRAM | **95–120 tok/s** | HumanEval: 72.6%<br>MMLU: 68.4% | **Generalist / Tool-Use**: General NLP classification, JSON formatting, summary. |
| **Qwen 2.5 Coder 32B Instruct** | 32.5B | Q4_K_M | 19.8 GB | Hybrid (GPU + RAM) | **14–18 tok/s** | HumanEval: 92.7%<br>MultiPL-E: 77.0%<br>LCB: 51.1% | **Frontier-Level Coding**: High-complexity autonomous algorithms, full module scaffolding. |
| **DeepSeek-R1-Distill-Qwen-32B** | 32.5B | Q4_K_M | 19.8 GB | Hybrid (GPU + RAM) | **12–16 tok/s** | MATH-500: 94.3%<br>AIME: 72.6% | **Frontier Reasoning**: Matches OpenAI o1-mini on math and competitive logic. |
| **Llama 3.3 70B Instruct** | 70.6B | Q4_K_M | 42.5 GB | RAM Heavy (Hybrid) | **5–8 tok/s** | HumanEval: 81.7%<br>MMLU: 86.0% | **Offline Synthesis**: Overnight batch runs, offline compliance audit without API spend. |
| **bge-large-en-v1.5** | 335M | FP16 | 1.34 GB | 100% VRAM | <15 ms / batch | MTEB: 64.11 | **Local Dense Embeddings**: Semantic doc retrieval, fast routing similarity. |
| **bge-reranker-v2-m3** | 568M | FP16 | 1.14 GB | 100% VRAM | <25 ms / pair | NDCG@10: 67.8 | **Local Reranking**: Cross-encoder verification of candidate context snippets. |
| **Laya (ModernBERT-large)** | 421M | FP16 / Int8 | 0.84 / 0.42 GB | 100% VRAM or RAM | **12–20 ms / decision** | Jev API Drop-in | **System 1 Decision Engine**: Non-autoregressive routing, triage, mutation gating, calibrated probabilities. |
| **ModernBERT-base Classifier** | 149M | FP16 / Int8 | 0.30 / 0.15 GB | 100% VRAM or RAM | **6–10 ms / decision** | GLUE: 89.2 | **Ultra-Fast Triage**: High-throughput intent classification and inline security guardrails. |

---

## 4. Architectural Recommendations Across Tiers

### 4.1 Fleet Configuration by Hardware Profile

1. **Tier A Workstations (16 GB+ VRAM, 64–128 GB RAM)**:
   - Primary Workhorse: **Qwen 2.5 Coder 14B Instruct (Q4_K_M)** ($\sim75\text{ tok/s}$, 100% VRAM).
   - Velocity Worker: **Qwen 2.5 Coder 7B Instruct (Q4_K_M)** ($>120\text{ tok/s}$, 100% VRAM).
   - Reasoning Worker: **DeepSeek-R1-Distill-Qwen-14B (Q4_K_M)**.
   - Offline Heavyweight: **Qwen 2.5 Coder 32B Instruct (Q4_K_M)** (hybrid offload at $\sim16\text{ tok/s}$).

2. **Tier B Workstations (12 GB VRAM, 32–64 GB RAM)**:
   - Primary Workhorse: **Qwen 2.5 Coder 14B Instruct (Q4_K_M)** with 16k context or **Qwen 2.5 Coder 7B Instruct (Q8_0)**.
   - Velocity Worker: **Qwen 2.5 Coder 7B Instruct (Q4_K_M)**.

3. **Tier C Workstations (8 GB VRAM, 16–32 GB RAM)**:
   - Primary Workhorse: **Qwen 2.5 Coder 7B Instruct (Q4_K_M)** ($\sim4.7\text{ GB}$ VRAM, 100% VRAM).
   - Lightweight Worker: **Qwen 2.5 Coder 3B / 1.5B** or **Llama 3.2 3B**.

4. **Tier D Workstations (Unified Memory / Apple Silicon, 36–128 GB)**:
   - Primary Workhorse: **Qwen 2.5 Coder 14B or 32B (Q4_K_M / Q8_0)** directly in unified memory via Metal backend.

5. **Tier E Workstations (CPU-Only / Vector Acceleration)**:
   - Primary Worker: **Qwen 2.5 Coder 1.5B / 7B (Q4_K_M)** with AVX2/AVX-512 multi-threading.

---

## 5. Workstation Memory Allocation Architecture

```text
+-------------------------------------------------------------------------------+
|                    WORKSTATION RESOURCE ALLOCATION OVERVIEW                   |
|                                                                               |
|   DEDICATED GPU VRAM (16 GB Class)                 HOST SYSTEM RAM (64-128 GB)|
|   +---------------------------------------+        +----------------------+   |
|   | OS / Desktop Display GUI| 2.0-3.5 GB  |        | OS & Core Services   |   |
|   +-------------------------+-------------+        | (8-16 GB used)       |   |
|   | Primary Model (14B Q4)  | ~9.0 GB     |        +----------------------+   |
|   | KV Cache (16k-32k tok)  | 1.5-2.0 GB  |        | Available for Hybrid |   |
|   | CUDA Overhead & Headroom| 1.0-1.5 GB  |        | Offload & 32B Models |   |
|   +-------------------------+-------------+        | (48-112 GB free)     |   |
|   | Total Usable VRAM Budget: ~13.0 GB    |        +----------------------+   |
|   +---------------------------------------+                                   |
+-------------------------------------------------------------------------------+
```
