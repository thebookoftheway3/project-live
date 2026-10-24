# ADR 0001: Prefer a modular monolith for initial research implementation

- Status: Proposed
- Proposed date: 2026-10-24
- Decision date: Pending explicit maintainer review
- Decision-maker: Current maintainer; reviewers: none recorded yet
- References: R00, R08, R10, R12, R15, R17, R20; LIVE-016; [principles](../architecture/PRINCIPLES.md)
- Supersedes: None

## Problem and evidence

The repository currently contains a small synthetic Python replay with no runtime third-party dependencies declared, distributed workload measurements or demonstrated need for service orchestration. Architectural scope is growing faster than implementation evidence. We need boundaries that can evolve without making operations a prerequisite for research.

This is an implementation-structure proposal, not a change to the insulin research model or approval of the unmerged virtual-sensor specification in PR #2.

## Alternatives

| Option | Complexity, faults and recovery | Security and measured need |
| --- | --- | --- |
| Unstructured single process | Minimal setup, but coupled state and implicit contracts make change and replay difficult. Process failure affects the whole run. | Few network surfaces, but weak ownership boundaries; no justification for losing traceability. |
| Modular monolith (preferred) | Explicit interfaces within one deployable unit; deterministic replay and restart from recorded evidence; process failure remains shared. | Fewer credentials and transports. Logical boundaries are not isolation against malicious plugins. Fits current synthetic scale. |
| Distributed services | Independent failure/scale domains, but partial failures, ordering, retries, recovery and operations require additional design. | More identities, secrets and network surfaces; no measured bottleneck currently justifies that cost. |

## Proposed decision

Prefer logical modules in a modular monolith, using the [principles](../architecture/PRINCIPLES.md). Preserve one coherent logical Bayesian belief state per research subject; replicas or retrospective views must not become competing authorities. Keep contracts versioned and evidence traceable. No runtime changes are authorized by this ADR while proposed.

Do not mandate Docker Swarm, K3s, Kubernetes, NATS or another orchestrator/transport. A future transport or distribution ADR must compare operational complexity, fault tolerance, recovery, security and measured need. Provider isolation may justify a separate sandbox earlier, but requires its own threat model and decision; in-process plugins are not a security boundary.

## Validation and reconsideration

No benchmark or new implementation was performed for this proposal. Future slices should demonstrate deterministic replay, duplicate idempotency, explicit ownership and boundary tests. Revisit on measured resource contention, recovery objectives, independent scaling needs or a demonstrated isolation requirement. Specify migration, rollback and failure tests before distributing execution. Record when a simpler design remains adequate and when an experiment fails.
