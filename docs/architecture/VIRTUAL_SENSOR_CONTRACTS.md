# Minimal virtual-sensor contracts — proposed

PR #2 accepts the design requirements; these concrete API shapes remain proposed until the relevant implementation decision and tests resolve the [open choices](../PROJECT_DIRECTION.md#unresolved-engineering-decisions). Follow the [methodology](../METHODOLOGY.md) and link affected [claims and verification](../assurance/CLAIMS_MATRIX.md).

These are semantic design sketches for LIVE-004, LIVE-005, LIVE-012, LIVE-017–020 and LIVE-023, not implemented schemas or provider-specific request payloads. Use a small in-process registry and indexed synthetic evidence first. Historical investigation extends these contracts and the existing planner; it is not a separate analytics system. Keep measurement units, domain hypotheses and physiological models outside infrastructure-specific types.

## Source adapter

`SourceDescriptor` describes a stable ID/version, supported modalities and representations, units where relevant, sampling characteristics, local/remote location, permission purpose/scope/revision, retention/transmission restrictions, availability, expected latency and resource estimates. Modalities include scalar measurements, time series, images, audio, events and logs. Access and authorization are separate checks.

`ObservationEnvelope` contains immutable observation ID, source ID/version, the temporal provenance below, units, quality flags, missingness, clock uncertainty, correlation-group hints, permission revision, synthetic flag, and a bounded payload or authorized local payload reference. A content reference alone never grants access. Do not copy raw media into audit logs.

Candidate operations are capability discovery and bounded `read(window, deadline, permission_context)`. Missing, stale, unavailable and revoked are explicit outcomes. Consent revocation must stop future reads and dispatch; stored-data deletion/retention behavior is decided by policy, not silently by an adapter.

## Temporal provenance and knowledge boundaries

Use timezone-aware timestamps (UTC for storage), intervals where appropriate and explicit clock uncertainty. A field may be unknown; do not invent an event time from its later interpretation.

| Field | Meaning |
| --- | --- |
| `event_time` / `event_window` | When the physical event is believed to have occurred; inferred timing belongs to a versioned interpretation, not an edit of the recording |
| `recorded_at` / `recording_window` | When the source actually captured the measurement, image, audio or event |
| `ingested_at` | When the pipeline received/persisted the object; not necessarily when it became usable |
| `available_at` | Earliest actual availability of this specific object to the relevant consumer after necessary processing/access; record scope and a sequence number for equal timestamps |
| `execution_started_at` / `execution_completed_at` | When a detector, provider, query or inference actually ran; no backdating to event time |
| `published_at` / result `available_at` | When a derived result became consumable; old inputs do not give a new result an old availability time |
| `target_time` / `target_window` | The state or event a belief/interpretation concerns, independent of when it is inferred |
| `evidence_cutoff` | Latest permitted availability boundary for evidence and interpretations used in that snapshot, plus an exact input manifest |
| `model_version`, `sensor_version`, `question_version`, `registered_at` | Versions and availability of the processing definitions; later versions are not silently used in as-was replay |
| `retain_until`, `permission_revision` | Per-object retention/access constraints, including derived results and episode-index entries |

An observation can be available but unused. Each snapshot records the IDs actually admitted, their result availability and the definition/model versions actually used. An image stored at 12:30 does not make a 14:31 interpretation known at 12:30. A newly registered sensor may run on older compatible data now, but cannot appear in an original online snapshot. Clock ties use recorded ordering, not a convenient retrospective sort.

## Minimal searchable evidence memory

`HistoricalEvidenceQuery` is a bounded read through the same source/evidence contract: purpose and permission context, event/recording window, `knowledge_as_of`, source/modality/quality filters, required retained representation, optional compatible sensor version, result limit, deadline and resource budget. First implement an in-memory index over synthetic envelopes keyed by source, time and availability; a small episode table references these same evidence IDs. No large database, embeddings platform or duplicate raw store is required.

Support window retrieval, explicit retrieval of previously uninteresting events, and a bounded similar-episode query over documented synthetic features. Episode IDs, feature/extractor versions, availability, referenced windows and source leaves remain traceable. Similarity scores nominate evidence, not causes or independent facts. A feature, outcome or interpretation learned later cannot affect an as-of ranking. For present-day investigation it may be used only if actually available and currently authorized.

Filter authorization, retention and as-of availability before returning results or ranking candidates. Recheck access before payload resolution, inference dispatch and result admission. Return permitted references plus explicit completeness/coverage and absence reasons (`not_retained`, `expired`, `unavailable`, `denied`, `incompatible`, `no_match`) without leaking denied content. No match is not proof no event occurred. A metadata entry cannot reconstruct deleted audio/video or make a feature-only record sufficient for a raw-image sensor.

As-of replay never restores revoked permissions or deleted content: historical knowledge and current permission are both required. Retention applies to metadata, derived interpretations, snapshots and logs as well as media. When authorized deletion removes a dependency, preserve only permissible tombstones and mark replay incomplete; immutability forbids rewriting retained records, not authorized erasure. Availability of a useful historical question does not justify indefinite recording or retention.

## Virtual-sensor definition and registry

A `VirtualSensorDefinition` declares:

| Field group | Required meaning |
| --- | --- |
| Identity | Stable sensor ID, version, question and output schema version |
| Inputs | Required/optional modalities, source or derived-result selectors, purpose permissions, availability requirements |
| Time | Freshness limit, target and recording windows, trigger, clock-skew tolerance, deadline and whether historical execution is supported |
| Inference | Cheap and advanced alternatives, provider capabilities needed, model/question versions |
| Interpretation | Output type, alternatives and score/probability semantics, calibration reference or uncalibrated status |
| Dependencies | Upstream sensor IDs, raw evidence references, correlation groups, composition rules and known limitations |
| Policy | Expected information-value estimate with uncertainty, costs, escalation rule, stopping rule and budgets |
| Failure | Missing, stale, contradictory, OOD, timeout, refusal, invalid-output and revoked-permission behavior |

The registry maps IDs/versions to definitions and local implementations. Validate unique IDs, compatible inputs/output versions and acyclic dependencies. Adding a detector on a supported representation must not require edits to the Bayesian estimator's core. A new modality may require an adapter; this is not automatic support for every device.

A new sensor version declares compatibility with retained representations and permitted purposes. A bounded backfill selects explicit evidence IDs/windows, uses current permissions, and records the sensor/question/model versions, input manifest, configuration and mock response/seed needed for reproducibility. Outputs append new interpretation IDs with actual execution/availability times and optional `reinterprets_result_ids`/`backfill_run_id`; they never alter recordings or replace previous interpretations in place. Comparison views identify both versions and the target interval. Historical age is assessed against the question's target, not automatically rejected by a freshness rule intended for current-state observations.

## Result and evidence lineage

`VirtualSensorResult` references its definition/question, provider/model version, execution ID, input observation/result IDs, transitive raw leaf IDs, evidence cutoff/window, permission revision, interpretation/alternatives, score semantics, calibration status, quality/OOD flags and actual resource usage. Include estimated versus measured cost provenance. Results are immutable; corrections reference superseded results.

Historical results additionally carry target event/recording windows, execution and actual result-availability timestamps, query/backfill references and links to earlier interpretations. Reprocessing the same leaves with a new model does not create independent evidence. The triggering mismatch and any context passed to the provider must appear in lineage and dependence accounting too.

Possible statuses are `ok`, `unknown`, `missing`, `stale`, `contradictory`, `unavailable`, `timeout`, `refused`, `invalid_output`, `permission_revoked` and `cancelled`. `unknown` is not automatically probability 0.5, zero probability or a confirmed negative. A valid low detector score may still be uncalibrated.

Composition retains both derived and raw evidence references. Before a belief update, record which observation factor is added, replaced, jointly modelled or conservatively ignored. This prevents parent and child evidence from being counted independently. Lineage identifies overlap; it does not quantify correlation by itself.

## One BeliefSnapshot contract, separate temporal views

Extend LIVE-005's existing snapshot with `snapshot_id`, `inference_kind` (`online_filter`, `retrospective_smoother` or `retrospective_reanalysis`), `target_window`, `inferred_at`, `evidence_cutoff`, exact `evidence_manifest`, definition/model versions, `original_snapshot_ids`, `parent_snapshot_id` and revision reason. Preserve existing posterior, hypothesis, calibration and non-actuation fields. No separate historical belief authority is introduced.

An original online snapshot is append-only. A smoother estimates earlier states with later available evidence and produces a new snapshot. Reanalysis with a sensor/model invented later is explicitly distinguished from the original online run and from smoothing under the original model. An updated current belief may use the corrected past through the same transition model, but it too is a new snapshot.

`as_was` replay uses the original snapshots, exact admitted evidence, availability cutoffs and versions. `retrospective` replay names later evidence/interpretations and a new cutoff. Report original predictive scores separately from retrospective explanation quality; a revised historical estimate is never substituted into the original forecast. Missing authorized replay dependencies make the replay incomplete, not permission to substitute later versions or reconstruct the old answer.

## Provider-neutral bounded inference

`InferenceRequest` contains a request ID, virtual-sensor/question version, permitted selected evidence references, expected result kind, allowed labels if applicable, model capability requirements, deadline, resource limits, destination policy and cancellation context. It is an internal abstraction, not an OpenAI request schema.

`InferenceResult` contains status, typed value/distribution or explicitly absent answer, provider/model revision, input references, score meaning, usage and timing. Validate response type, labels, finite numeric ranges and input association before admitting evidence. Normalize refusal, unsupported modality, timeout and malformed responses without converting them to negative evidence.

Implementations may be thresholds, conventional signal processing, local ML, mocks or optional external providers. They return evidence only. They have no pump interface and cannot run actions named in an input or result. A live remote adapter is outside the first slice; [Decisions research](../research/DECISIONS_API.md) is a feasibility record.

## Acquisition decision and audit

`AcquisitionCandidate` identifies the target uncertainty, source/question/model tier, evidence already available, anticipated result space, expected benefit and its basis, cost vector, deadline and required permissions. Add an action kind (`fresh_observation`, `reanalyze_retained`, `historical_query`, `similar_episode_query`, `historical_sensor_run`, or `stop`), target window, knowledge-as-of boundary and retained-representation requirements. These actions share one ranking policy and budget; historical retrieval is not free or automatically useful. The first implementation may use a declared heuristic instead of estimated mutual information.

`AcquisitionDecision` records policy version, belief snapshot before selection, eligible/rejected candidates and reasons, selected action or `stop`, permission/budget snapshot, evidence requested, actual outcome, actual costs, resulting belief reference and unresolved gaps. Record estimated versus observed information gain separately from independently measured correctness.

For historical investigation include the mismatch/trigger ID, query and searched window, evidence/episode IDs returned, completeness, why those earlier events were relevant, old/new interpretation IDs and affected original/smoothed/current snapshot IDs. A proposed retrieval and any follow-up inference spend the same budget; re-rank after retrieval before deeper analysis rather than automatically escalating every returned item.

Apply hard permission and resource gates before candidate ranking and at dispatch/result acceptance. Stop on no worthwhile permitted candidate, deadline, unavailable evidence, revoked consent or exhausted budget. Log rejected requests without retaining disallowed content. A human clarification candidate has an explicit attention cost and remains disabled in the first slice.

## Decisions still required

Concrete serialization and units, retention/revocation policy, dependence approximation, likelihood calibration, budget defaults, value-of-information policy and provider selection are in the [project decision register](../PROJECT_DIRECTION.md#unresolved-engineering-decisions). Do not treat these sketches as a released API.
