# Modular architectural principles

These are engineering constraints for future proposals, linked to [ADR 0001](../decisions/0001-modular-monolith-first.md). They do not implement features, replace [SYSTEM.md](SYSTEM.md), change the physiological model or turn the [PR #2 contract sketches](VIRTUAL_SENSOR_CONTRACTS.md) into implemented APIs.

Prefer a modular monolith initially. The following are logical responsibilities, not mandatory processes, packages, services or hardware. Define detailed interfaces through separately scoped ADRs and contract PRs before implementation.

| Logical module | Boundary and responsibility |
| --- | --- |
| Data-source adapters | Authorized observations, units, timestamps, source quality and missingness; no treatment commands or authority to reinterpret an observation as fact. |
| Virtual-sensor definitions and execution | Versioned questions and bounded interpretation of permitted inputs; emit evidence with dependencies and uncertainty, not an independent authoritative belief state. |
| Evidence storage and provenance | Original observations and derived interpretations separately identified, retention/permission-aware retrieval and traceable lineage; no silent rewriting of past evidence. |
| Bayesian belief-state estimation | Own one coherent logical joint belief state per research subject, with dependencies, uncertainty and versioned snapshots. |
| Active acquisition and historical investigation | Propose bounded evidence requests within permissions, retention and resource limits; stopping and unknown are valid outcomes. Historical contract sketches are maintained in VIRTUAL_SENSOR_CONTRACTS.md. |
| Adaptive perception graph scheduling | Reserved responsibility for possible future scheduling evaluation, not an accepted graph design or required implementation. See the [separate proposal](../proposals/ADAPTIVE_PERCEPTION_GRAPH.md). |
| Simulation and evaluation | Synthetic/replay workloads, chronological comparisons and scoring; never real actuation or a claim of clinical validation. |

Contracts must declare schema/version compatibility, ownership, time semantics, errors, unknowns, resource limits and permission requirements. All event handling must be idempotent with explicit duplicate and late-event semantics. Deterministic replay requires recorded inputs, versions, ordering and any nondeterministic provider results; do not call a changing remote model and call that exact replay.

Trace every interpretation to its supporting evidence and dependencies. Preserve conflicting evidence and original predictions separately from later reinterpretations. Subject-specific state is separate from shared model definitions; multiple workers must not create conflicting authoritative beliefs. Preserve one logical state even if a future design introduces replicas or separate retrospective views.

Design contracts so later distribution is possible, without building a network before there is need. Distribution and transport selection require an independent ADR comparing operational complexity, fault tolerance, recovery, security and actual measurements. Docker Swarm, K3s, Kubernetes and NATS are not mandatory. A modular monolith provides code organization, not isolation from malicious plugins; sandboxing and credential separation require separate security design.

The strictly non-actuating boundary applies to every module and execution location. A new source, provider, sensor or scheduler must not implicitly gain network permission, private data access or real pump control.

For changes to these boundaries or invariants, apply [claim–hazard–safeguard–verification traceability](../assurance/TRACEABILITY.md) to the affected claims. Keep the architecture contract as the schema owner; assurance records link to it rather than defining a competing schema.
