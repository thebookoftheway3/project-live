# Surfer OS research FMEA

Preliminary design analysis, 2026-11-16. The traffic-signal conflict-monitor pattern
inspires separation of probabilistic proposals and deterministic constraints. No
NEMA TS2 compliance, medical safety certification or physiological equivalence is
claimed. Scores and residual acceptability are deliberately unassigned until
qualified reviewers and intended-use evidence exist.

Scope: [ADR 0004](decisions/0004-work-package-research-monorepo.md), R01/R03/R07/R12/
R14/R26/R27; existing assurance claims C-01/C-04/C-07/C-08/C-09. The primary implemented
boundary remains absence of real actuation capability. “Severe if connected” below
describes a hypothetical future system, not an authorized clinical deployment.

| Failure / cause | Effect | Implemented research safeguard | Verification and remaining gap |
| --- | --- | --- | --- |
| Proposal exceeds scheduled rate; AI or input error | Excess delivery if connected; potentially severe | Pure bench clamp; no pump transport | Enumerated C++ cases; schedule authenticity and hardware bypass resistance unverified |
| Endless renewal, timer reset or process failure | Prolonged suppression if connected | Original green start retained; 30-minute bench expiry | Repeated-renewal and exact-boundary tests; real independent watchdog/reset persistence absent |
| Noisy pause/resume toggling | Repeated unintended interruption | Explicit 15-minute bench lockout | Boundary tests; clinical appropriateness and persistent hardware state unverified |
| Missing/duplicate/stale delivery bins | False belief about delivery budget | 180 contiguous integer bins; UNKNOWN on incomplete history | Gap/stale/order/55% boundary tests; no actual pump delivery confirmation |
| A 55% threshold is physiologically inadequate | Harm despite a “passing” budget | No clinical adequacy claim and no real control | Qualified evaluation required; no test establishes DKA prevention |
| NaN, negative input, future state or regressed clock | Constraint bypass or fabricated output | Invalid results carry no simulated basal | Negative tests; independent clock and configuration integrity unverified |
| Wi-Fi loss and LTE-M not registered / MQTT not acknowledged | Stale or lost context | Pure bearer selector returns OFFLINE unless acknowledged | Physical modem, SIM, TLS, queue expiry/deduplication and <3 s target untested |
| False compression or warmup classification | True low wrongly dismissed if used for alarms | Quality hypothesis only; no alarm or therapy output | Synthetic boundary tests; real detector calibration and alarm policy absent |
| Repeated questions, silence treated as No, restart resets budget | Attention loss and misleading evidence | One pending prompt, 180 s expiry, cooldown, rolling budget; unknown replies retained | Session tests; durable state, delivery acknowledgement and field usability absent |
| User preemption confused with treatment authority | Suppressed protection or duplicate intervention | Synthetic attention-only interval; no dosing route | API/auth/idempotency tests; human control interface and clinical review absent |
| Bystander misidentified as SELF or media leaves node | Wrong inference and privacy breach | Explicit unknown subject, minimal export schema, no media capture/network adapter | Negative schema tests; real multi-person/egress/consent controls unverified |
| Relative depth treated as metric or wrong food density | Incorrect volume or metabolic interpretation | Reject uncalibrated metric inputs; no absorption model | Synthetic geometry tests; held-out calibration and food ground truth absent |
| Late evidence overwrites history or inflates certainty | Retrospective fit represented as prediction | Baseline chronology/lineage unchanged; semantic event IDs and availability gate | Existing tests and mutation controls; full multimodal dependence model incomplete |
| Unauthenticated request or duplicated callback | Session override or prompt replay | Bearer auth, strict bounded schemas, request identity/conflict checks | In-process API tests; no public VPS endpoint or production threat assessment |
| Deceptive voice identity or automatic treatment advice | Confusion, loss of trust or harmful action | No outgoing voice call or dosing recommendation | Any future service requires opt-in recognizable identity, cancellation and specialist review |

Do not convert this table into an assertion that the system is safe. For each
integration, identify an accountable owner, test the actual composed failure path,
record counterexamples and decide residual risk independently. Unit tests cannot
prove that physical limits are unbypassable, that pod firmware returns to a safe
schedule, or that a physiological minimum applies to a person.

See [verification plan](GRANT_VERIFICATION_PLAN.md) for proposed experiments and
[executed results](assurance/WP_REFACTOR_VALIDATION.md) for present evidence.
