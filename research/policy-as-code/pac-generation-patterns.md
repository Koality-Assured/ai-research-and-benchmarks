---
doc_kind: research
canonical_id: pac-generation-patterns
topics: [policy-as-code, pac-architecture, spec-to-code, kyverno, kubernetes, governance]
rag_keywords: [pac-pipeline, spec-to-code, rfc2119-extraction, spec-ir, test-co-generation, provenance, advisory-first]
version: "1.0"
publication: Internal Research - Generalized Policy-as-Code Generation Patterns
captured_at_utc: 2026-10-10T12:00:00Z
advisory_only: true
---

# Policy as Code generation patterns (Spec-to-Code)

Generalized architectural framework for translating human-curated organizational standards into machine-enforceable, verifiable policy code.

---

## 1. The Core Principle: Traceability and Provenance

Policy-as-Code must never be invented from a vacuum. In enterprise architectures, disconnected policies lead to rule drift, developer confusion, and unmaintainable exception sprawling.

**Every policy rule must remain strictly downstream from an authoritative human standard.**

```text
Human Standard (docs/standards/*.md)
        │
        ▼
Normative Invariants (RFC 2119 MUST / SHOULD NOT)
        │
        ▼
Policy Engine Implementation (Kyverno, Gatekeeper, Pulumi)
        │
        ▼
Automated Unit Tests (Passing & Failing Mock Resources)
```

---

## 2. The Spec-to-Code Synthesis Pipeline

A reliable agentic or automated synthesis pipeline decomposes into four formal stages:

### Stage 1: Invariant Extraction
Inspect the curated standard (e.g. [`docs/standards/kubernetes-security.md`](../../docs/standards/kubernetes-security.md)) and isolate atomic normative requirements:

```markdown
"Apply immutable image tags (digest or unique build ID); prohibit mutable tags such as :latest in production manifests."
```

### Stage 2: Spec-IR Normalization
Normalize the English requirement into a structured Intermediate Representation (Spec-IR) defining target resources, match conditions, and enforcement constraints:

```yaml
id: K8S-SEC-IMG-001
source_standard: docs/standards/kubernetes-security.md
source_section: "## Container image and workload hardening"
normative_strength: MUST NOT
target:
  kind: Pod
  api_groups: [""]
condition:
  field: spec.containers[*].image
  operator: not_ends_with
  value: ":latest"
failure_action: Audit
message: "Workloads must use immutable image tags or digests; :latest is prohibited."
```

### Stage 3: Target Engine Synthesis
From the normalized Spec-IR, synthesize the concrete engine artifact. For Kyverno:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
  annotations:
    policies.kyverno.io/title: Disallow Latest Tag
    policies.kyverno.io/standard: docs/standards/kubernetes-security.md
spec:
  validationFailureAction: Audit
  rules:
    - name: validate-image-tag
      match:
        any:
        - resources:
            kinds:
              - Pod
      validate:
        message: "Workloads must use immutable image tags or digests; :latest is prohibited."
        pattern:
          spec:
            containers:
              - image: "!*:latest"
```

### Stage 4: Test Manifest Co-Generation
Synthesize paired mock resources (`resources.yaml`) and declarative test assertions (`kyverno-test.yaml`):

- **Passing Mock**: A workload using `nginx:1.25.3` or `nginx@sha256:...`.
- **Failing Mock**: A workload using `nginx:latest` or `nginx`.
- **Assertion**: Verifies that the test runner flags the failing mock while admitting the passing mock.

---

## 3. Governance and Safe Rollout Rules

When synthesizing policies across any infrastructure domain, adhere to four operational safety rules:

1. **Advisory by Default**:
   - Initial deployment must always set `validationFailureAction: Audit` (or equivalent warning mode).
   - Generates actionable `PolicyReport` telemetry without rejecting live deployments.
2. **Explicit System Exclusions**:
   - System and operator namespaces (`kube-system`, `kyverno`, `monitoring`) must be excluded in the policy manifest.
   - Prevents bootstrapping deadlocks and ingress controller crashes.
3. **Controller Autogen Discipline**:
   - Workload policies targeting `Pod` must account for higher-level controllers (`Deployment`, `StatefulSet`, `DaemonSet`, `Job`).
4. **Zero Live Credential Access**:
   - Policies and test runners must run entirely offline in CI/CD without querying live production clusters or requiring cloud credentials.
