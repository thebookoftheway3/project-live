# ADR 0002: Add lightweight claim–hazard–safeguard–verification traceability

- Status: **Proposed**
- Proposed: 2026-10-24
- Decision date: None; responsible decision-maker: maintainer, pending review
- Actual independent human reviewers: None recorded
- Scope: research methodology; no runtime, treatment or administrative change
- References: main R00/R01/R03/R10/R12/R17–R21 and LIVE-016; [assessment](../assurance/TRANSFER_ASSESSMENT.md), [method](../assurance/TRACEABILITY.md), [matrix](../assurance/CLAIMS_MATRIX.md)
- Related: PR #3 methodology and ADR 0001 remain proposed/unmerged; this ADR neither accepts nor supersedes them
- Supersedes / superseded by: None

## Problem and evidence

LIVE already separates research from treatment and asks contributors to record tests. PR #2 specifies detailed invariants whose implementations and acceptance tests do not yet exist. PR #3 proposes a disciplined lifecycle. Neither provides a compact, bidirectional argument from a particular claim through a violation and enforceable safeguard to versioned evidence.

The transfer assessment supports using that discipline while rejecting imported control authority, reversible-treatment assumptions and unsupported risk-equivalence claims. Current tests illustrate the gap: deterministic replay does not prove absence of future-information leakage, and a frozen record does not guarantee its payload is immutable. The included counterexample is a reason to keep claims falsifiable, not to implement unrelated fixes in this PR.

## Alternatives

| Alternative | Benefits | Costs and limitations |
| --- | --- | --- |
| Existing test-driven development only | Familiar, minimal paperwork, close to code and regression behaviour. | Can omit system hazards, privileged bypasses and assumptions; passing cases can be mistaken for broad assurance. Tests remain necessary under every option. |
| Lightweight claim/invariant traceability (recommended) | A few Markdown records connect requirements, hazards, safeguards, evidence and gaps; preserves counterexamples and supports impact review. | Needs ownership and upkeep; not exhaustive or independently sufficient for a safety claim. Avoid ceremonial rows for trivial edits. |
| More formal safety-case methods now | Structured argument, explicit assumptions and independent challenge can improve assurance for consequential capabilities. | Current implementation offers little evidence to populate a credible case; specialist work, model validation and maintenance add cost. A formal-looking document can create false confidence. |
| Defer all formalisation | Keeps immediate work small while designs evolve. | Allows unsupported claims and missing negative requirements to accumulate before live data, external code or human exposure. Later reconstruction of rationale is unreliable. |

## Proposed decision

Adopt the lightweight supplement for changes to research boundaries, epistemic/temporal meaning, permissions or other consequential invariants. Link existing requirement and contract IDs; do not duplicate PR #2 schemas or PR #3 governance. Keep claims scoped, safeguards marked by implementation state, plans separate from executed evidence, and failures visible. Require an explicit explanation of how evidence supports a claim and where it does not.

Use the initial nine-row matrix to trial the method. No new software dependency, service, review committee, clinical permission or general-purpose actuation gate is introduced. The ADR stays proposed until a maintainer explicitly records acceptance after review. Number 0002 follows the proposed 0001 in PR #3; reconcile the eventual register without creating a competing copy in this main-based branch.

## Assurance escalation and acceptance criteria

Increase assurance before introducing personal data, live acquisition, untrusted executable plugins, external providers, shared treatment hardware, human-visible advice or broader distribution. Require appropriately qualified independent review, concrete isolation/privacy evidence, fault injection and study-specific human-factors validation as relevant. If no reviewer or evidence is available, record the gap and defer capability expansion. Actual treatment influence requires a separately authorized control/clinical program; success under this method is not permission to start one.

Trial acceptance requires reviewers to traverse an affected claim to its evidence and back, distinguish proposed safeguards from implementation, identify stale/contradictory evidence, and find the recorded limits without reconstructing the conversation. Evaluate upkeep time and whether the method catches a real gap; a longer table is not success. No reviewer has yet established those acceptance results.

## Consequences, reversal and reconsideration

Benefits are clearer review and fewer unsupported assurance statements. Costs are a small evidence-maintenance burden and a risk of treating links as proof. Mitigate that by retaining counterexamples and sufficiency review, not scoring by row coverage. Keep public records privacy-safe; restricted source material does not become publishable because it supports a claim.

After the first bounded synthetic implementation using the method, review missed hazards, stale-link frequency, review usefulness and maintainer attention cost. Simplify if bookkeeping obscures rather than clarifies decisions. Escalate to a more formal safety-case approach when composed failure modes or capability/exposure require it. Any replacement should preserve historical evidence, dissent and reasons for changing course; no runtime rollback is needed for this documentation proposal.
