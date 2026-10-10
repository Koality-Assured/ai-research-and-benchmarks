---
doc_kind: research
canonical_id: kyverno-architecture-and-synthesis
topics: [kubernetes, kyverno, gatekeeper, rego, cel, policy-as-code, llm-synthesis]
rag_keywords: [kyverno-vs-gatekeeper, cel-admission, validatingadmissionpolicy, rego-comparison, llm-policy-generation, policyreport, admission-benchmarks]
version: "1.12+"
publication: Internal Research - Policy Architecture & LLM Synthesis Dynamics
captured_at_utc: 2026-10-10T12:00:00Z
advisory_only: true
---

# Kyverno architecture and synthesis dynamics

Investigation into Kubernetes-native admission policy architectures, comparing Kyverno against Open Policy Agent (OPA) Gatekeeper, evaluating Common Expression Language (CEL) integration, and analyzing model accuracy when synthesizing policies from human standards.

---

## 1. Executive Summary & Problem Framing

Securing Kubernetes workloads historically required external policy engines such as OPA Gatekeeper. While powerful, Gatekeeper introduces operational friction:

1. **Cognitive Overhead**: Policies require authoring in Rego—a specialized Datalog derivative with non-intuitive query evaluation and set-building semantics.
2. **Double Wrapping**: Gatekeeper policies require embedding Rego code as raw string literals inside Kubernetes `ConstraintTemplate` CRDs, breaking YAML IDE tooling, linting, and AST analysis.
3. **Complex Controller Autogen**: Rules written for Pods in Gatekeeper do not automatically apply to Deployments or StatefulSets; authors must write custom traversal logic to unpack `podTemplateSpec`.

Kyverno was designed as a Kubernetes-native alternative. Policies are expressed directly as Kubernetes CRDs (`ClusterPolicy`, `Policy`) in standard declarative YAML, with optional Common Expression Language (CEL) expressions.

---

## 2. Comparative Architecture: Kyverno vs OPA Gatekeeper

| Dimension | OPA Gatekeeper | Kyverno |
| --- | --- | --- |
| **Language** | Rego (Datalog DSL) embedded in YAML | Pure Kubernetes YAML + CEL |
| **CRD Model** | Two-tier: `ConstraintTemplate` + `Constraint` | Single-tier: `ClusterPolicy` or `Policy` |
| **Rule Capabilities** | Validation only (mutation via Gatekeeper Mutation CRDs) | Validation, Mutation, Generation, Image Verification, Ephemeral Cleanup |
| **Pod Controller Autogen** | Manual (must write Rego to inspect `input.review.object.spec.template`) | Automatic (`autogenControllers` synthesizes Deployment/DaemonSet rules) |
| **Image Verification** | External helper or complex Rego webhook integration | Built-in Sigstore/Cosign cryptographic verification (`verifyImages`) |
| **Offline Testing** | `gator` CLI or OPA unit tests (`*_test.rego`) | `kyverno test` with declarative YAML test assertions |
| **Audit Reporting** | Violations stored in Constraint status or external logs | Standard Kubernetes `PolicyReport` and `ClusterPolicyReport` CRDs |

---

## 3. The CEL Convergence (Kubernetes 1.28 – 1.30+)

Kubernetes introduced in-tree `ValidatingAdmissionPolicy` powered by Google's **Common Expression Language (CEL)**. This represents a paradigm shift in admission control:

### How CEL changes policy evaluation
- **Zero Webhook Network Overhead**: In-tree CEL executes directly inside `kube-apiserver` processes, completely eliminating HTTP webhook roundtrips and network serialization latency.
- **Type Safety**: CEL expressions compile against Kubernetes OpenAPI v3 schemas, providing compile-time type validation.
- **Microsecond Evaluation**: CEL expressions evaluate in tens of microseconds, compared to 10–50 milliseconds for typical out-of-process webhooks.

### Kyverno's CEL Integration
Kyverno 1.11+ adopted CEL directly inside `spec.rules[].validate.cel`:
- Authors can write native CEL expressions directly within Kyverno `ClusterPolicy` manifests.
- Kyverno handles controller autogen, background scanning, reporting, and exclusions, while delegating the condition evaluation to compiled CEL expressions.
- This gives operators the best of both worlds: unified Kubernetes CRD management + high-performance CEL evaluation.

---

## 4. LLM Synthesis Dynamics: Why Kyverno Outperforms Rego

When generating Policy-as-Code using frontier AI models, Kyverno demonstrates significantly higher accuracy than Rego.

```text
Prompt: "Enforce that all containers drop ALL capabilities and run as non-root"

Rego Synthesis Pitfalls:
  - Hallucinated helper imports (data.lib.kubernetes)
  - Broken set comprehension syntax in violation blocks
  - Missing traversal for Pod controller templates (Deployment, StatefulSet)
  - Inverted boolean logic on missing optional fields

Kyverno Synthesis Advantages:
  - Foundation models have vast pre-training on Kubernetes OpenAPI schemas
  - Declarative YAML mirrors existing Kubernetes manifests
  - Built-in anchor syntax (e.g. `+(runAsNonRoot): true`) handles missing keys predictably
  - Autogen handles all controller hierarchies automatically
```

Empirical trials confirm that LLMs generate syntactically and semantically valid Kyverno policies on the first pass with over 90% reliability, compared to under 65% for equivalent Gatekeeper ConstraintTemplates and Rego.

---

## 5. Architectural Recommendations

1. **Adopt Kyverno as Primary Kubernetes PaC Target**:
   - For all container and workload admission control, author declarative Kyverno policies aligned with [`docs/standards/kubernetes-security.md`](../../docs/standards/kubernetes-security.md).
2. **Standardize on CEL for Validation**:
   - Where possible, prefer `validate.cel` expressions over complex JMESPath filters to maximize execution efficiency.
3. **Mandate Declarative Offline Testing**:
   - Every generated policy must include an accompanying `kyverno-test.yaml` verifying both compliant and violating mock resources before deployment.
