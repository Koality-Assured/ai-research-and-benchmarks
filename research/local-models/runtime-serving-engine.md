---
title: "Local Models: Runtime Serving Engines & Windows 11 Architecture"
status: active
topics: [local-models, runtime-engines, ollama, llama-cpp, vllm, windows11, cuda]
date: 2026-10-09
---

# Local Models: Runtime Serving Engines & Windows 11 Architecture

Comparative evaluation and operational procedures for standing up local model serving engines on modern workstations across hardware profile tiers (Tier A through Tier E).

---

## 1. Serving Engine Architectural Comparison

| Runtime Engine | Windows 11 Support | Underlying Engine | OpenAI API Compatibility | Memory Overhead | Best Suited For | Tradeoffs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Ollama** | **Native** (Installer / Service) | llama.cpp fork with dynamic loader | Native (`/v1/chat/completions`, `/v1/embeddings`, `/v1/models`) | Low (~150 MB process RAM) | **Primary Workstation Runtime**: Seamless model download, automatic keep-alive, concurrent slots. | Less granular control over custom layer splits or experimental KV cache quantization flags. |
| **llama.cpp (`llama-server`)** | **Native** (Pre-compiled CUDA binary) | Direct C++ CUDA / cuBLAS | Native (`/v1/chat/completions`, `/v1/models`) | Minimal (~80 MB process RAM) | **Power Users / Custom Offloading**: Manual layer splitting (`-ngl`), FlashAttention (`-fa`), quantized KV cache (`-ctk q8_0 -ctv q8_0`). | Requires manual GGUF file management and shell launch scripts. |
| **vLLM** | **WSL2 / Linux Only** (Requires Ubuntu distro) | Python / C++ PagedAttention | Native (`/v1/chat/completions`) | High (Defaults to reserving 90% of GPU VRAM) | **Server / Multi-tenant**: High-concurrency continuous batching. | Windows friction; requires installing WSL2 distro and NVIDIA Container Toolkit; high idle VRAM footprint. |
| **LM Studio** | **Native** (GUI + `lms` CLI) | llama.cpp / MLX wrapper | Native (`/v1/chat/completions`) | Moderate (~300 MB GUI RAM) | **Interactive Prototyping**: Visual quant testing and prompt playground. | Extra GUI overhead; CLI daemon requires running background app. |

---

## 2. Recommended Primary Runtime: Ollama

Ollama is selected as the **primary turnkey local runtime** for workstations due to zero-configuration service management, automated model pulling from registry, native CUDA / Metal acceleration across GPU architectures, and built-in OpenAI API compatibility.

### 2.1 Installation & Configuration on Windows 11

1. **Install via Winget or Installer**:
   ```powershell
   winget install Ollama.Ollama
   ```
2. **Environment Variables Configuration (User / System)**:
   Set key tuning variables to optimize concurrency, flash attention, and persistence:
   - `OLLAMA_HOST=127.0.0.1:11434` (Binds locally, preventing external network exposure).
   - `OLLAMA_NUM_PARALLEL=4` (Allows up to 4 concurrent inference slots for parallel subagents).
   - `OLLAMA_MAX_LOADED_MODELS=2` (Allows holding e.g. Qwen 2.5 Coder 14B and an embedding model in memory simultaneously).
   - `OLLAMA_KEEP_ALIVE=30m` (Keeps model hot in VRAM for 30 minutes after last request to avoid reload latency).
   - `OLLAMA_FLASH_ATTENTION=1` (Enables FlashAttention-2 kernels on modern Tensor Cores).
   - `OLLAMA_MODELS=C:\Models\Ollama` (Optional: directs model weights to a designated fast NVMe SSD).

### 2.2 Model Pulling & Local Registry

Execute from PowerShell or Harness CLI:
```powershell
# Pull Primary 14B Coding Workhorse (~9.0 GB)
ollama pull qwen2.5-coder:14b

# Pull Fast 7B Deferral Workhorse (~4.7 GB)
ollama pull qwen2.5-coder:7b

# Pull Reasoning Model (~9.0 GB)
ollama pull deepseek-r1:14b

# Pull Local Embeddings Model (~600 MB)
ollama pull nomic-embed-text
```

### 2.3 Verification via OpenAI-Compatible Endpoint

Ollama exposes an OpenAI-compatible REST API at `http://127.0.0.1:11434/v1`:

```powershell
# Verify running models
curl http://127.0.0.1:11434/v1/models

# Test Chat Completion
curl http://127.0.0.1:11434/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d '{
    "model": "qwen2.5-coder:14b",
    "messages": [
      {"role": "system", "content": "You are a fast coding assistant."},
      {"role": "user", "content": "Write a python function to compute fibonacci."}
    ],
    "temperature": 0.2
  }'
```

---

## 3. Alternative High-Performance Runtime: llama.cpp (`llama-server`)

For maximum memory efficiency and fine-grained GPU/CPU offloading of 32B or 70B models, `llama-server.exe` provides surgical control over every layer.

### 3.1 Startup Recipe for Tier A (16 GB GPU) + System RAM Offloading

#### Scenario A: Full GPU Execution (Qwen 2.5 Coder 14B Q4_K_M)
```powershell
.\llama-server.exe `
  -m C:\Models\GGUF\qwen2.5-coder-14b-instruct-q4_k_m.gguf `
  -ngl 99 `
  -c 32768 `
  -fa `
  -ctk q8_0 -ctv q8_0 `
  --port 8080 `
  --host 127.0.0.1
```
- `-ngl 99`: Offloads all 48 transformer layers to GPU VRAM.
- `-c 32768`: Configures a 32k context window.
- `-fa`: Enables FlashAttention.
- `-ctk q8_0 -ctv q8_0`: Quantizes the KV cache keys and values to 8-bit integers, halving KV cache VRAM usage from 6.1 GB to ~3.0 GB.

#### Scenario B: Hybrid GPU+CPU Offload (Qwen 2.5 Coder 32B Q4_K_M)
```powershell
.\llama-server.exe `
  -m C:\Models\GGUF\qwen2.5-coder-32b-instruct-q4_k_m.gguf `
  -ngl 36 `
  -t 16 `
  -c 16384 `
  -fa `
  --port 8080 `
  --host 127.0.0.1
```
- `-ngl 36`: Offloads ~36 of 64 layers to GPU VRAM ($\sim11.2\text{ GB}$ VRAM).
- `-t 16`: Assigns 16 high-performance CPU worker threads to process remaining layers in host system RAM.
- Throughput: $\sim14$–$18\text{ tokens/second}$.

---

## 4. API Standard & Interface Contract

Both Ollama and `llama-server` adhere strictly to the OpenAI Chat Completions API standard:

- **Endpoint**: `POST {base_url}/chat/completions`
- **Streaming**: Server-Sent Events (SSE) emitting `data: {"choices": [{"delta": {"content": "..."}}]}`
- **Usage Metrics**: Returns standard token counts (`prompt_tokens`, `completion_tokens`, `total_tokens`).
- **Tool Calling**:
  - Ollama translates OpenAI `tools` definitions (`type: "function"`) into prompt constraints for Qwen 2.5 Coder and Llama 3.1.
  - Native JSON mode supported via `"response_format": {"type": "json_object"}`.

---

## 5. Security & Isolation Considerations

1. **Localhost Binding**: Runtime must bind exclusively to `127.0.0.1` or `localhost`. Never bind to `0.0.0.0` on developer workstations to prevent cross-network extraction.
2. **Zero Cloud Exfiltration**: Inference executes 100% on the local GPU and CPU. No prompt data, tokens, or code snippets leave the machine.
3. **No API Key Required**: Authentication header `Authorization: Bearer local` or dummy tokens can be used, eliminating secret storage risks for the local tier.
