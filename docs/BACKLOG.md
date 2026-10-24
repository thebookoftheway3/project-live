# Implementation backlog — virtual sensors and Bayesian inference

Integration revision 3 preserves existing IDs, extends LIVE-004/005/008/009/012, and adds only missing infrastructure/integration work. Priorities: P0 = first synthetic slice, P1 = following research/integration, P2 = later validated scope. Status refers to implemented research capability, not documentation or clinical validation.

Dependencies are engineering prerequisites, not a demand to finish a full framework. LIVE-022 is the **first implementation delivery**, implementing the smallest in-process subset of its dependencies together. LIVE-008 supplies fixtures and a posterior oracle; LIVE-022 owns their end-to-end composition, avoiding a circular dependency or duplicate demo task. LIVE-003/014 are independent later device tracks.

| ID | Work / linked requirements | Priority | Status | Dependencies | Measurable acceptance criteria |
| --- | --- | --- | --- | --- | --- |
| LIVE-001 | Synthetic replay foundation — R10/R12 | Foundation | Implemented | None | Existing seven tests pass; deterministic replay denies pump actions |
| LIVE-002 | Pin Loop workspace/dependencies | Foundation | Implemented | None | Exact recursive commit manifest and unchanged upstream baseline |
| LIVE-003 | Unmodified Loop simulator baseline | P1 | Pending | LIVE-002 | Reproducible simulator build/test results and recorded toolchain; independent of first slice |
| LIVE-004 | Generic source and observation contracts — R08/R10/R22 | P0 | Proposed in contracts | None | Fixtures exercise scalar/time-series/event/image/audio-feature/log envelopes; units, timestamps, missingness, permissions and freshness explicit; no live source required |
| LIVE-005 | BeliefSnapshot and hypothesis contracts — R19 | P0 | Proposed | LIVE-004 | Cutoff/version/provenance, alternatives and unavailable forecasts explicit; observations never promoted to confirmed actions |
| LIVE-006 | Confirmed real-action history — R11 | P1 | Pending | LIVE-004/005 | Separate command/delivery/effect semantics; shadow recommendations excluded from real-action input |
| LIVE-007 | Transparent physiological forecaster — R16 | P1 | Pending | LIVE-004/006 | Predictive intervals with chronological evaluation; no future-data leakage; baseline for later physiological models |
| LIVE-008 | Known-state synthetic evidence fixtures and posterior oracle — R15/R17 | P0 | Scenario specified | LIVE-004/005 | Hidden truth separated from inputs; independent finite-state posterior reference; cases include correlation, ambiguity, missingness and change points |
| LIVE-009 | Bayesian integration and sequential prototype — R15/R17/R18 | P0 context; P1 physiology | Not implemented | LIVE-005/008/017 | Context posterior matches oracle; normalization, joint evidence, lineage overlap and mismatch checks; one belief owner, no dosing |
| LIVE-010 | Calibration and policy/model comparison — R18/R27 | P0 harness; P1 broader study | Evaluation specified | LIVE-008/009/019 | Same held-out cases for cheap-only/fixed/progressive policies; proper scores, coverage where applicable, calls, latency and negative results; no single-trace calibration claims |
| LIVE-011 | Dual-CGM quality model — R17 | P1 | Pending | LIVE-004/009/010 | Separate traces, correlated/common-mode fault cases and source ablations; no automatic averaging |
| LIVE-012 | Information-value acquisition policy — R13 | P0 | Design extended | LIVE-005/008/017 | Explicit feasible candidates including stop, estimated benefit/cost and reasons; no-value, permission and budget controls make zero forbidden/unnecessary calls |
| LIVE-013 | Product clarification design — R14/D16 | P2 | Open decision | LIVE-012/015 | Evaluated timing, accessibility and attention cost; no answer remains unknown; disabled in first slice |
| LIVE-014 | Read-only device feasibility — R09 | P1 | Pending | LIVE-004; LIVE-003 for Loop route | Supported interfaces, acquisition rights and non-interference evidence; no device integration in this task |
| LIVE-015 | Generalisation/accessibility — R21 | P1 | Pending | LIVE-004/010 | Target populations and missing-hardware cases explicit; per-person models distinct from shared infrastructure |
| LIVE-016 | Public contribution/release process — R20 | Foundation | In place | None | License, provenance, PR/CI protection and documented review limits |
| LIVE-017 | Virtual-sensor contract and static registry — R23 | P0 | Proposed | LIVE-004 | Unique ID/version, question, input/output semantics and dependencies; reject cycles; swapping a sensor uses the same belief interface |
| LIVE-018 | Low-cost event detection — R24 | P0 | Proposed | LIVE-004/017 | Threshold/change detector triggers a bounded question; ordinary/no-event fixture causes no advanced call; trigger is not consumption confirmation |
| LIVE-019 | Progressive scheduler and budget enforcement — R24/R26 | P0 | Proposed | LIVE-012/018/020 | Cheap-first escalation, bounded requests, deadlines/cancellation; timeout/revoked/exhausted cases stop with auditable uncertainty |
| LIVE-020 | Provider-neutral adapters — R25 | P0 mock; P1 optional external | Contract and Decisions research only | LIVE-004/017 | Mock and local implementations share typed outputs; normalize unknown/refused/timeout/invalid; prove no OpenAI dependency. Live Decisions adapter deferred until interface/access/cost/privacy checks |
| LIVE-021 | Privacy, failure and resource evaluation — R26/R27 | P0 | Cases specified | LIVE-004/012/019/020 | Mid-run revocation, other-person, network-unavailable and budget tests; distinguish measured/simulated costs; zero unauthorized access/transmission |
| LIVE-022 | Synthetic multimodal vertical slice — R13/R15/R22–27 | P0 first delivery | Proposed; not built | Minimal LIVE-004/005/008/009/012/017–021 | Door → cheap audio feature → virtual sensor → selected mock image → Bayesian update → weight evidence → audit/replay. Initial milestone plus full alternative matrix in linked design; no live device, paid call, dosing or human prompt |

See [contracts](architecture/VIRTUAL_SENSOR_CONTRACTS.md), [first-slice design](design/SYNTHETIC_VIRTUAL_SENSOR_SLICE.md) and [decision register](PROJECT_DIRECTION.md#unresolved-engineering-decisions). Production plugin systems, applications in other domains and live treatment changes are outside this backlog expansion.
