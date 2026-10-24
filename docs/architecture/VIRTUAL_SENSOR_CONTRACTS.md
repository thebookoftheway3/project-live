# Minimal virtual-sensor contracts — proposed

These are semantic design sketches for LIVE-004, LIVE-005, LIVE-012 and LIVE-017–020, not implemented schemas or provider-specific request payloads. Use a small in-process registry first. Keep measurement units, domain hypotheses and physiological models outside infrastructure-specific types.

## Source adapter

`SourceDescriptor` describes a stable ID/version, supported modalities and representations, units where relevant, sampling characteristics, local/remote location, permission purpose/scope/revision, retention/transmission restrictions, availability, expected latency and resource estimates. Modalities include scalar measurements, time series, images, audio, events and logs. Access and authorization are separate checks.

`ObservationEnvelope` contains immutable observation ID, source ID/version, observed and received timestamps, temporal window, units, quality flags, missingness, clock uncertainty, correlation-group hints, permission revision, synthetic flag, and a bounded payload or authorized local payload reference. A content reference alone never grants access. Do not copy raw media into audit logs.

Candidate operations are capability discovery and bounded `read(window, deadline, permission_context)`. Missing, stale, unavailable and revoked are explicit outcomes. Consent revocation must stop future reads and dispatch; stored-data deletion/retention behavior is decided by policy, not silently by an adapter.

## Virtual-sensor definition and registry

A `VirtualSensorDefinition` declares:

| Field group | Required meaning |
| --- | --- |
| Identity | Stable sensor ID, version, question and output schema version |
| Inputs | Required/optional modalities, source or derived-result selectors, purpose permissions, availability requirements |
| Time | Freshness limit, temporal window, trigger, clock-skew tolerance and deadline |
| Inference | Cheap and advanced alternatives, provider capabilities needed, model/question versions |
| Interpretation | Output type, alternatives and score/probability semantics, calibration reference or uncalibrated status |
| Dependencies | Upstream sensor IDs, raw evidence references, correlation groups, composition rules and known limitations |
| Policy | Expected information-value estimate with uncertainty, costs, escalation rule, stopping rule and budgets |
| Failure | Missing, stale, contradictory, OOD, timeout, refusal, invalid-output and revoked-permission behavior |

The registry maps IDs/versions to definitions and local implementations. Validate unique IDs, compatible inputs/output versions and acyclic dependencies. Adding a detector on a supported representation must not require edits to the Bayesian estimator's core. A new modality may require an adapter; this is not automatic support for every device.

## Result and evidence lineage

`VirtualSensorResult` references its definition/question, provider/model version, execution ID, input observation/result IDs, transitive raw leaf IDs, evidence cutoff/window, permission revision, interpretation/alternatives, score semantics, calibration status, quality/OOD flags and actual resource usage. Include estimated versus measured cost provenance. Results are immutable; corrections reference superseded results.

Possible statuses are `ok`, `unknown`, `missing`, `stale`, `contradictory`, `unavailable`, `timeout`, `refused`, `invalid_output`, `permission_revoked` and `cancelled`. `unknown` is not automatically probability 0.5, zero probability or a confirmed negative. A valid low detector score may still be uncalibrated.

Composition retains both derived and raw evidence references. Before a belief update, record which observation factor is added, replaced, jointly modelled or conservatively ignored. This prevents parent and child evidence from being counted independently. Lineage identifies overlap; it does not quantify correlation by itself.

## Provider-neutral bounded inference

`InferenceRequest` contains a request ID, virtual-sensor/question version, permitted selected evidence references, expected result kind, allowed labels if applicable, model capability requirements, deadline, resource limits, destination policy and cancellation context. It is an internal abstraction, not an OpenAI request schema.

`InferenceResult` contains status, typed value/distribution or explicitly absent answer, provider/model revision, input references, score meaning, usage and timing. Validate response type, labels, finite numeric ranges and input association before admitting evidence. Normalize refusal, unsupported modality, timeout and malformed responses without converting them to negative evidence.

Implementations may be thresholds, conventional signal processing, local ML, mocks or optional external providers. They return evidence only. They have no pump interface and cannot run actions named in an input or result. A live remote adapter is outside the first slice; [Decisions research](../research/DECISIONS_API.md) is a feasibility record.

## Acquisition decision and audit

`AcquisitionCandidate` identifies the target uncertainty, source/question/model tier, evidence already available, anticipated result space, expected benefit and its basis, cost vector, deadline and required permissions. The first implementation may use a declared heuristic instead of estimated mutual information.

`AcquisitionDecision` records policy version, belief snapshot before selection, eligible/rejected candidates and reasons, selected action or `stop`, permission/budget snapshot, evidence requested, actual outcome, actual costs, resulting belief reference and unresolved gaps. Record estimated versus observed information gain separately from independently measured correctness.

Apply hard permission and resource gates before candidate ranking and at dispatch/result acceptance. Stop on no worthwhile permitted candidate, deadline, unavailable evidence, revoked consent or exhausted budget. Log rejected requests without retaining disallowed content. A human clarification candidate has an explicit attention cost and remains disabled in the first slice.

## Decisions still required

Concrete serialization and units, retention/revocation policy, dependence approximation, likelihood calibration, budget defaults, value-of-information policy and provider selection are in the [project decision register](../PROJECT_DIRECTION.md#unresolved-engineering-decisions). Do not treat these sketches as a released API.
