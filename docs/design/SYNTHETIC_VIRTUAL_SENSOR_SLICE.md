# First vertical slice: a synthetic beverage question

**Proposed implementation, not implemented by this documentation PR.** Scope: synthetic event → cheap detector → virtual sensor → selective additional inference → Bayesian belief update → auditable replay. Reuse LIVE-004/005/008/009/012 and add only the infrastructure tasks identified in the backlog.

## Smallest executable milestone

Use one in-process replay runner, a static registry, a finite joint hypothesis table and a mock image provider. Reuse the starter's replay conventions where suitable without asserting its existing event schema already meets the proposed contracts. No camera access, audio capture, cloud requests, credentials, human prompts, glucose forecasts or insulin-dose calculations.

A synthetic fixture supplies reference-only truth labels and separately accessible observations. Truth labels are evaluation data and must not enter the detector, planner or estimator input. Pin the fixture, prior, observation-likelihood, question, provider and policy versions. Use a logical clock and fixed seed where needed.

The first executable milestone covers the principal sequence plus missing-camera and repeated-evidence controls. The remaining variants below are required before claiming the complete scenario family is validated. It is not a production plugin ecosystem or full physiological twin.

## Principal sequence

| Step | Input / operation | Auditable result |
| --- | --- | --- |
| 1 | Adapter replays an authorized synthetic refrigerator-door contact event | Immutable observation and low-cost change trigger |
| 2 | A lightweight detector evaluates a synthetic audio-feature value | Versioned virtual-sensor evidence: sound consistent with a can opening, with uncalibrated score semantics |
| 3 | Finite Bayesian model applies documented synthetic observation likelihoods | Prior and posterior over beverage identity, consumption/quantity and actor hypotheses; no confirmed meal |
| 4 | Planner compares no action, another redundant audio feature and selected image classification | Decision explains why the permitted image question offers more expected value within the fixture budget |
| 5 | Mock image provider returns a typed result consistent with regular cola | New evidence retains the selected image reference, question version and dependencies; score is not silently treated as a likelihood |
| 6 | The estimator incorporates the joint/dependent evidence model | Revised alternatives: regular/diet/unknown beverage and handled-only/consumed/unknown actor remain possible |
| 7 | Synthetic before/after scale observations show a container-weight decrease | Consumption-volume belief changes but spilling, sharing and a different consumer remain possible; retain zero-consumption possibility where warranted |
| 8 | Planner finds no sufficiently useful permitted next observation | Stop reason, remaining uncertainty, final BeliefSnapshot and complete audit trail |

A container weight change is evidence of mass leaving the container, not proof that a particular person drank it. Any conversion to volume is an explicit fixture assumption with uncertainty. Identity, actor and amount are factors of a joint state, not mutually exclusive labels that accidentally exclude combinations.

## Bayesian and acquisition simplifications

Use a small enumerated joint state with a documented prior and synthetic likelihood tables, including a shared-event variable or explicit joint likelihood for dependent features. Compare updates against a separately calculated reference posterior. State probabilities must be nonnegative, finite and normalize to one within a declared tolerance (initial numerical target: `1e-9`). Zero-likelihood/impossible-evidence cases return mismatch/unknown rather than divide-by-zero or certainty.

The first planner uses a deterministic, documented benefit/cost heuristic. Rank only feasible authorized candidates. Stop is an explicit candidate. A fixture may cap advanced image analysis at one mock call; that is a test constraint, not a production budget. Record predicted benefit, observed posterior change and independently scored truth performance separately. Do not claim an entropy reduction proves the chosen observation was useful.

Replay may reuse recorded mock results. A later live provider would require versioned response capture to reproduce a run; rerunning a nondeterministic remote model is not deterministic replay.

## Required alternative cases

| Case | Expected behavior / falsifiable check |
| --- | --- |
| Sugar-free beverage | Diet explanation remains available and gains support under the matching fixture; regular-cola assumptions do not hard-code the outcome |
| Opened but not consumed | Opening evidence alone cannot assert consumption; zero-consumption probability remains represented |
| Partial consumption | Retain quantity uncertainty and alternatives to complete consumption |
| Another person present | Actor attribution stays ambiguous unless person-specific evidence exists |
| Missing camera | No provider call against an unavailable source; choose another permitted source or stop |
| Contradictory modalities | Preserve contrary evidence and competing explanations; no silent evidence deletion |
| Repeated correlated evidence | Exact duplicates leave the posterior unchanged; overlapping but distinct evidence follows the explicit dependence rule, including parent/child derivations |
| Provider timeout | Respect logical deadline, record timeout/cost and retain uncertainty; no unbounded retry |
| No useful next observation | Stop with zero unnecessary advanced calls; explain expected-value or budget rejection |
| Confidently wrong model | A biased fixture can initially produce wrong confidence; subsequent surprising independent evidence triggers the declared predictive-mismatch check. If no diagnostic evidence exists, do not claim the system can always detect its error |
| Permission revoked mid-run | Cancel pending acquisition, prevent transmission, and handle late results according to declared permission/retention policy |
| Budget exhausted / provider malformed or refusing | No over-budget dispatch; invalid or refused output is not admitted as negative evidence |

## Acceptance and comparison

- Principal sequence yields linked observation, sensor-result, acquisition-decision and belief records; every inference reaches its immutable source leaves.
- All acquisition calls pass purpose/destination permission and resource checks; the missing/revoked/no-value cases make zero forbidden calls. Human prompts and network calls are zero throughout.
- The independent posterior reference agrees within the declared numerical tolerance; duplicate replay is idempotent and chronological cutoffs prevent future-evidence leakage.
- Replaying identical fixtures/versions produces identical semantic output, including selected actions, stop reason, posterior and simulated costs.
- Every snapshot has `shadow_only=true`, `may_actuate_insulin=false`; physiological forecast fields are explicitly unavailable in this context-only slice. No dosing command object exists.
- Compare cheap-only, fixed-escalation and progressive policies using identical held-out fixture ensembles and resource assumptions. Report Brier/log loss, event precision/recall, false confidence, calls and logical latency. Show no-value/redundancy cases avoid unnecessary calls. Do not require the progressive policy to win every scenario; publish tradeoffs and negative results.
- Calibration claims require enough labelled cases and a stated evaluation procedure. A single happy-path trace does not establish calibration or clinical validity.
- Track energy, bandwidth, monetary and attention costs as simulated estimates or unavailable until measured; do not report guessed hardware performance as measured. Downstream physiological predictive benefit remains future work under LIVE-007/010.

Implementation is complete only after the chosen milestone's tests and limits are reported. This document specifies the future work; existing seven starter tests do not exercise these behaviors.
