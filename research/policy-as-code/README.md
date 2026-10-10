# Policy as Code Research

Investigation notes on declarative policy engines, Kubernetes admission control architectures, and automated Policy-as-Code (PaC) synthesis from human-curated standards.

Human entry point only. Follow [`../../research/AGENTS.md`](../AGENTS.md) and [`../../AGENTS.md`](../../AGENTS.md).

## Contents

| Document | Topic |
| --- | --- |
| [`kyverno-architecture-and-synthesis.md`](./kyverno-architecture-and-synthesis.md) | Comparative architecture: Kyverno vs OPA/Gatekeeper, in-tree CEL, and LLM synthesis reliability |
| [`pac-generation-patterns.md`](./pac-generation-patterns.md) | Architectural methodology for deriving machine-verifiable policies and tests from RFC 2119 standards |

## Related

- Kyverno references: [`../../references/kyverno/`](../../references/kyverno/README.md)
- Tooling recipes and starter policies: [`../../supporting/kyverno/`](../../supporting/kyverno/README.md)
- Curated standards: [`../../docs/standards/kubernetes-security.md`](../../docs/standards/kubernetes-security.md)
