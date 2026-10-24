# First vertical slice: a synthetic beverage question and historical investigation

**Proposed implementation, not implemented by this documentation PR.** Scope: synthetic event → cheap detector → virtual sensor → selective fresh or historical investigation → Bayesian belief update → auditable replay. Extend the same LIVE-022 slice and reuse LIVE-004/005/008/009/012/019. LIVE-023 supplies only the minimal searchable evidence index; no separate investigation engine is introduced.

## Complete milestone and incremental delivery

Use one in-process replay runner, a static registry, a finite joint hypothesis table, an indexed synthetic history and a mock image provider. Reuse the starter's replay conventions where suitable without asserting its existing event schema already meets the proposed contracts. A supplied synthetic forecast/observation pair triggers a simulated glucose-prediction mismatch; this does not implement a physiological forecaster. No camera access, audio capture, cloud requests, credentials, human prompts, executable glucose-forecasting model or insulin-dose calculations.

A synthetic fixture supplies reference-only truth labels and separately accessible observations. Truth labels are evaluation data and must not enter the detector, planner or estimator input. Pin the fixture, prior, observation-likelihood, question, provider and policy versions. Use a logical clock and fixed seed where needed.

Deliver small independently reviewed increments, beginning with a synthetic detector-to-belief/replay path if useful. That first increment is not LIVE-022 completion. The complete milestone covers the principal sequence, the required 12:30/14:30 historical phase below, and its leakage, unavailable-history, correlated-evidence and consent/retention controls, together with the existing missing-camera/repeated-evidence controls. The remaining variants below are required before claiming the complete scenario family is validated. Historical investigation is foundational, not an optional analytics follow-up. This is not a production plugin ecosystem or full physiological twin.

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

## Required historical phase: what was known then versus learned later

Use a second timeline of the same beverage fixture. Unlike the fresh-investigation path above, the early event is deliberately not escalated. Display times below are 24 October 2026, Europe/Stockholm (`+02:00`); record UTC instants and ordering in the fixture. The synthetic payload references contain no real media. A scripted forecast targeting 14:30 is sealed with the 12:30 snapshot before the later observation is revealed to the runner; hidden truth stays evaluation-only. Declare each representation's retention/consent window explicitly, rather than assume a recording exists indefinitely.

| Time | Available evidence and operation | Immutable record / expected result |
| --- | --- | --- |
| 12:30:00–12:30:02 | Kitchen contact/audio-feature event is recorded; a synthetic frame reference is ingested and actually available by 12:30:01. Cheap detection finds possible activity, with low current expected value for deeper investigation | `online_1230` at 12:30:02 records actual admitted cheap evidence, versions, cutoff and a stop/no-escalation decision. The unused frame may be retained under the fixture's explicit policy; it is not yet a beverage interpretation |
| 14:30:00 | A scripted prediction/observation mismatch becomes available. The toy model considers an earlier beverage event, activity-related effects, sensor/model error and unresolved alternatives | Freeze `online_1430`, including the mismatch already admitted and the original forecast ID/cutoff. No result from the coming historical query or provider is present |
| 14:30:05 | The same planner compares a fresh sample, bounded history query, similar-episode search and stop under one budget | Select the 12:00–13:00 historical window because the declared fixture benefit/cost predicts it can distinguish the alternatives. Log all candidates, the mismatch trigger and selection reason |
| 14:30:06 | Indexed retrieval checks source/representation compatibility, knowledge-as-of boundary, current permission and retention | Return the permitted 12:30 low-interest event and available payload references, with coverage/completeness. Metadata-only or expired-history variants instead return no usable frame |
| 14:30:10–14:30:21 | After re-ranking, one mock provider analyzes the selected historical frame through the same virtual-sensor contract | Create `interpretation_later` targeting the 12:30 event, execution ending at 14:30:20 and actual result availability at 14:30:21. Record input leaves, model/question/sensor versions and any earlier interpretation it revisits |
| 14:31:00 | The Bayesian model incorporates the newly learned interpretation with later observations via the declared joint trajectory likelihood | Create `smoothed_1230_at_1431` linked to `online_1230` and `online_1430`; optionally issue a distinct `current_1431`. Original snapshots, original forecast and their cutoffs remain byte-for-byte unchanged |
| Replay | Render as-was and retrospective views using their own manifests and cutoffs | Show what was available, what was actually used, why the old event became relevant, which interpretation changed and what remains unknown |

The unexpected glucose observation is a fixture stimulus, not a diagnosed cause. A revised probability for consumption is not proof that consumption caused the mismatch, and says nothing about the outcome of an unperformed insulin action. The toy hypothesis/likelihood tables are synthetic research assumptions.

## Historical controls and proposed tests

These are acceptance tests to implement with LIVE-022, not tests claimed to exist today.

| Test | Setup | Required assertions |
| --- | --- | --- |
| Future-information leakage | Give an old event a late `available_at`; also add the 14:30:21 derived result and a similar-episode feature/outcome learned later | As-was 12:30/14:30 replay excludes each later object from queries, rankings and model inputs, even when event/recording time precedes the cutoff. Original snapshot/forecast digests and original scoring inputs are unchanged. Retrospective output explicitly has a new cutoff |
| Retained but unused evidence | Frame is available at 12:30, but no image analysis ran | Original snapshot does not contain the later image interpretation; availability alone is not admission or knowledge of a feature |
| Unavailable history | Remove the retained frame but keep permitted metadata, or mark history unavailable | No image-provider call; return incomplete-history reason and choose another worthwhile permitted action or stop. No-match does not establish no consumption |
| Correlated historical evidence | Query the same leaves twice; reinterpret a frame with a newer sensor; include the mismatch in both trigger context and belief input | Identical replay is idempotent. Related interpretations and the triggering observation are jointly modelled/replaced/capped by the declared dependence rule, not multiplied as new independent evidence |
| Consent/retention denial | At retrieval or dispatch, revoke the investigation purpose or expire the payload/index entry | Zero denied payload reads, transmissions and inference calls; no consent resurrection in as-was replay. Return only permissible denial/completeness metadata. Mark old replay incomplete if required evidence was legitimately erased |
| Newly invented virtual sensor | Register `beverage_sensor_v2` on the next day; explicitly retain compatible synthetic inputs until that bounded backfill run | Append a new versioned interpretation with next-day execution/availability; retain v1/original snapshots. As-was replay cannot use v2 or its features. An incompatible/expired record yields no fabricated output |
| Similar historical episodes | Index a small labelled synthetic episode set with versioned features and availability; choose a time cutoff | Permission/as-of filters precede similarity ranking; results reference original episodes/leaves and are candidates for analysis, not causal evidence. Later labels are excluded from earlier predictor inputs |

Use a separately calculated finite-state trajectory reference for both filtering and smoothing. The fixture's declared likelihoods must produce a distinguishable retrospective update; retaining uncertainty is still required. Compare v1/v2 interpretations only with explicit model/assumption differences and permitted common inputs. Backfill reproducibility uses pinned manifests and mock results, not repeated calls to a changing model.

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
- Every snapshot has `shadow_only=true`, `may_actuate_insulin=false`; the mismatch stimulus references a supplied synthetic forecast, while computed physiological forecast fields remain explicitly unavailable. No dosing command object exists.
- Compare cheap-only, fixed-escalation and progressive policies using identical held-out fixture ensembles and resource assumptions. Report Brier/log loss, event precision/recall, false confidence, calls and logical latency. Show no-value/redundancy cases avoid unnecessary calls. Do not require the progressive policy to win every scenario; publish tradeoffs and negative results.
- Calibration claims require enough labelled cases and a stated evaluation procedure. A single happy-path trace does not establish calibration or clinical validity.
- Track energy, bandwidth, monetary and attention costs as simulated estimates or unavailable until measured; do not report guessed hardware performance as measured. Downstream physiological predictive benefit remains future work under LIVE-007/010.
- Compare fresh-only and historically enabled policies at identical knowledge cutoffs, retention assumptions and budgets. Report query/inference cost, unavailable-history rate, changed hypothesis probabilities and explanation uncertainty separately from original predictive scores. Only newly issued future predictions may benefit prospectively from an investigation.
- Historical acceptance requires frozen `online_1230` and `online_1430` digests, traceable later interpretation/smoothing IDs and passing the leakage/unavailable/correlation/consent-retention controls. Retrospective fit must never be presented as an improved original forecast or proof of causation.

Implementation is complete only after the chosen milestone's tests and limits are reported. This document specifies the future work; existing starter tests do not exercise these behaviors.
