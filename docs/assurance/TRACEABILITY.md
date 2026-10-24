# Proposed lightweight claim traceability

Status: **Proposed supplement**, not an accepted safety case. See [ADR 0002](../decisions/0002-lightweight-assurance-traceability.md). Procedural reference: [PR #3 methodology at 5886ed6](https://github.com/thebookoftheway3/project-live/blob/5886ed63c37fed876dd0a54c20ebd3c7ef224905/docs/METHODOLOGY.md), still unmerged.

Use **Claim → Hazard → Safeguard → Verification evidence**, with an explicit argument explaining why each item supports the next. A requirement specifies an obligation; a claim asserts a scoped property to assess. Neither a specification, a listed safeguard nor a passed test alone establishes system safety. Start with the [nine claim rows](CLAIMS_MATRIX.md); no special database or tool is required.

## Minimal record

| Record | Required content |
| --- | --- |
| Claim `C-nn` | Bounded property/invariant; requirement/decision source and acceptance status; component/configuration, intended use, assumptions and exclusions; responsible role and review status. Avoid “the system is safe.” |
| Hazard `H-nn` | Plausible violation, triggering conditions, affected people/data/research validity and consequence. Include bypasses, correlated faults and misuse, not only happy-path errors. |
| Safeguard `S-nn` | Structural, technical or procedural mechanism, enforcement location, dependencies and limits; mark proposed, implemented or inspected. A policy is not an isolation mechanism. |
| Verification plan `V-nn` | Stimulus, observation points, expected result, coverage and method (test, inspection, analysis, human evaluation). A plan is not evidence. |
| Evidence `E-nn` | Exact subject revision/configuration, test/procedure and tool/fixture versions, execution date, observed result and artifact/location, coverage, limitations and linked C/H/S/V IDs. Record failures and unavailable evidence. |
| Review | Who evaluated the argument, actual expertise/independence, unresolved objections, validity conditions and next review trigger. Do not invent assigned people or approvals. |

One row may reference several hazards or safeguards; IDs are local to this assurance record, not replacement requirement IDs. Keep bidirectional links in the matrix and evidence index: from a requirement find claims, safeguards and evidence; from an artifact find the supported claims and assumptions. Shared evidence is reused by ID, not counted as independent confirmation twice. An absent artifact stays explicitly absent.

Recommended claim states: **proposed**, **unsupported**, **limited evidence**, **contradicted within stated scope**, or **supported for stated scope after review**. Evidence outcomes are **pass**, **fail/counterexample**, **inspection finding**, **not run**, or **stale**. These are separate from ADR states. Do not declare a broad claim supported by aggregating passing test counts. This initial matrix has no claim marked system-level supported.

## Using the lifecycle

During problem/evidence review, identify affected claims and what could falsify them. During alternatives/decision, compare safeguards, including removing a capability instead of adding a gate. At contract time define prohibited events and observation points. At implementation/test time record actual artifacts and counterexamples. During review verify both directions of traceability, challenge assumptions and assess sufficiency. At an explicitly authorized merge record remaining limitations; retrospective learning appends corrections and invalidates stale evidence.

Before claiming a forbidden event did not occur, attempt the triggering condition and measure the relevant effect. Zero log entries can mean a broken observer. Validate the observation mechanism with a harmless synthetic positive control (such as a mock write counter), then attempt denied behaviour and observe all relevant paths. Tests exercise bounded cases; static/dependency analysis, capability inspection, fault injection and independent deployment review provide different evidence. Formal analysis also depends on model assumptions and correspondence to the deployed system.

## Evidence validity and change impact

Bind evidence to code, contracts, configuration, dependencies, model/permission versions and fixture identity. On changes to any relied-on safeguard or assumption, mark affected conclusions stale pending impact review. If relevant artifacts are byte-identical, explain why previous evidence still applies; do not reset its date. Preserve adverse results and superseded interpretations. Deleted or inaccessible sensitive evidence reduces reproducibility; public metadata must not disclose private inputs or allow their reconstruction.

Review sufficiency before capability expansion, release, changed data use or human exposure. No universal number of passing tests or confidence threshold closes a hazard. A reviewer must state what the evidence establishes, what it does not, and why residual uncertainty is acceptable for the narrowly proposed research activity. This is not clinical risk acceptance.

## Proportionate assurance

- **Synthetic offline research:** use affected claim rows, existing tests, targeted negative tests and source inspection. No committee or certification claim.
- **Personal data, external providers, untrusted code or shared hardware:** require data-flow/threat analysis, enforced capabilities, revocation and recovery tests, privacy review and appropriately qualified independent scrutiny before use. Record a missing reviewer as a gap.
- **Human-visible or prospective studies:** add misuse, comprehension, interruption/attention, non-interference and study-specific oversight evidence. Labels do not eliminate behavioural influence.
- **Any proposal affecting actual treatment:** stop this research progression and require a separately scoped control, clinical and governance assessment. A more formal safety-case method may be necessary, but this document neither specifies an insulin gate nor authorizes the work.

NASA's public [Systems Engineering Handbook appendices D, E and I](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) provide an independent methodological reference for identifiable requirements, verification matrices and validation planning. This small record adapts that general discipline to LIVE's scale; it asserts no NASA conformance and imports no aerospace or traffic safety assurance.
