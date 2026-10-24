# Requirements ledger — virtual-sensor integration revision 3

Source: the governing blueprint plus explicit project direction. PR #2 accepts R22–R30 as design requirements; their safeguards remain unimplemented and concrete API sketches remain proposed. Documentation acceptance is not implementation or validation.

| ID | Requirement | Status | Required evidence |
| --- | --- | --- | --- |
| R00 | Return attention, preserve human competence and support recovery | Confirmed goal | Workload, sleep, interruption and recovery evaluation |
| R01 | Preserve independently operating treatment during initial research | Initial boundary | No runtime pump transport; non-interference evidence for future adapters |
| R02 | Interpret context with history | Illustrative starter only | Temporal inference and prospective comparisons |
| R03 | Respect control over sensing resources and data | Design pending | Permissions, retention, provenance and availability |
| R04 | Accessible low-burden interaction | Design pending | User research across contexts and abilities |
| R05 | Modular home/office/car/mobile context | Environment tracking only | Real adapter validation and context uncertainty |
| R06 | Environment cannot grant dosing authority | Synthetic tests pass | Preserve boundary in each implementation |
| R07 | Treatment remains independent of experimental infrastructure | Architectural requirement | Dependency and failure analysis |
| R08 | Progressive, replaceable sensor integrations independent of hardware modality | Initial schema only | Add a sensor on an existing representation without rewriting the belief core; explicit missing-device behavior |
| R09 | Read-only CGM acquisition | Not implemented | Supported interfaces, time quality and non-interference |
| R10 | Distinguish observations, beliefs, actions and outcomes | Partial replay; temporal design not implemented | Versioned schemas; event/recording/ingestion/actual-availability/execution times; immutable original cutoffs and exact admitted manifests |
| R11 | Distinguish command intent, delivery and uncertain effect | Design pending | Confirmed action semantics and ambiguity tests |
| R12 | Initial software cannot actuate insulin | Synthetic implementation | No real pump client or credentials; boundary tests |
| R13 | Select the next useful fresh or historical investigation | Confirmed foundational requirement; design extended | One policy ranks fresh samples, retained-data analysis, historical and similar-episode queries, historical sensor runs and stop under shared budgets/permissions; log mismatch trigger, rationale, cost and changed understanding |
| R14 | Carefully design possible clarification prompts | Open design | Timing, accessibility, burden and unanswered cases |
| R15 | Maintain joint Bayesian belief over hidden states and discrete modes | Required; not implemented | Priors, transitions, likelihoods, updates and known-state reference cases |
| R16 | Report posterior predictive distributions and competing explanations | Required; not implemented | Horizon-specific distributions, multimodality and evidence audit |
| R17 | Model dependent evidence and source missingness | Required; not implemented | Shared errors, lag, repeated frames, cross-modal correlation, parent/child evidence overlap and unavailable signals; exact duplicates idempotent |
| R18 | Expose model mismatch, OOD and calibration status | Required; not implemented | Prospective proper scores, interval coverage and rare-context checks |
| R19 | Audit BeliefSnapshot fields and temporal views | Required; not implemented | Target time, inference kind, execution/cutoff, exact manifest, model/sensor versions, original/parent links, hypotheses and shadow flags; original online snapshots remain immutable |
| R20 | Enable open reuse and contributions for the diabetes community | Public foundation | Open-source license, accessible documentation and contribution workflow |
| R21 | Separate per-person calibration from general claims | Required; not validated | Population scope, held-out people/contexts and subgroup evaluation |
| R22 | Generic adapters for scalar/time-series/media/event/log evidence | Required; not implemented | Timestamp/unit/quality/permission/availability contract across heterogeneous fixtures; no assumption that accessibility grants authorization |
| R23 | Question-defined, composable virtual sensors, including historical execution | Required; not implemented | Stable version, historical input compatibility, actual availability, provenance and purpose checks; acyclic raw-leaf lineage and append-only reinterpretations |
| R24 | Event-driven progressive inference | Required; not implemented | Cheap detector first; selected escalation only; repeated/no-value cases avoid unnecessary work; explicit deadline and stop behavior |
| R25 | Provider-neutral bounded inference | Required; not implemented | Local and mock providers interchange behind one contract; typed unknown/refusal/timeout/invalid outputs; cloud outage cannot require unavailable provider or enable actuation |
| R26 | Permission, privacy and resource enforcement | Required; not implemented | Check purpose/destination and revocation at acquisition/dispatch/acceptance; zero prohibited transmissions; budget/cancellation tests; attention cost explicit |
| R27 | Evaluate incremental virtual-sensor and acquisition value | Required; not implemented | Same-case passive/fixed/progressive comparisons; calibration, false confidence, precision/recall, calls, latency, resource and downstream prediction metrics; measured versus simulated provenance; preserve negative results |
| R28 | Preserve filtering, smoothing and as-was knowledge separately | Required; not implemented | Original 12:30/14:30 snapshots and forecast remain unchanged; new retrospective target/cutoff/view; late evidence and later versions cannot enter original prediction inputs or episode ranking |
| R29 | Run new virtual sensors on authorized compatible retained data | Required; not implemented | Bounded versioned backfill with pinned input/result manifests; new execution/availability times, linked prior interpretations and reproducible comparisons; no overwrite or independent double counting |
| R30 | Minimal permission-aware searchable evidence memory | Required; not implemented | Synthetic time/source/availability index plus episode references; filter consent/retention before ranking and access; distinguish no-match/unavailable/expired/denied/incompatible and mark incomplete replay |

These requirements extend R08/R10/R13/R15/R17/R19 rather than define a competing sensing or belief system. R28–R30 make active historical investigation foundational, not optional analytics. The smallest contracts, synthetic cases and requirement-to-task mapping are in the architecture and backlog. Current tests do not establish these specified capabilities.

Verification uses the [assurance matrix](../assurance/CLAIMS_MATRIX.md): R01/R07/R12 → C-01; R10/R19/R23/R29 → C-02/C-03; R03/R26/R30 → C-04/C-05; R17/R23/R27 → C-06; R10/R19/R28 → C-07; R18/R25/R26 → C-08; R03/R12/R25/R26 → C-09. Each implementation must link actual evidence and scope limits back to affected requirements; a matrix reference alone is not a pass.

D08 remains open: the long-term division of human and automated control. Public benefit does not imply that the present prototype is validated for all people with diabetes.
