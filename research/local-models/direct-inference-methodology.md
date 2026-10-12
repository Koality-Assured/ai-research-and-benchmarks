# Direct local model inference methodology

Operational and architectural dossier for human-driven direct inference on host-local language models, air-gapped security workflows, and repository boundary separation.

---

## 1. Context and rationale

While frontier commercial models (Claude 3.7 Sonnet, Gemini 3 Pro, GPT-4o) excel at high-level reasoning and complex architecture synthesis, specific classes of engineering and security work cannot be routed through commercial cloud APIs:

1. **Safety refusals & false positives**: Frontier commercial providers enforce strict alignment guardrails designed for consumer chat interfaces. These filters frequently trigger false-positive refusals on legitimate cybersecurity activities, including exploit proof-of-concept (PoC) reproduction, shellcode analysis, buffer overflow verification, deserialization gadget chaining, and red-team payload development.
2. **Proprietary intellectual property & NDA compliance**: Proprietary algorithms, trade secrets, confidential customer data, internal network manifests, and enterprise API keys cannot be transmitted over public networks or ingested into vendor cloud infrastructure.
3. **Air-gapped and disconnected environments**: Critical infrastructure evaluations, incident response triage, and offline deployments require 100% host execution without active WAN connectivity.
4. **Unmetered high-volume batch experimentation**: Fuzzing log triage, bulk regex extraction, and continuous local code formatting incur zero marginal cloud spend.

To address these needs, the local AI architecture establishes a first-class **direct inference methodology** for the human operator, providing seamless terminal-native interaction with host-local System 2 models (e.g. `qwen2.5-coder:14b`, `deepseek-r1:14b`) and System 1 decision models without cloud leakage.

---

## 2. Repository boundary: Public tooling vs. Private workloads

A primary design concern is maintaining clean separation between host-agnostic open-source tooling and confidential, proprietary workloads:

```text
+-------------------------------------------------------------------------+
|  Public Open-Source Tooling Tier (Zero Secrets / Host-Agnostic)        |
|                                                                         |
|  - Koality-Assured/ai-router (`harness chat --provider local`)          |
|  - Koality-Assured/local-ai-management (`local-ai chat`)                |
|  - Upstream runtimes: Ollama, llama-server, vLLM                        |
+-------------------------------------------------------------------------+
                                     |
                                     | (Invokes CLI with local flags)
                                     v
+-------------------------------------------------------------------------+
|  Private Workstation Tier (Air-Gapped / Private Git Repository)         |
|                                                                         |
|  Repo: `Koality-Assured/private-workstation-ai` (Private)               |
|                                                                         |
|  - Internal exploit research, CVE reproductions, zero-day PoCs          |
|  - Proprietary source trees, client NDA materials, internal configs     |
|  - Private prompt templates and domain-specific system prompts          |
|  - Private fine-tuned LoRA weights and customized Modelfiles            |
|  - Local session notes and vulnerability triage records                 |
+-------------------------------------------------------------------------+
```

### Architectural recommendation on private repositories

- **Execution tooling remains public**: The underlying CLI utilities (`harness chat` and `local-ai chat`), REPL loops, context file formatters, hardware profilers, and benchmark runners are completely generic and public.
- **Sensitive artifacts live in a private repo**: Operators performing restricted work should maintain a dedicated private repository under `Koality-Assured` (e.g. `Koality-Assured/private-workstation-ai` or `internal-ai-tooling`).
- **Interaction pattern**: The operator launches `harness chat --provider local` or `local-ai chat` from within their private repo, passing relative paths to private context files (`-f ./exploits/poc.c`) and custom system prompts (`--system-file ./prompts/redteam.txt`). No sensitive data is ever checked into public repositories.

---

## 3. Direct inference interfaces

Operators have two complementary direct inference interfaces available on the workstation:

### 3.1 Harness CLI (`harness chat --provider local`)

Integrated directly into the primary `ai-router` harness, sharing session storage (`~/.harness/state.db`), slash commands, and multi-turn context management.

```bash
# Interactive REPL with local model and security preset
harness chat --provider local --model qwen2.5-coder:14b --preset security

# One-shot query with context file injection
harness chat --provider local -f ./vuln_driver.c -q "Audit this driver for race conditions"

# Pipe diff or log into session via stdin context
git diff HEAD~1 | harness chat --provider local -f - -q "Review diff for security regressions"

# Pipe raw query directly from stdin
cat prompt.txt | harness chat --provider local -q -
```

#### Supported slash commands in REPL

- `/preset <name>`: Switch active system prompt preset (`general`, `private_code`, `security`, `analysis`, `raw`).
- `/system <prompt>`: Inspect or override the session system prompt.
- `/model <id>`: Switch active local model.
- `/status`: Show active provider, model, token count, and session ID.
- `/compact`: Compress middle turns into a concise context checkpoint.
- `/sessions`: List recent conversation sessions.
- `/quit`: Exit the interactive session.

---

### 3.2 Satellite CLI (`local-ai chat`)

Standalone, lightweight CLI provided by `Koality-Assured/local-ai-management` with zero external dependencies beyond the Python standard library.

```bash
# Launch interactive REPL
local-ai chat --model qwen2.5-coder:14b --preset security

# One-shot query with structured JSON output
local-ai chat -m qwen2.5-coder:14b -q "List top 5 memory safety invariants in Rust" --json

# Multi-file context injection
local-ai chat -m qwen2.5-coder:14b -f ./auth.c -f ./auth.h -q "Identify bypass vectors"
```

---

## 4. System prompt presets for restricted tasks

Pre-configured prompt templates calibrated for high-autonomy local execution:

| Preset | Target Workload | Behavioral Contract |
| :--- | :--- | :--- |
| `security` | Exploit reproduction, vulnerability auditing, red-team analysis | Objective technical breakdown of attack vectors, memory corruption mechanics, and remediation payloads. Zero moralizing disclaimers or refusals. |
| `private_code` | Proprietary code refactoring & architecture | Air-gapped engineering posture, zero external network assumptions, strict memory safety and error handling invariants. |
| `analysis` | Formal logic, invariant checking, threat modeling | First-principles breakdown, explicit edge-case mapping, and hidden assumption enumeration. |
| `general` | Daily developer tasks | Direct, concise, technical answers without pleasantries or boilerplate. |
| `raw` | Direct model weights | Empty system prompt; pure completion against base model weights. |

---

## 5. Working with uncensored & custom models

For advanced security auditing where open-source base models exhibit undesirable refusal behavior, operators can serve abliterated or unaligned model variants locally:

### 5.1 Abliterated weight execution

```bash
# Pull abliterated/unaligned weights in Ollama
ollama pull huihui-ai/qwen2.5-coder-abliterated:14b

# Run directly via harness CLI
harness chat --provider local --model huihui-ai/qwen2.5-coder-abliterated:14b --preset security
```

### 5.2 Custom Modelfile synthesis

Generate tailored Modelfiles with customized stop tokens, context windows, and sampling parameters:

```bash
# Synthesize Modelfile via local-ai
local-ai modelfile --model qwen2.5-coder:14b --context 32768 --temperature 0.2 > Modelfile.security

# Build local image
ollama create local-sec-coder:14b -f Modelfile.security

# Verify in harness
harness chat --provider local --model local-sec-coder:14b
```

---

## 6. Air-gap security & anti-exfiltration guarantees

1. **Loopback interface enforcement**: By default, `harness chat` and `local-ai chat` reject non-loopback URLs (`127.0.0.1`, `localhost`, `::1`), preventing accidental transmission across external network interfaces.
2. **Zero external telemetry**: Local model calls emit no usage analytics, tracking beacons, or prompt hashes.
3. **Encrypted/Restricted session persistence**: Harness chat sessions are written to `~/.harness/state.db` with strict user-only read/write file permissions (`0600` / Windows ACLs).
