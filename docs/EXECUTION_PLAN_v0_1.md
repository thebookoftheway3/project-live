> Historical starter material. The Context-Aware Insulin System blueprint governs; use this document selectively. See the root PROJECT_BLUEPRINT.md and docs/PROJECT_DIRECTION.md. Setup commands here are not current completion evidence.

# PROJECT LIVE — Execution Plan v0.1
Date: 2026-10-24
Status: Initial research and design; no live insulin-control implementation authorized.

## Mission
Build an extensible open diabetes research system that preserves each person’s learned CGM-led capability, provides independently engineered low-glucose protection, and adds opt-in contextual support (meals, sleep, activity, home sensing). Optimize for life and attention returned, subject to demonstrated safety.

## Design commitments
- Preserve the original user observations separately from our interpretations.
- R00: Preserve the learned human–technology feedback relationship, not necessarily any specific device or algorithm.
- R01: Preserve or improve predictive low-glucose protection, manual dosing authority and trustworthy CGM visibility. No automatic insulin increases in the baseline protective mode.
- R02: Modular contextual support, beginning with meal detection and confirmed-bolus awareness.
- Never require cloud or home sensing availability for life-critical local protection.
- No probabilistic life-context inference may directly authorize insulin delivery.
- Safety properties must be specified, independently verified, and evaluated for common-cause failures.
- Do not alter existing therapy for initial research; simulation and retrospective replay first.

## Source inventory — verified 2026-10-24
1. BCDiabetes handouts index: https://www.bcdiabetes.ca/handouts/ . Relevant items: Looping with Omnipod 5 pods (2026-08-29); Looping at BCDiabetes (2026-08-21); Omnipod 5 vs Loop (2026-06-26); Loop Affiliate Program (2026-02-02); Additional Loop Resources; Looping in hospital; Looping Safety/Emergency Kit; Loop Custom presets; FINESSE study of undeclared meals; OLIVER Omnipod 5 vs Loop RCT; AID options September 2026.
2. BCDiabetes implementation introduction: https://loop.bcdiabetes.ca/welcome/introduction (note page contains older statements; verify against dated handouts).
3. BCDiabetes Omnipod 5 vs Loop: https://www.bcdiabetes.ca/wp-content/uploads/bcdpdfs/Omnipod-5-vs-Loop.pdf (dated 2026-06-10; pre-dates Omnipod 5 integration release).
4. Loop source: https://github.com/LoopKit/Loop
5. Loop workspace/releases: https://github.com/LoopKit/LoopWorkspace/releases
6. LoopKit source: https://github.com/LoopKit/LoopKit
7. LoopDocs: https://loopkit.github.io/loopdocs/
8. Loop CGM compatibility: https://loopkit.github.io/loopdocs/build/cgm/
9. Loop browser build: https://loopkit.github.io/loopdocs/browser/bb-overview/
10. GrapheneOS: https://grapheneos.org/
11. Android foreground microphone/camera restrictions: https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start

Verified release fact: Loop v3.14.7 (2026-09-15) introduced Omnipod 5 pod support; v3.14.9 released 2026-10-05. Pin exact tags/commits before analysis. Open-source Loop is an iOS app; AndroidAPS is a separate Android project. A GrapheneOS device is a candidate sensing node, not a drop-in host for iOS Loop.

## Proposed execution domains
A. **Local therapy controller (future, isolated)**: CGM freshness, insulin state, prediction, proposed basal action, independent safety supervisor, pump adapter. Must not depend on internet, cameras or home server.
B. **Context and support backend**: timestamped observations, probabilistic inference, sleep/meal/activity models, bolus awareness, user prompts. Failure must not affect A.
C. **Home sensing nodes**: optional cameras, microphones, room occupancy/motion, wearables. Prefer local inference, explicit household consent, retention limits and sensor-health monitoring.
D. **Assurance environment**: immutable/versioned event logs, deterministic replay, scenario generation, fault injection, safety cases and release provenance. No connection to live pump in early phases.

## Work packages, sequence and acceptance criteria
### WP0 — Requirements and baseline (days 1–5)
- Create requirements ledger: R00/R01, user-defined support functions, operational constraints and measurable outcomes.
- Map Tandem Basal-IQ + Dexcom G6 observable behaviours and interaction requirements; collect version details and permitted retrospective data exports.
- Define primary outcomes: time below range, severe events, response latency, missed events, alert burden, sleep disruption, time spent interacting, ability to recover from failure.
- **Exit:** requirements traceable to user observations, no presumed clinical equivalence.

### WP1 — Evidence and code inventory (days 1–7)
- Archive BCDiabetes handouts with publication dates, URLs, hashes, and claim/evidence status.
- Pin Loop/LoopKit/OmnipodKit versions; identify licenses, dependencies, interfaces, test suites, build and signing requirements.
- Map data flow: CGM → prediction → recommendation → safety gates → command → acknowledgement → reconciliation.
- Examine local/cloud dependencies and pod behaviour after disconnect.
- **Exit:** version-specific architecture map, known unknowns and reproducible simulator build.

### WP2 — Simulated safety core (weeks 2–4)
- Define strongly typed, timestamped events for glucose, insulin, CGM health, pod state, command intent and command outcome.
- Implement deterministic event replay and pump simulator; initially no actual pump communication.
- Formalize invariants for suspend-only mode, command idempotency, stale readings, uncertainty, restart and manual override.
- Add independent checking and fault injection; explicitly model common-cause failures.
- **Exit:** repeatable tests demonstrate constraints in the simulator; unresolved safety questions documented.

### WP3 — Context backend and first support function (weeks 3–6)
- Prototype Bayesian/temporal meal-state inference from audio features, phone placement/motion, contextual cues, CGM and confirmed insulin events.
- Distinguish observations, hypotheses and confirmed events. Avoid assuming conditional independence of correlated signals.
- Output advisory prompts only; no automatic bolus or dose changes.
- Measure precision, recall, calibration, detection latency, missed meals, interruption burden and utility over time.
- **Exit:** local prototype with offline replay and opt-in real-world passive data collection, no therapy control.

### WP4 — Hardware feasibility (weeks 2–5)
- Compare supported Pixel/GrapheneOS, standard Android and dedicated Linux sensor nodes by sensor access, developer control, battery, audio/camera uptime, local inference, reliability and security updates.
- Keep iPhone as possible Loop controller and use separate sensing node(s) if necessary.
- Evaluate cameras in home for occupancy, food preparation/eating and sleep context; test on-device inference, false positives and household consent.
- **Exit:** bench-test evidence and a short bill of materials; no purchase before key compatibility checks.

### WP5 — Clinical and regulatory pathway (parallel, weeks 1–8)
- Identify Swedish/EU medical-device requirements, professional review, software lifecycle and clinical evidence needed for any eventual live insulin-delivery use.
- Define independent review and safety case, with separate gates for prototype, bench integration and any human use.
- Preserve current approved therapy while researching alternatives; establish fallback and continuity planning.
- **Exit:** written go/no-go criteria; no assumption that simulation demonstrates clinical safety.

### WP6 — Comparative evaluation (weeks 5–10)
- Replay historical Basal-IQ/CGM/pump records when legitimately available; annotate uncertainty and the fact that observed trajectories were altered by historical insulin decisions.
- Compare candidate prediction timing and fault handling; run physiological simulations with documented assumptions.
- Test contextual support utility and alert burden independently of insulin control.
- **Exit:** evidence report identifying improvements, failures, confounders and open questions; not a claim of superiority.

## First ten engineering tickets
1. Create repository structure: docs/, research/, requirements/, schemas/, simulator/, inference/, tests/, assurance/.
2. Pin upstream Loop release and dependency revisions; preserve licenses and provenance.
3. Build upstream Loop in simulator and record environment/version.
4. Map OmnipodKit command/acknowledgement/reconciliation states.
5. Define event schema and monotonic-time handling.
6. Implement read-only replay ingestion from sample/synthetic glucose and insulin records.
7. Write safety invariant tests for suspend-only *simulated* actions.
8. Implement a mock pod with lost/duplicated/delayed acknowledgements.
9. Prototype local audio-feature meal-event classifier and Bayesian state estimator using non-medical test data.
10. Benchmark Android microphone background behavior and a home Linux sensor node.

## Decision register (open)
D01: iPhone Loop controller + separate Android/Linux sensing node vs alternative architecture.
D02: Separate safety supervisor process vs independent hardware: evaluate actual achievable isolation and pump command authority.
D03: On-premise home backend vs device-local backend; cloud for noncritical backups/analysis only.
D04: Sensor selection: Dexcom G7 primary candidate; alternatives for research.
D05: Camera placements and features, household consent, local storage, retention.
D06: Existing user apps and data export formats.
D07: Scope of user-controlled automation modes; baseline remains manual + predictive low protection.

## First-week schedule
Day 1: Establish source/evidence ledger and repo skeleton; record existing apps and hardware.
Day 2: Download/archive priority BCDiabetes handouts and verify revision dates; freeze Loop release.
Day 3: Build unmodified Loop simulator; list dependencies and test commands.
Day 4: Map insulin-delivery state machine and CGM freshness paths.
Day 5: Draft requirements and first STPA control structure, including human interactions.
Day 6: Implement synthetic event schema and replay test harness.
Day 7: Review evidence, decide next sprint, select a sensing-device bench test.

## Immediate inputs requested from project owner
Existing development OS/toolchain; current phone/watch/CGM/pump versions; names/interfaces of existing tracking apps; any existing home camera/microphone hardware; available anonymized or synthetic datasets; preference for local-only or hybrid infrastructure.

## Non-negotiable development boundary
No modified software is connected to an insulin-delivering pump as part of this initial plan. An experimental controller needs independent engineering review, verification, clinical validation and an appropriate regulatory/clinical pathway before human use. No probabilistic meal detection may automatically administer insulin in the initial system.
