# AI Research & Benchmarks (`ai-research-and-benchmarks`)

[![Benchmarks CI](https://github.com/Koality-Assured/ai-research-and-benchmarks/actions/workflows/ci.yml/badge.svg)](https://github.com/Koality-Assured/ai-research-and-benchmarks/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Benchmarks: Automated](https://img.shields.io/badge/Benchmarks-Automated-brightgreen.svg)](benchmarks/)
[![Research: Empirical](https://img.shields.io/badge/Research-Empirical-purple.svg)](reports/)

## Mission Statement

`ai-research-and-benchmarks` is the open research and empirical evaluation repository of Koality-Assured.

We publish reproducible benchmarks, comparative harness evaluations, context retrieval trade-off analyses, and token cost telemetry across autonomous coding frameworks and LLM reasoning models.

## Architecture Overview

```
ai-research-and-benchmarks/
├── .github/workflows/ci.yml    # Benchmark dry-run CI pipeline
├── benchmarks/                 # Standardized test suites & datasets
│   ├── README.md
│   └── suites/
│       └── coding_agent_benchmark_v1.json  # Reference coding benchmark suite
├── harnesses/                  # Execution runners and harness adapters
│   ├── README.md
│   ├── __init__.py
│   └── runner.py               # Benchmark execution harness
├── telemetry/                  # Token usage & cost calculation engine
│   ├── README.md
│   ├── __init__.py
│   └── cost_calculator.py      # Multi-model token cost & headroom calculator
├── reports/                    # Published research reports and whitepapers
│   ├── README.md
│   └── template_evaluation_report.md
├── tests/                      # Automated test suite
│   ├── __init__.py
│   └── test_benchmarks.py      # Unit tests for runner and cost calculation
├── pyproject.toml              # Python project configuration
├── .editorconfig               # Editor configuration
├── .gitignore                  # Git ignore rules
└── LICENSE                     # MIT License
```

## Research Focus Areas

1. **Agentic Harness Efficiency:** Measuring wall-clock latency, token consumption, and cost-per-resolved-issue across coding agent architectures.
2. **Context Tiering & Headroom:** Quantifying performance and cost delta between raw text context dumps and Tier-4 AST Fact extraction with Headroom compression.
3. **Framework Shootouts:** Objective side-by-side evaluations of multi-agent orchestrators (e.g. LangGraph, AutoGen, CrewAI, Native Harnesses).

## Running Benchmarks

### Prerequisites
- Python >= 3.10

### Quickstart

```bash
# Clone the repository
git clone https://github.com/Koality-Assured/ai-research-and-benchmarks.git
cd ai-research-and-benchmarks

# Run benchmark suite in dry-run mode
python harnesses/runner.py --suite benchmarks/suites/coding_agent_benchmark_v1.json --dry-run

# Run cost calculator for context tier comparison
python telemetry/cost_calculator.py --input-tokens 50000 --output-tokens 2000 --model gpt-4o
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## Research Ethics & Methodology Disclosures

All benchmark runs adhere to strict empirical standards:
- **Reproducibility:** All prompt templates, harness configurations, and evaluation seeds are checked into git.
- **Fairness:** Temperature, seed, and timeout limits are pinned uniformly across evaluated frameworks.
- **Cost Attribution:** Token accounting reflects true blended input, output, cache-read, and cache-write rates.

## Contributing

We welcome benchmark task contributions and independent evaluation reports. Please see [`reports/README.md`](reports/README.md) for report authoring guidelines.

## Security Notice

Benchmark execution harnesses run arbitrary generated code. Harnesses MUST run inside sandboxed containers or ephemeral VMs. To report vulnerabilities, contact security@koality-assured.org.

## License

Distributed under the [MIT License](LICENSE). Copyright (c) 2026 Koality-Assured.
