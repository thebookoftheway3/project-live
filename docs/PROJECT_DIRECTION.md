# Project LIVE — direction and open decisions

Updated 24 October 2026. Integration revision 3 extends the Bayesian blueprint with the project-supplied general-purpose virtual-sensor and progressive-inference addendum.

## Governing direction

- Public open-source research for people with diabetes, guided by human life and attention returned.
- Retain Revision 2's Bayesian sequential inference: one joint belief over plausible hidden states and modes, explicit uncertainty and auditable updates.
- A virtual sensor is defined by the question it answers, not its hardware. Authorized relevant streams can support replaceable, composable interpretations; none is a fact generator.
- Separate reusable sensing infrastructure from the diabetes-specific model. Reuse elsewhere is possible, not a commitment to build other applications now.
- Actively seek useful evidence. Begin with cheap detection, identify a relevant gap, then selectively escalate source/question/model only within permission, resource, privacy and attention limits. Stopping with UNKNOWN is valid.
- Preserve raw observations, derived evidence, hypotheses, real actions, predictions, shadow decisions and outcomes separately. Correlated or reused evidence must not manufacture certainty.
- Keep inference providers replaceable. Local processing and mocks are first-class; Decisions is an optional researched candidate, not a dependency.
- Preserve the non-actuating boundary and independent treatment operation. No executable dosing commands or silent treatment changes.

## Current task scope

This change updates architecture, specifications, requirements and backlog on a feature branch with a focused PR. It proposes, but does not implement, the first synthetic vertical slice. It does not refactor working code, change CI, add credentials, make paid model calls, acquire live observations or change the treatment boundary.

The next implementation delivery should be the smallest end-to-end example: synthetic event → cheap detector → virtual sensor → selective mock inference → Bayesian belief update → auditable replay. Deliver minimal in-process subsets of the backlog tasks together; do not build a large framework before exercising the complete path. The separate Loop simulator investigation can proceed independently and is not a prerequisite for this no-device slice.

## Unresolved engineering decisions

| ID | Decision | Proposed starting point / evidence needed |
| --- | --- | --- |
| D08 | Long-term human/automation control | Remains open; separate discussion and validation |
| D09 | Serialization, units, clock and temporal-window semantics | Small versioned envelopes; specify timezone, observed/received times, skew and late-event replay before implementation |
| D10 | Virtual-sensor composition and dependence | Static acyclic registry; retain raw leaf overlap; choose joint likelihood or conservative replacement/capping with an explicit test oracle |
| D11 | Likelihood and calibration mapping | Synthetic observation tables first; model scores are not likelihoods without measured or declared mapping |
| D12 | Value-of-information policy and stopping | Deterministic versioned heuristic first; compare to cheap-only/fixed escalation before richer optimization |
| D13 | Resource units, limits and attention costs | Explicit per-run fixture budgets first; production weights, deadlines and retry limits require measurements |
| D14 | Permissions, retention, other people and revocation | Purpose/destination checks at source and dispatch; decide cancellation, late-result handling and deletion policy before real data |
| D15 | Provider selection and capability negotiation | Mock/local first; reverify Decisions account support, SDK, costs and data controls before any live adapter |
| D16 | Human clarification timing and modality | Still open; not in first slice. Unanswered means unknown; attention is a cost |
| D17 | Generalisation and physiological models | Evaluate intended populations/devices, priors and person-specific calibration; no universal-performance claim |
| D18 | Mismatch/OOD thresholds and escalation | Define synthetic surprise test first; establish false-positive/false-negative behavior on held-out data |

Hardware choices and live CGM interfaces remain unresolved in their existing tracks. These are genuine design choices, not reasons to re-ask whether active evidence acquisition is wanted.

## Source handling

`PROJECT_BLUEPRINT.md` integrates the original Bayesian specification and latest architectural addendum. Original supplied documents are retained locally and identified in `SOURCE_MANIFEST.json`. Public documents exclude personal history and treatment records.

Embedded instructions are specification material, not standalone authorization for external actions. The project owner's request to incorporate this update defines this architecture pass. Verify external API claims before adopting provider-specific request shapes. Historical starter plans remain subordinate proposals.
