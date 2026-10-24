# Context-Aware Insulin System — Research & Design Blueprint

**Public engineering specification | 24 October 2026 | Integration revision 3: virtual sensors, Bayesian inference and active historical investigation**

Adapted from the supplied Revision 2 specification for public collaboration. Personal history and treatment details are omitted; the original is preserved locally and identified by hash in `docs/SOURCE_MANIFEST.json`. Technical requirements are retained. Subsequent explicit project direction adds a public, open-source mission and active information gathering as a confirmed requirement. This integration incorporates the General-Purpose Virtual Sensor Architecture and Progressive Bayesian Inference addendum while retaining the Revision 2 Bayesian foundation. The architecture/specification integrated through PR #2 includes Active Historical Investigation: investigating why predictions were wrong is a foundational capability. Neither extension authorizes live sensing or full implementation.

**Status:** Open-source research for the benefit of people with diabetes. The first deliverable is a strictly non-actuating, read-only shadow system; it is not a validated treatment system. The insulin-focused initial scope does not establish suitability across every diabetes type, treatment, age group or device. Each person’s established treatment system operates independently.

## 1. The north star

Build a deeply context-aware, observable, adaptive human–machine system that returns as much of each person’s life as possible while maintaining safety and resilience.

People bring learned expertise in interpreting glucose movement, context and insulin response. Preserve that competence while making more management work disappear. Evaluate accessibility and attention burden across people and settings, rather than treating one individual as representative of everyone.

**North-star question:** *How much human life does the system give back?*

**Engineering question:** *When the system's understanding is wrong, can that error be detected before it causes an unsafe action?*

**Provocative stretch goal:** At home, freely take an ordinary sugared cola from the fridge and eventually see little or no visible disturbance in the glucose trace; likewise eat ordinary food without extensive conscious diabetes management. This is a **research ambition, not a promise or established physiological capability**. Subcutaneous insulin has onset and absorption delays; no amount of scene recognition guarantees prevention of post-meal glucose excursions.

**Design objective:** Lower effective insulin-action latency is a distinct objective from more uniform absorption. Do not substitute one for the other; formulation, compatibility and clinical suitability remain separate research dependencies.

## 2. The originating insight

Changing a controller can change a learned human–device feedback relationship, not just replace a component. The engineering question is which sensing, feedback and control relationships should be preserved or improved.

Apply ideas from distributed real-time systems: sensing, estimation, changing operating regimes, latency, fallback and fault observability. The project is open for reuse and contribution by the wider diabetes community. Its purpose is useful shared capability.


## 3. Core design principles

1. **Automation should give back attention, not demand continuous supervision.** Alarm frequency, cognitive switching and family burden are real output metrics alongside glucose outcomes.
2. **Model the actual human–machine relationship.** The human is already a skilled controller with contextual knowledge; do not classify their observations as mere “preferences” or “resistance to change.”
3. **The past matters.** Glucose response and any hypothetical intervention depend heavily on preceding meals, insulin delivery, physical activity, sleep, stress and other context—not merely the current CGM reading or the next carbohydrate event. Maintain a **Bayesian belief state with memory**, not a single asserted state or a point estimate disguised as certainty.
4. **Distinguish sensing, interpretation and action.** A camera observation is not a confirmed meal. A pump command is not necessarily effective insulin. CGM agreement is not proof of correctness.
5. **Distinguish uncertainty sources.** Measurement uncertainty, context uncertainty, model uncertainty and insulin-delivery/absorption uncertainty are different failure modes.
6. **Change control authority with *validated* observability, not location alone.** Home may provide richer sensing; outdoors less. “At home” never proves a state is safe or justifies unconstrained dosing.
7. **Degrade gracefully.** Missing, stale, contradictory or out-of-distribution signals should reduce claims of certainty. A safer, independently established treatment path remains available.
8. **Learn from disagreement.** Record the model's interpretation, the user's interpretation, the actual action and the observed aftermath as separate objects. Never overwrite original observations with inferred explanations.
9. **Keep the experimental system unable to actuate insulin at first.** Independent physical and software boundaries matter more than an on-screen label saying “simulation.”
10. **Test whether additional sensors add value.** More sensors are not inherently more intelligence; measure incremental predictive information, latency, availability and false-confidence risk.

11. **The sensor is the question, not the hardware.** Any authorized relevant stream can support a testable, software-defined virtual sensor. Separate generic sensing infrastructure from the diabetes-specific physiological model.
12. **Ask the next useful question.** Progress from cheap detection to selected advanced inference only when expected benefit justifies permissions, resource and attention costs. UNKNOWN and stopping are valid outcomes.
13. **Compose interpretations without inventing evidence.** Preserve raw observations, derivation lineage, correlation and competing hypotheses through every virtual-sensor layer. New sensors extend the existing Bayesian belief state rather than establishing a competing authority.

14. **Investigate the past without rewriting knowledge.** The next useful question may concern the present, future or past. A sensor invented today can reinterpret compatible retained data recorded yesterday. Preserve what the system knew then separately from what it understands now.

## 4. System boundary: two parallel worlds

### A. Active treatment system

The established controller/pump/CGM arrangement remains solely responsible for actual insulin delivery. Examples of *distinct alternatives* are a Tandem pump using Tandem Control-IQ, an Omnipod 5 using its manufacturer-controlled automated mode, or a separately configured Loop-driven Omnipod arrangement. **These are not interchangeable algorithms:** Control-IQ belongs to Tandem; the Omnipod 5 manufacturer's SmartAdjust algorithm is different; the open-source Loop algorithm controlling an Omnipod pod is different again. Do not imply Control-IQ runs on Omnipod 5.

### B. Experimental shadow system — the first build

Consumes authorised read-only observations and recorded treatment history; predicts glucose and contextual state; records *hypothetical* interventions; estimates confidence; compares predictions to observed results. **It neither sends pump commands nor silently modifies treatment parameters.**

Shadow output is labelled `SIMULATED / NOT DELIVERED`, separated from confirmed insulin delivery. Read-only permissions, no pump command credentials, and a simulated pump backend are the preferred engineering boundaries.

**Important:** Loop's own **Open Loop** mode disables its automated insulin adjustments, but the application may still expose manual pump-control functions. For a *strictly non-actuating* research build, use the documented **pump simulator** or a separate shadow application with **no real pump control path**. Do not assume “Open Loop” alone means no commands can reach a real pump.

### Conceptual data flow

```text
Authorized streams: measurements / time series / images / audio / events / logs
                                  |
Generic adapters -> cheap detection -> virtual-sensor evidence
                                             |
                                Bayesian joint belief state
                                  /                     \
                    shadow predictions               evidence gaps
                                                           |
                                                acquisition planner
                                               /                  \
                             fresh / retained / historical query    stop, retain unknown
                                             |
                           new traceable evidence or interpretation

One planner queries a permission/retention-aware evidence index.
One estimator preserves online snapshots and separate retrospective views.

HARD BOUNDARY: NO EXPERIMENTAL OUTPUT -> LIVE PUMP COMMANDS
Independent treatment continues outside this research pipeline.
```

See the [architecture diagram and boundaries](docs/architecture/SYSTEM.md) and [proposed contracts](docs/architecture/VIRTUAL_SENSOR_CONTRACTS.md). These are logical components, initially suitable for one process; they do not require a fleet of services or a plugin ecosystem.

## 5. Proposed sensing and component inventory

### 5.0 General-purpose software-defined virtual sensors

A physical sensor measures a signal; a virtual sensor answers a versioned question about evidence. Microphone audio may support questions about a can opening or acoustic reliability; video may support presence or container identification; power, door contacts and movement can support the same event through different evidence. Scalar measurements, time series, images, audio, logs, software events, CGM, pump history and other authorized streams share an ingestion/provenance framework.

Virtual sensors may compose other virtual sensors while retaining their raw evidence leaves and alternative explanations. A higher-level beverage event remains an inference. Never count its supporting leaves again as independent evidence. Provider scores require explicit semantics and calibration status; missing data are not negative evidence.

Each sensor declares identity/version, question, input requirements, permissions, temporal window/freshness, triggers, cheap/advanced alternatives, output schema, uncertainty semantics, provenance/dependencies, failure/OOD behavior, costs, expected value, escalation and stopping rules. Historical execution additionally requires compatible retained representations, current purpose authorization and versioned backfill results with actual execution/availability times. Begin with [small contracts and a static registry](docs/architecture/VIRTUAL_SENSOR_CONTRACTS.md), not a complex plugin framework.

Items marked **core** below describe the intended diabetes research profile, not mandatory hardware built into the generic framework. Missing devices must remain supported explicitly; **optional** means investigate usefulness and access before purchasing or implementing. Reuse in traffic, buildings, industry or accessibility is architectural potential, not additional product commitments.

### 5.1 Glucose sensing — **core: two CGMs**

- Two simultaneously worn CGM sensors, ideally with sufficiently distinct failure modes and independent access to readings; exact brands/models are undecided.
- Preserve each raw trace independently: measured glucose, sample timestamp, reception timestamp, trend, age, signal gaps, connection state, sensor age, calibration/health flags when available.
- Compare agreement, disagreement, drift, delay, dropout and rate-of-change consistency over time.
- Avoid automatically averaging two readings or assuming two agreeing sensors are correct. Shared physiology and shared artefacts can create correlated errors. When they disagree, neither one is automatically the truth; an independent blood-glucose check may be necessary for clinical decisions.
- Loop's documented standard configuration chooses a CGM source. **Two-source acquisition, synchronisation and quality assessment are custom research features**, not a verified out-of-box dual-CGM safety function.

### 5.2 Insulin delivery and treatment history — **core**

- Actual confirmed pump delivery events, not merely requested or recommended delivery.
- Current and past basal delivery, corrections, user-initiated boluses, interruptions, suspensions, controller mode, connectivity and warnings where reliably accessible.
- Derived estimates of insulin remaining active may be informative, but must retain model assumptions and uncertainty.
- Pod/infusion-site start time, location, age, changes, alarms, suspected failures and user observations.
- Never infer that commanded insulin has reached or been absorbed by tissue merely because a command was logged.

### 5.3 Wearable physiology — **core, subject to device/API support**

- Heart rate and temporal trends.
- Heart-rate variability where available, including its measurement cadence and quality.
- Accelerometer/gyroscope activity and movement intensity.
- Sleep and waking patterns, resting versus active state.
- Respiratory rate, skin/wrist temperature or other available wearable signals.
- ECG measurements **when explicitly recorded and accessible**; do not assume a consumer watch streams continuous ECG. For example, Apple Watch's standard ECG app captures a user-initiated ~30-second sample; ECG data access via HealthKit does not make it an always-on live waveform source.
- Treat all wearable signals as possible context predictors, not validated direct measurements of glucose, insulin sensitivity or meal content.

### 5.4 Home perception — **core concept, phased implementation**

- Local cameras observing relevant home activity: kitchen/fridge, drinking/eating gestures, movement and occupancy as permitted by consent and privacy design.
- Beverage identification: item, brand/type, regular versus sugar-free, package size, opened/handled status, consumption evidence and uncertainty.
- **Quantity cannot be assumed exact from video.** Investigate independent cues such as a smart scale, before/after container weight, repeat observations or explicit confirmation. A visible cola can be opened, poured out, shared or not consumed.
- Smart-home cues: fridge/cupboard state, room presence, lights, door sensors, smart scales and other context signals if they improve inference.
- Option to run local computer vision without long-term video storage; maintain derived events with provenance and confidence.
- Respect the privacy and consent of other people in the home; no unneeded persistent recordings.

### 5.5 Mobile and environmental context — **candidate inputs**

- Phone/watch location and whether the user is home, commuting or elsewhere.
- Motion, walking, exercise and travel state.
- Ambient temperature, weather or other environmental variables if they demonstrate predictive value.
- Manual annotations for illness, medication changes, alcohol, atypical exercise, sensor faults and context no sensor can infer reliably.
- Optional future inputs such as additional wearable or room sensors belong in an **evidence-driven backlog**, not the first mandatory hardware shopping list.

## 6. The Bayesian core: a belief state, not a guessed state

**Central architecture (previously under-specified):** Bayesian sequential inference is the explicit foundation of the *non-actuating* digital twin. Rather than producing one supposedly known physiological state, the system maintains a **probability distribution over plausible hidden states and explanations**, updates it as new evidence arrives, and preserves unresolved ambiguity. This formalises a human learning process: incorporate history, compare predictions with what happens, revise beliefs, and become less confident when observations cease to fit.

A core research hypothesis is that **prior behaviour often dominates what an upcoming carbohydrate event will require**. This must be tested per person and context, not assumed to be an established numerical ranking for everyone. A Bayesian time-series model makes the historical dependence testable without pretending every relevant variable is directly observed.

### 6.1 Three kinds of objects: observations, hidden state, and discrete hypotheses

**Observed data `y_t`:** CGM A, CGM B, delivered-insulin records, confirmed meals, inferred camera events, watch/phone samples, activity, sleep-related signals, timestamps, sensor-quality data, and explicit human annotations. Carry source, latency and missingness. A camera's `cola_candidate` event is an observation about an image, **not proof of ingestion**.

**Latent state `x_t` (examples to investigate, not clinically validated quantities):** glucose trajectory underlying noisy and delayed measurements; residual insulin-effect state; delayed meal appearance; activity/recovery effects; uncertain time-varying response to insulin; sensor-specific drift or bias; and context variables that cannot be observed directly. Some are identifiable only weakly or not at all from available sensors.

**Discrete modes `m_t`:** competing interpretations such as `beverage_not_consumed / regular_beverage_consumed / diet_beverage_consumed / unknown`, `site_responding_as_expected / altered_response / suspected_delivery_problem`, or `CGM_A_suspect / CGM_B_suspect / both_uncertain`. These are **hypotheses**, not medical diagnoses, and they are allowed to coexist with nonzero probability.

The system retains a *joint belief*, including dependencies between variables and modes. It must not collapse disagreement into an early winner merely to simplify UI or control logic.

### 6.2 Bayesian filtering — prediction, evidence, correction

Let `u_t` represent **verified actions that actually occurred**, such as confirmed insulin delivered, rather than proposed shadow actions. At each time step:

1. **Predict:** propagate yesterday's distribution through a time-aware process model and action history. Include physiological delay, context, and uncertainty in the process model.
2. **Observe:** add new timestamped evidence through source-specific observation models. Include delays, dropouts and quality flags.
3. **Update:** reweight the plausible states and modes according to how well they explain the evidence.
4. **Predict forward:** generate **posterior predictive distributions**, not just one predicted glucose line. Preserve and display the width and multimodality of those distributions.
5. **Check fit:** measure whether actual observations repeatedly fall where the model said they were plausible. If not, flag model mismatch rather than silently retuning until every event seems explained.

Compact notation:

```text
predict:  p(x_t, m_t | y_1:t-1, u_1:t-1)
update:   p(x_t, m_t | y_1:t,   u_1:t-1)
          ∝ p(y_t | x_t, m_t, quality_t)
            · p(x_t, m_t | y_1:t-1, u_1:t-1)
```

This is a *conceptual factorisation*: actual asynchronous events, sensor lag, late-arriving data, missing information and correlated errors require a more careful implementation. Crucially, **a shadow recommendation is never treated as `u_t` unless an independently recorded real action confirms it**.

### 6.3 Prior knowledge and individual calibration

- Start with explicitly documented, conservative **research priors** and stated model assumptions; do not silently treat population averages as this individual's physiology.
- Learn **person-specific posterior distributions** from chronological history, rather than fitting a fixed insulin sensitivity number and assuming it remains constant.
- Distinguish relatively slow parameters from rapidly changing states and from discrete events (for example, a new infusion site or suspected sensor failure).
- When a pod or infusion site changes, investigate a **change-point / new-mode hypothesis**, instead of blindly carrying the previous site's response estimate forward.
- Avoid posterior overconfidence: limited data, strong priors, correlation between streams and unexplained disturbances must remain visible.
- Updating beliefs in the shadow twin is allowed. **Online updates that would automatically change real dosing parameters are outside this project's validated scope.**

### 6.4 Probabilistic sensor fusion without invented independence

Two CGMs are valuable partly because *disagreement itself is evidence*. But both observe related physiology with lag and may share error sources. Naively treating two CGMs as independent and multiplying their likelihoods can produce unjustified certainty even when they agree. Model temporal correlation, shared lag and common-mode error where possible; otherwise cap effective evidence rather than double-counting it. A fingerstick/reference reading may help adjudicate a clinically significant conflict, under the user's established care procedures.

Similarly, smartwatch pulse, HRV, temperature, intermittent ECG, motion and camera signals are **indirect clues** about context. They must not be promoted into direct measurements of insulin sensitivity or glucose. An absent observation is not a negative observation; irregular sampling and source availability must enter the likelihood model.

### 6.5 Behaviour recognition as competing explanations

A fridge event raises a *prior* probability that a drink-related event may follow; it does not establish consumption. Subsequent evidence may update probabilities for regular cola, diet cola, partial consumption, someone else drinking, or no ingestion. Inferred consumed volume should be represented by a **distribution including the possibility of zero**, not an invented exact millilitre count. Cross-check camera, container weight, explicit user input and subsequent observations without using the later glucose curve to retroactively claim the camera independently observed drinking.

The system should be able to say: `Several explanations fit; more evidence is needed.` That is a useful output, not a failure to produce a label.

### 6.6 Model family and practical staged implementation

This is a **Bayesian design requirement, not a premature commitment to one algorithm**:

- **Baseline:** simple historical CGM + confirmed-insulin predictor with honest predictive intervals and explicit errors. Establish that a complicated model actually improves on something transparent.
- **Prototype A:** structured state-space model with uncertainty (e.g. Kalman-family approximations if the submodel assumptions permit them).
- **Prototype B:** switching-mode / hidden-Markov representation for discrete hypotheses such as sensor reliability or site-response changes.
- **Prototype C:** particle filtering or other sequential Monte Carlo methods if nonlinear dynamics, delayed observations and competing explanations require richer posteriors. Computational cost and particle collapse must be measured.
- **Later, if justified:** hierarchical Bayesian learning for person-specific dynamics. Do not add complexity without measured predictive improvement and better-calibrated uncertainty.

Start by reproducing synthetic cases where the latent state is known, then challenge the model on historical and *prospective* read-only data. Model selection should be evidence-driven, including comparisons against non-Bayesian baselines.

### 6.7 Required belief-state API (research-only)

A model response should make its uncertainty auditable:

```text
BeliefSnapshot:
  snapshot_id / inference_kind / target_window
  inferred_at / evidence_cutoff / model_version
  exact_evidence_manifest + actual_availability + sensor_versions
  original_snapshot_ids + parent_snapshot_id + revision_reason
  observed_sources + freshness + quality + provenance
  posterior_state_summary + credible_intervals
  discrete_hypotheses_with_probabilities
  glucose_posterior_predictive_distribution_by_horizon
  competing_explanations + supporting/contradictory evidence
  model_mismatch_flags + OOD_flags + calibration_status
  evidence_needed_to_reduce_uncertainty
  shadow_only: true
  may_actuate_insulin: false
```

Do not conflate a mathematically narrow credible interval with proven safety. A confidently wrong model remains possible, especially after domain shift or correlated sensor error. Probabilities must be *empirically calibrated* before being interpreted as decision-grade confidence.

### 6.8 What to evaluate and what not to infer

Evaluate proper probabilistic scores (e.g. log score or CRPS where appropriate), Brier/log loss for discrete events, observed coverage of predicted intervals, calibration by horizon and environment, detection delay, and whether adding each sensor actually improves *prospective* predictions. Stress-test rare modes, joint sensor failures, missingness, infusion-site changes and repeated false confidence.

Keep **prediction** separate from **counterfactual intervention**. If a human took one dose, the later glucose curve cannot tell us what would have happened under a different shadow dose. Bayesian inference does not remove this causal identification problem. Neither high posterior confidence nor agreement with the user's intuition authorises live insulin delivery.

**Key design statement:** *Represent what the system believes, why it believes it, what competing explanations remain, and how wrong it might be — then let reality update those beliefs. At this stage, this belief state informs only a shadow model.*


### 6.9 Active information gathering

The system is responsible for recognising insufficient evidence and actively seeking useful additional sensor observations. Cheap event detection produces initial evidence; update the Bayesian belief, identify a relevant gap, then select the next source, question or model tier only when worthwhile. The same planner compares fresh observations, deeper retained-data analysis, targeted historical retrieval, searches for similar episodes, retrospective execution of compatible virtual sensors and no action. A current mismatch may make a low-interest event from hours earlier newly relevant. Historical queries and follow-up inference spend the same privacy, permission, latency, compute and attention budgets as new acquisition.

Evaluate information value against latency, compute/API costs, energy, bandwidth, freshness, source reliability, privacy and human attention. Hard authorization and resource limits precede ranking. Record the reason, requested evidence, predicted benefit, actual costs/outcome, belief revision and independently evaluated improvement. Expected information gain, observed entropy reduction and predictive correctness are different measurements.

Stop when useful evidence is unavailable, not permitted, too costly or not expected to help. Permission revocation and provider failures must preserve unresolved uncertainty. Provider-neutral inference supports local algorithms, local ML, mocks and optional external services; the existing Bayesian estimator remains the single integrator. The [Decisions feasibility record](docs/research/DECISIONS_API.md) verifies capabilities before any adapter-specific schema or implementation. No cloud provider is foundational to this architecture.

Human clarification is a possible architectural mechanism whose timing and interaction design remain open. An unanswered question is unknown, never a negative observation. Insufficient evidence must remain explicit when no useful observation can be obtained; acquisition does not grant treatment authority.

### 6.10 Active Historical Investigation: filtering, smoothing and knowledge time

**The past has not changed. Our understanding of the past has.** A prediction mismatch can trigger a bounded investigation of earlier camera, audio, wearable, activity, CGM or insulin-history evidence, including events initially classified as uninteresting. This is a core use of the existing acquisition planner and Bayesian estimator, not an optional analytics subsystem.

Online filtering estimates the current state using evidence actually available and admitted at the time. Retrospective Bayesian smoothing estimates an earlier state using later available observations or interpretations. Retain both views as separate versioned snapshots. A later interpretation may also support a newly issued current estimate, but cannot replace an original forecast or change its evidence cutoff. The event-time shorthand in section 6.2 must be implemented with the availability-aware semantics in the [architecture](docs/architecture/SYSTEM.md#online-filtering-versus-retrospective-smoothing).

Distinguish event time, recording time, ingestion time, actual object availability, inference execution/publication, target interval, model/question/sensor versions and the original forecast's evidence cutoff. Record exactly which evidence was used; an available but unexamined frame is not an already-known interpretation. A new sensor result inherits its actual availability time, never its old input's timestamp.

A newly invented virtual sensor can backfill compatible retained data under current consent and purpose limits. Append interpretations and reproducible manifests, preserving earlier interpretations and original inputs while retention permits. New-model reanalysis is explicitly labelled; it is not evidence that the original model knew the same thing. The past/current views remain outputs of one belief architecture.

Begin with a simple index over synthetic events and episode references. Queries filter time windows, actual availability, representation compatibility, permission and retention before retrieving or ranking results. Similar episodes nominate evidence rather than prove causes. No query assumes indefinite household audio/video storage, revives expired media or restores revoked consent. Missing history is missing evidence. If authorized erasure prevents exact replay, report incompleteness rather than fabricate the former view.

Preserve lineage across original detections, later reinterpretations, episode matches and the mismatch that triggered the query. Do not count the same raw event or later glucose observation repeatedly. As-was evaluation excludes later interpretations, versions and similarity features; retrospective analysis declares its later cutoff and separate metrics. A retrospective explanation cannot establish causation or identify the outcome of an insulin intervention that never occurred.

## 7. Infusion site as a dynamic process, not an afterthought

**Research question:** Can site-to-site differences and changes with site age be detected without mistaking meals, sensor error or activity for delivery/absorption changes? The magnitude and cause of any variation must be established from evidence.

Engineering interpretation: a potentially time-varying, partially observable **delivery/absorption channel**. Questions for offline study:

- Can a characteristic change after a site replacement be detected from time-aligned events?
- Is there measurable drift with site age?
- Can unusual response be differentiated from sensor error, meals, activity or illness?
- Which patterns are detectable early, and what is the false-alarm rate?
- Which patterns need human or independent glucose confirmation?

**Do not treat an apparent lack of effect as permission to automatically increase insulin.** Delayed absorption and delivery failure can resemble lower sensitivity while carrying very different risks, including later insulin stacking. Suspected infection, irritation, occlusion or failure is a treatment/device concern to address through the user's established clinical procedures, not something software should merely optimise around.

**Separate objective:** Investigate lower effective insulin-action latency separately from site-response variation. Formulation, device compatibility and person-specific suitability remain dependencies for qualified clinical assessment. No anatomical site is assumed to provide faster action.

## 8. Context-dependent automation and the attention budget

The intended long-term architecture is a **supervisory system** deciding how much *experimental* control can be trusted in different contexts. This is a design hypothesis to validate, not an authorisation to actuate.

- **Home / rich observation:** More sensors may make some behaviours detectable earlier and more reliably. Long-term aspiration: more useful automation and fewer unnecessary interruptions.
- **Away / reduced observation:** More unknown context; more reliance on deliberate user input and situation-relevant notifications, if validated.
- **Sensor disagreement, missing data, unfamiliar context or suspected site malfunction:** Reduce confidence, make uncertainty legible and rely on the independently established treatment/safety path.

Never equate `home=true` with `safe=true`. A home camera does not know everything, and a model's self-reported confidence can be wrong. Modes and any future mode transitions require empirical validation and independent constraints.

**Attention is a finite resource.** If good automation handles ordinary home situations with fewer nonessential prompts, the user can devote more attention when away or when the situation genuinely requires judgment. Record attention costs as a first-class performance variable.

Safety-critical alarms and established protective functions must not be silently suppressed as part of an “alarm-free home” goal. Separate nuisance-alert reduction from medically necessary alerts.

## 9. Multimodal beverage experiment: defining what must be inferred

Use a familiar event as a demanding observational test. A camera is one possible source; audio, motion, a door contact, power readings and a scale may provide complementary evidence:

1. A known beverage is taken from the fridge.
2. The system identifies the likely beverage, including whether it contains sugar.
3. It observes evidence of actual consumption and estimates quantity, with uncertainty.
4. It combines the event with *preceding* physiology, activity, meals and confirmed insulin delivery.
5. It generates shadow predictions and hypothetical treatment suggestions without acting.
6. It compares predicted and subsequently observed glucose behaviour and records where the model was wrong.

Research questions: Can recognition occur early enough to matter? What is the rate of false drink detections, mistaken regular/diet classification, inaccurate quantity estimates and missed events? Does the enriched history materially outperform a CGM-plus-insulin baseline? What happens when the user drinks somewhere without cameras?

Do **not** infer “the camera knows exactly how much was drunk.” Do **not** assume a perfect flat glucose curve is physiologically possible with unannounced fast carbohydrates and subcutaneous insulin.

The [first synthetic vertical slice](docs/design/SYNTHETIC_VIRTUAL_SENSOR_SLICE.md) is narrower: door event → cheap audio-feature detector → virtual sensor → selectively requested mock image inference → Bayesian update → synthetic weight evidence → auditable replay. It includes diet, no/partial consumption, another person, missing camera, contradiction, correlated repetition, timeout, no-value acquisition and confident-error cases. The same LIVE-022 slice includes a required historical phase: low-interest 12:30 activity, a scripted 14:30 prediction mismatch, selective historical retrieval and mock reinterpretation, then a retrospective posterior with both online snapshots frozen. Leakage, unavailable-history, correlated-evidence and consent/retention-denial checks are mandatory. It calculates no insulin doses and makes no live requests.

## 10. Shadow mode, calibration and learning together

The design includes a **calibration period**: the system makes predictions and hypothetical suggestions; the user continues using their existing judgment; over time, the user becomes familiar with the model and the model is evaluated against experience. Eventually some suggestions might become inputs to a real controller **only after a separate safety/clinical validation decision**.

Store four objects separately:

1. **Observation:** What sensors recorded, including time and reliability.
2. **Model belief:** What the shadow system inferred *at that time* and how uncertain it was.
3. **Human decision and actual delivered treatment:** What the user chose and what the pump confirmed.
4. **Subsequent observed outcome:** What happened after the actual treatment, including interventions and data gaps.

Important methodological limits:

- Observing an outcome after the user's action does **not** prove the model's different hypothetical action would have been safe or successful. That counterfactual outcome is unobserved.
- Agreement with the user's decisions is useful for learning the user's policy, but does not independently validate safety or glucose outcome.
- If the user starts adopting model suggestions, training data become policy-dependent; track this explicitly and avoid treating agreement as independent confirmation.
- Use chronological holdouts, scenario replay and prospective pre-registered shadow predictions, not only retrospective fitting to past traces.
- Maintain original inputs, predictions, model version and timestamps so that performance cannot be improved retroactively by leaking future information.
- Record later smoothing and new-sensor reanalysis separately from original online snapshots. Later outcomes may score an original forecast, but must never enter its inputs; retrospectively improved explanations are not improved original predictions.

The key target is **detectable wrongness**, not infallibility. Evaluate whether error signals arrive soon enough for a human or independently validated safety mechanism to respond.

## 11. Non-actuating software modules for Codex

The following is a future physiological-shadow layout from Revision 2, not a required refactor of the current Python starter. The generic source/virtual-sensor/provider/planner contracts are defined in the architecture documents and may initially live in one package. Do not create empty services or duplicate the Bayesian state API merely to match this sketch.

A suggested future repository layout:

```text
README.md
PROJECT_BLUEPRINT.md                   # this document
SAFETY_BOUNDARY.md                     # exact non-actuation boundary
ASSUMPTIONS_AND_OPEN_QUESTIONS.md
DATA_DICTIONARY.md
src/
  adapters/
    cgm_a/
    cgm_b/
    pump_history_readonly/
    wearable/
    home_events/
    phone_context/
    human_annotations/
  events/                             # normalisation / provenance / timestamps
  quality/                            # freshness / agreement / missingness
  state/                              # Bayesian filtering / latent state / modes
    bayes/                            # priors, transition models, likelihoods
    inference/                        # sequential filtering + belief snapshots
    calibration/                      # posterior predictive calibration
    changepoints/                     # site/sensor regime shifts
  perception/                         # beverage / activity inference
  shadow/                             # no-live-pump interface
  evaluation/                         # prediction quality / error detection
  reporting/                          # readable human-model disagreements
schemas/
  observation.schema.json
  inferred_event.schema.json
  prediction.schema.json
  shadow_decision.schema.json
  belief_snapshot.schema.json
  model_hypothesis.schema.json
  delivered_treatment.schema.json
simulator/
  synthetic_cases/
  replay/
tests/
  ingestion/
  timeline/
  quality/
  fault_injection/
  replay/
```

**Hard architecture rule:** `src/shadow/` must not import a real pump-command client or possess credentials capable of commanding a live pump. The only output is to a simulator, log, report or UI clearly identified as hypothetical.

A minimal normalised event should capture:

```json
{
  "event_id": "uuid",
  "event_type": "beverage_observation",
  "observed_at": "2026-10-24T12:00:00+02:00",
  "received_at": "2026-10-24T12:00:01+02:00",
  "source_id": "kitchen_camera_01",
  "source_kind": "camera_inference",
  "value": {
    "beverage_candidate": "regular_cola",
    "estimated_container_volume_ml": 330,
    "consumed_volume_ml": null,
    "consumption_confirmed": false
  },
  "confidence": 0.82,
  "model_version": "perception-dev-001",
  "quality_flags": ["consumption_unverified"],
  "provenance": ["local_camera_event_123"],
  "is_treatment_instruction": false
}
```

Example values above are synthetic and **not** a claim that camera classification or measured consumption has been validated.

Cross-cutting engineering requirements: monotonic sequencing where appropriate, UTC plus local display time, late/out-of-order event handling, clock-skew detection, source IDs, event versioning, audit trails, explicit missing-data semantics, encrypted local storage, short retention, permission controls, and no unconsented external uploading of physiological data or identifiable household video.

## 12. Evaluation and success criteria

Do not evaluate only glucose averages or a visually smooth line. Compare a baseline using CGM and insulin history against progressively enriched models, with the same evaluation periods and no future-data leakage.

Measure:

- Glucose-prediction error **and probabilistic calibration** across horizons: posterior predictive coverage, proper scoring rules (e.g. CRPS/log score), false confidence, and temporal drift.
- Calibration and Brier/log-loss of discrete hypothesis probabilities (beverage events, suspected sensor problems and site-response modes), assessed prospectively.
- Comparison of Bayesian variants to transparent non-Bayesian baselines; ablation of each added data source.
- How much extra predictive value activity, wearable signals and home perception actually contribute.
- Detection and lead time for CGM faults, site-response anomalies and out-of-distribution situations.
- Disagreement rates between the two CGMs; false agreement and missing-data cases.
- Beverage identification, regular/diet differentiation, quantity uncertainty, and false or missed ingestion events.
- Shadow-model versus human-decision disagreement, investigated by context rather than merely counted.
- False-alert frequency, missed important events, cumulative interruption time and attention burden.
- Sleep disruption, practical effort, freedom to leave home, and (where relevant and consensually recorded) burden on family members.
- Connectivity, on-device availability, power consumption, local processing latency, storage and privacy impact.
- Progressive versus cheap-only and fixed-escalation policies: event precision/recall, calibration, false confidence, provider calls, cost, acquisition latency, resource use and downstream prediction quality. Separate measured costs from simulated or unavailable metrics. Preserve negative results.
- Robustness to sensor outages, changing routines, unseen settings and infusion-site changes.

A predicted smooth glucose curve is **not** a sufficient success criterion. Counterfactual safety, actual insulin effect and independent fault handling remain distinct evaluation problems.

## 13. Failure scenarios that must be simulated before any further ambition

Develop fault-injection tests with synthetic and de-identified data for:

- Two CGMs agreeing but both biased, or disagreeing without an identifiable winner.
- CGM compression lows, sensor lag, stale data, dropouts and clock desynchronisation.
- Cola versus sugar-free cola confusion; bottle opened but not drunk; drink shared; partial consumption.
- Exercise not captured by sensors; unusual activity after a meal.
- Insulin recorded as commanded but not verifiably delivered; delayed absorption; infusion-site failure.
- Unexpected recovery of insulin action after a period of apparently poor response.
- Human manual corrections absent from the log, creating wrong insulin-on-board assumptions.
- Model confidence staying falsely high under a new routine or new sensor condition.
- Correlated CGM errors that a naive independent Bayesian likelihood would count twice.
- Multi-modal posteriors collapsing onto the wrong explanation; late-arriving evidence that changes a previous belief.
- Abrupt change-point after an infusion-site change, and gradual drift with site age; tests of false identification between site and meal hypotheses.
- Probability calibration appearing good overall while becoming dangerously overconfident in rare contexts.
- Network disconnection, phone restart, wearable dropout, low battery, home-camera outage.
- Privacy failure or sensor observations involving another person rather than the user.
- A model that appears accurate on historical data but fails prospectively.
- Historical retrieval admitting late-available interpretations, later-registered sensors or later episode features into an earlier knowledge cutoff.
- Unavailable, incompatible, expired or consent-denied history; a later query must not invent evidence or bypass the original retention constraints.
- Duplicate historical derivations and selective investigations that falsely reinforce the same explanation.

These scenarios are for **non-actuating simulation and fault detection**, not instructions for modifying clinical dosing.

## 14. Implementation sequence

These are the longer-term physiological research phases. The immediate delivery order is the [synthetic LIVE-022 milestone](docs/BACKLOG.md), in small reviewed increments; live acquisition and the Loop simulator track are not prerequisites. Progression beyond synthetic work requires separate permission and assurance review under the [methodology](docs/METHODOLOGY.md).

**Phase 0 — Establish the boundary.** Document actual equipment, treatment controller, supported APIs, read-only acquisition, data rights, safety ownership and clinical compatibility. Set up a synthetic pump simulator. No code capable of live dosing.

**Phase 1 — Reliable event history.** Ingest one CGM stream and confirmed insulin history, with accurate timestamps, provenance and replay. Then add the second CGM without merging away either original.

**Phase 2 — Context instrumentation.** Begin with generic adapters, versioned virtual-sensor questions and the synthetic progressive-inference slice. Later add authorized watch/phone and home context through those contracts, guided by measured information value. Keep image/audio interpretation independent of treatment and validate observation quality.

**Phase 3 — Bayesian belief-state estimator.** First implement a baseline forecaster with predictive intervals; then a documented Bayesian filtering prototype with explicit priors, state transitions, source likelihoods, posterior updates, competing discrete modes and posterior predictive checks. Compare accuracy *and calibration* against baseline. Treat site-response changes and CGM fault modes as separate, testable hypotheses. Keep the entire estimator read-only.

**Phase 4 — Shadow twin.** Generate time-stamped glucose forecasts and hypothetical actions to a virtual pump; compare with real outcomes following actual delivered treatment. Record human–model disagreement without assuming either is infallible.

**Phase 5 — Robustness and burden evaluation.** Stress-test ambiguous beverages, missing context, sensor faults, infusion anomalies and new environments. Quantify improved prediction *and* additional time or attention required to use the system.

**Future, separate decision — Real actuation.** Only after independent engineering verification, clinical evaluation, appropriate regulatory assessment and a well-tested safety/fallback architecture. Nothing in this blueprint implies that camera-driven or autonomously adapting insulin delivery has been validated for live use.

## 15. Confirmed technical facts versus unresolved dependencies

**Claims carried over from the supplied specification, dated 24 October 2026. Reverify against the linked primary sources before implementation; this document update does not independently verify compatibility or medical claims:**

- Open-source Loop's released branch supports Omnipod 5 pods from v3.14.7; its documentation currently recommends v3.14.9 or later and describes an Omnipod 5 certificate/setup step. Insulet does **not** provide support for controlling the pods through Loop. Confirm regional availability and exact pod firmware before deciding on hardware.
- Loop has documented **Open Loop** prediction/recommendation mode and an **insulin pump simulator** for learning alongside another treatment setup. Open Loop should not be confused with a read-only security boundary.
- Tandem's Control-IQ, Insulet's native Omnipod 5 automated algorithm and open-source Loop are separate controller implementations. The pod model does not determine which algorithm is running.
- Standard Loop documentation describes selecting a CGM source, not built-in safety-certified fusion of two simultaneous CGMs.
- Apple Watch ECG is not a continuous stream from the standard ECG app; its ECG recording is user-initiated, and ECG data may be available as HealthKit samples.

**Generalisation requirement:** Separate shared software and population-level research priors from person-specific models and observations. Validate prospective accuracy, calibration, accessibility and burden across the intended populations; preserve negative results and avoid claiming universal benefit from one person’s experience.

**Still open:** two CGM models and data interfaces; model of watch and accessible physiological signals; actual controller for the first shadow run; actual-versus-requested insulin history interface; home-camera/smart-scale inventory; local compute platform; formulation compatibility and clinical suitability; quantified infusion-site response; and which context signals measurably outperform CGM/insulin alone.

## 16. The gold nuggets — keep these visible

> **The curve can become language.** Preserve the human capacity to learn by acting, observing, recognising mistakes and correcting.

> **The system's best output is returned human life.** Less attention, fewer unnecessary alarms, better sleep, more spontaneity and less family coordination are real outcomes.

> **Past behaviour informs the Bayesian belief state.** A carbohydrate event is not adequately described by carbohydrates alone; maintain a posterior over plausible current states rather than pretend the state is known.

> **Inference means revisable beliefs, not a magical confidence score.** Priors, sensor reliability, competing explanations and posterior predictive checks must be explicit and auditable.

> **Never invent independence.** Two CGMs can share physiological lag and failure modes; agreement is evidence only to the extent the error models justify it.

> **The critical object is relational capability.** Changing the controller changes the human–machine relationship, not just the pump software.

> **Automation should be conditional on what can actually be observed.** Rich sensing may enable more useful supervision, but missing or contradictory information must reduce confidence rather than invite aggressive compensation.

> **Two glucose sensors let us study measurement reliability, not certify truth.** Preserve disagreement; do not erase it through averaging.

> **Insulin delivery is not insulin action.** The changing infusion site is part of the process, and faster pharmacological action is a separate central objective.

> **The person's attention has a budget.** Doing more in well-understood situations can preserve attention for genuinely uncertain ones.

> **Train the human and the model alongside each other.** During calibration, preserve observations, predictions, the human's actual action and subsequent outcomes separately.

> **Agreement is not proof; plausible error detection matters.** We should study exactly when and why the system is wrong.

> **A camera detecting a cola is not a camera proving cola was consumed.** Event recognition, quantity estimation and treatment authority are separate layers.

> **The first implementation is a shadow system, not a new medical controller.** Prove observational value before contemplating any live-actuation path.

> **Distributed control; convergent consequence.** The body experiences the combined effects of sensor, insulin, pump, software, behaviour and infrastructure.

> **Information that cannot change action is telemetry, not feedback.** But premature action on unvalidated inference can be worse than no automation. Correction must be earned by evidence.

## 17. References and implementation starting points

- Loop pump compatibility: https://loopkit.github.io/loopdocs/build/pump/
- Loop releases: https://loopkit.github.io/loopdocs/version/releases/
- Loop Omnipod 5 setup: https://loopkit.github.io/loopdocs/loop-3/omnipod/
- Loop Open Loop mode: https://loopkit.github.io/loopdocs/operation/loop/open-loop/
- Loop simulator guidance: https://loopkit.github.io/loopdocs/loop-3/settings/
- Loop CGM support: https://loopkit.github.io/loopdocs/build/cgm/
- Tandem Basal-IQ versus Control-IQ: https://www.tandemdiabetes.com/support-center/pumps-and-supplies/automated-insulin-delivery/article/differences-between-basal-IQ-and-control-IQ
- Omnipod 5 native algorithm: https://www.omnipod.com/current-podders/resources/omnipod-5/faqs/omnipod-5-algorithm
- Apple Watch ECG: https://support.apple.com/en-us/120278
- HealthKit ECG samples: https://developer.apple.com/documentation/HealthKit/HKElectrocardiogram

**Final design rule:** Keep the **Bayesian shadow inference system** humble about what it knows, honest about what it observed, capable of recognising competing explanations and surprising evidence, incapable of silently changing insulin delivery, and useful enough that its eventual value can be measured as *human life returned*.
