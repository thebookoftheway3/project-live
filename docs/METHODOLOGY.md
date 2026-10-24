# Engineering methodology

This lifecycle supports R00, R10, R12, R17–R21 and LIVE-016 in the [requirements](requirements/LEDGER.md) and [backlog](BACKLOG.md). Scale the record to the change; a trivial correction can use a short PR. Significant proposals use an issue and [ADR](decisions/README.md).

**Problem → Evidence → Alternatives → Decision → Contract → Implementation → Tests → Review → Merge → Retrospective learning.**

| Stage | Minimum useful record |
| --- | --- |
| Problem | Who is affected, what fails or remains unknown, intended behaviour, scope and acceptance criteria. |
| Evidence | Observations, source/provenance, quality, permission and limitations. Separate observation from interpretation; identify assumptions and observations that could falsify them. |
| Alternatives | Include doing nothing and a simpler baseline. Compare benefit, complexity, failure/recovery, privacy, operational and human-attention costs. |
| Decision | Rationale, dissent, uncertainty and reopening criteria; numbered ADR for interface, boundary or invariant changes. |
| Contract | Versioned inputs/outputs, ownership, timing, evidence dependencies, errors/unknowns, permission limits and acceptance tests. |
| Implementation | Smallest coherent change behind explicit boundaries; synthetic inputs first. A proposed design is not implemented behaviour. |
| Tests | Exact commands, versions, fixtures and actual outcomes, including failures and omitted checks. Compare with baselines and quantify limitations. |
| Review | Traceability, correctness, security, accessibility, attribution and claims checked by the appropriate people; disclose missing expertise and independence. |
| Merge | Explicit maintainer decision after checks and review; no automatic merging. Record unresolved limitations and follow-ups. |
| Retrospective learning | What changed our understanding, failed experiments, negative results, operational/attention cost and what would trigger reconsideration. Append corrections without erasing history. |

## Research evidence rules

Preserve original observations and later reinterpretations as separate versioned records, within authorized retention limits. Record event time, availability time, inference time, model version, evidence cutoff and provenance. Erasure or unavailable evidence makes replay incomplete; do not reconstruct forbidden data or claim full reproducibility when inputs are gone.

Predictive models require chronological evaluation: freeze training/tuning windows, model versions and predictions before scoring later outcomes. Features, late-arriving data and later reinterpretations must not leak across the evaluation cutoff. Report retrospective explanation separately from prospective prediction; an improved historical explanation cannot improve an already-issued forecast. Evaluate held-out people and contexts where relevant before generalisation claims.

Test correlated inputs, duplicate observations, shared upstream evidence, missingness, contradictory signals, distribution shift and confidently wrong models. Retain raw-leaf dependencies to prevent double counting. Report calibration and proper predictive scores, not confidence alone. State which assumptions cannot yet be falsified with available data.

Compare added sensors and inference against passive acquisition, simpler models and no new sensor using matched evaluation windows and ablations. Measure incremental useful information and prediction quality, false confidence, latency, availability, compute/energy, privacy and human attention. Entropy reduction alone does not establish usefulness. Report interruptions, effort and recovery burden as first-class system costs; separate measured values from simulated estimates or unknowns.

Publish negative and null results with methods and limitations, including when complexity fails to beat a baseline. Keep only privacy-safe evidence in the public repository; reference restricted evidence without disclosing it. Synthetic demonstrations test specified behaviour under stated assumptions. They are neither real-world validation nor evidence of the outcome of an unperformed treatment intervention.
