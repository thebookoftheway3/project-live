# Separate proposal: evaluate an Adaptive Perception Graph

Status: **Proposed future architectural issue; not approved or implemented.** Open a separate issue after the governance foundation is established. Do not append this design to PR #2. This record supplies an issue-ready scope without consuming the governance PR's expected number.

## Motivation and evidence needed

Could explicit scheduling of dependent perception questions improve useful information per unit of compute, latency, privacy exposure and human attention? The current synthetic starter provides no measurements establishing that a graph scheduler is needed. Relate any future evaluation to R00, R08, R13, R15 and R17 and to the contract sketches integrated through PR #2, resolving concrete APIs through their own decisions.

## Alternatives

Compare a static sequence, a simple rule-based scheduler, no additional acquisition and a bounded graph design. Evaluate matched synthetic workloads before choosing infrastructure. A graph should be rejected or deferred if its complexity does not yield useful measured benefit.

## Affected boundaries and risks

Consider virtual-sensor execution, evidence provenance, acquisition and historical investigation, the single logical Bayesian belief state, and simulation/evaluation. Address cycles, duplicate and correlated evidence, stale results, permission revocation, cancellation, starvation, resource limits, missing history and false confidence. Preserve chronological evaluation and deterministic replay. No real sensing, external inference transmission, hardware purchase, distribution platform or actuation is authorized by this proposal.

## Acceptance criteria for the architecture issue

- Document problem, evidence, alternatives, affected contracts and unresolved questions in an ADR.
- Specify scheduling semantics, ownership, stopping/unknown behaviour and testable permission/resource invariants.
- Plan chronological comparisons and ablations with simpler baselines; distinguish simulated costs from measured values.
- Define meaningful information/accuracy improvements, false-confidence checks and human-attention costs before implementation.
- Separate architecture review, bounded synthetic implementation and later evaluation into focused PRs.

Open questions include whether a graph is needed at all, how its decisions are explained, which costs are measurable and how shared dependencies avoid repeated evidence counting. A proposal must remain correctable by negative results.
