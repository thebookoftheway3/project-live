# Safety methodology and architecture transfer assessment

Status: **Engineering assessment; recommendations remain scoped as below**, 24 October 2026. No clinical validation, certification, demonstrated risk equivalence or actuation authorization is claimed. The question is which methods improve Project LIVE's research discipline, not how to transplant a traffic system. North star: **HOW MUCH HUMAN LIFE DOES THE SYSTEM GIVE BACK?**

Read with the [traceability method](TRACEABILITY.md), [initial matrix](CLAIMS_MATRIX.md), [ADR 0002](../decisions/0002-lightweight-assurance-traceability.md) and [validation record](VALIDATION.md).

## Integration status — 24 October 2026

PR #3 has merged as `4ab8501`, accepting the initial structure preference in ADR 0001. PR #4 adopts only the lightweight method through ADR 0002, links it into METHODOLOGY and the ADR register, and leaves the graph, semantic-transition design, provider isolation and future studies unapproved. PR #2 remains under separate integration review. The baseline table and assessment below preserve the pre-integration evidence and proposal states; they are historical context, not current merge status. The original source restrictions remain unchanged.

## Source handling and decision baseline

A privately supplied municipal engineering reference was read locally, limited to governance, control boundaries, logical architecture, data semantics, hazards, traceability, publication boundaries, pilot and deployment methodology. Commercial frameworks, partner addenda and product-specific interface details are not used or reproduced here. Publication rights to the original remain unestablished. No original, substantial passage, partner term, local path or source attachment belongs in this PR. The analysis below is independently written and confined to general methods and public LIVE evidence. Source assertions of deployment, certification, enforcement, reversibility and residual risk were not independently verified; descriptions of intended behaviour are not results.

| Baseline inspected | What it establishes for this assessment |
| --- | --- |
| [Main at 0a99fa7](https://github.com/thebookoftheway3/project-live/tree/0a99fa78ed9d2a7c818f90933afc93a448375de5) | Merged blueprint, R00–R21 and LIVE-001–016, including non-actuation, joint Bayesian research, chronological evaluation and attention costs. Most are requirements, not implemented capabilities. Current implementation is synthetic replay and illustrative grouped evidence. |
| [PR #2 at 2c31186](https://github.com/thebookoftheway3/project-live/tree/2c31186f753e5f6d1bfbcb3de075325bfd3915e1) | Unmerged proposals: generic virtual sensors, provider interfaces, historical investigation, exact lineage, permission/retention and temporal contracts; R22–R30 and LIVE-017–023 remain proposed. Read SYSTEM, VIRTUAL_SENSOR_CONTRACTS, ledger and backlog. Their specified acceptance tests are not execution evidence. |
| [PR #3 at 5886ed6](https://github.com/thebookoftheway3/project-live/tree/5886ed63c37fed876dd0a54c20ebd3c7ef224905) | Unmerged AGENTS, governance/security, methodology, modularity principles, ADR 0001 and Adaptive Perception Graph proposal. Used as the requested procedural reference. ADR 0001 remains **Proposed**; the graph is not an accepted design. |

This branch starts at main and adds a standalone methodology supplement; it is not stacked on either PR. References are pinned so review does not depend on silently changing proposals. No files from PR #3 are copied. Adoption should reconcile this supplement with the eventual methodology and ADR register; it does not accept either pending PR by implication.

Verification asks whether a defined property holds for a specified implementation and configuration. Validation asks whether the resulting system is suitable for its intended use. Neither a complete specification nor conformance to it guarantees that the right hazards were considered. The public [NASA verification/validation guidance](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) supports keeping these questions distinct; no domain certification is imported.

## Transferability decisions

The classes below describe transfer of a principle, not verification of its implementation. “Already covered” means the design obligation exists in the cited LIVE baseline; evidence may still be missing.

| Idea | Classification and reason | Evidence that could change the conclusion |
| --- | --- | --- |
| Link claims to hazards, safeguards and evidence; examine prohibited outcomes | Directly transferable. Makes the argument and counterexamples reviewable without inventing a controller. A complete set of links is not a complete hazard analysis. | A bounded implementation trial showing maintenance effort exceeds review value would justify simplifying the record. Missed hazards would require extending it. |
| Separate control, analysis, storage and publication trust boundaries | Transferable with modification. LIVE separates observation, inference, historical inquiry, evaluation and export; actual treatment stays outside the research system. Logical boxes alone enforce no permissions. | Capability/dependency analysis and deployment isolation tests can establish particular boundaries; they cannot authorize a new treatment path. |
| Preserve provenance and original historical meaning | Already covered in main R10/R19 and PR #2's proposed lineage and temporal contracts. Reuse those contracts; add assurance links rather than a second schema. | Implemented cross-component replay and export tests showing semantic loss would justify a focused contract correction. |
| Distinguish source roles and decision authority | Transferable with modification. Separate epistemic type from who may approve a policy or disclose data. An official record can be wrong about a physical event. | Review of concrete ambiguous records and lossless round trips could refine types; institutional endorsement alone cannot resolve empirical uncertainty. |
| Give official assertions unconditional precedence over conflicting measurements | Potentially misleading or unsafe if transferred to belief estimation. Preserve conflicting evidence and qualify assertions; policy authority controls permitted use, not physical truth. | A narrowly specified policy-precedence rule may be valid for permissions, but not as a blanket likelihood or truth rule. |
| Municipal institutions, network-control protocols and certified signal constraints | Domain-specific and not transferable. They allocate responsibilities and control behaviour in another domain; LIVE has no corresponding validated clinical authority model or controller envelope. | Only a separate domain-specific assessment could justify a limited interface analogy; it would not transfer certification. |
| Admit an intervention because sensor evidence meets a threshold | Potentially misleading or unsafe. Reliable observation does not establish intervention safety. LIVE must retain no pump-command path, not add a reusable insulin gate. | No result of this assessment authorizes actuation. That would require an entirely separate control architecture and authorization process. |
| Fault containment and graceful degradation | Transferable with modification. Protect other research responsibilities, stop unsafe data operations and expose unavailable estimates. “Still running” and “still safe” are distinct claims. | Fault injection plus resource/isolation analysis can support research continuity; neither establishes physiological safety. |
| Immediate override, rollback and reversible automation | Potentially misleading or unsafe as system-level guarantees. Disablement can stop future computation or transmission; it cannot retract consumed advice, disclosed data or earlier physical effects. | Measured stop latency and recovery tests can support scoped software claims. They cannot prove reversal of past interventions. |
| Provider replacement, open interfaces and data portability | Already covered in main R08 and PR #2/#3 proposals. Preserve semantic compatibility, calibration provenance and permission constraints, not just message shape. | Same-fixture adapter conformance, portability and provider-specific calibration tests could establish substitutability for a defined task. |
| No single sensor is required for correctness | Transferable with modification. Support missing hardware, but a missing critical observation can make an estimate unavailable. Sensor independence cannot be assumed from different brands/modalities. | Ablations, shared-failure cases and held-out performance determine which claims remain supportable with each available sensor set. |
| Progressive exposure and default-inactive capabilities | Transferable with modification. Separate evidence, permission and exposure decisions. Synthetic, authorized offline and read-only shadow studies are distinct scopes, not automatic rungs toward actuation. | Demonstrated non-interference, privacy controls and human-factors review may justify a particular research study, not a clinical stage. |
| Claimed equivalence to baseline residual risk or an incident-free pilot | Potentially misleading or unsafe. Common interfaces, labels and no observed incidents do not establish equivalent hazards, exposure or detectability. | Defined comparators, exposure and failure distributions, system analysis and independent review could support a bounded claim; none is supplied here. |
| Assign all downstream harm to another organization or a disclaimer | Domain-specific and not transferable as assurance. Contracts do not demonstrate failure containment; advice can affect people even with no machine command path. | Explicit responsibility interfaces, receiving-system behaviour and human-factors evidence can refine the hazard argument; legal allocation needs separate review. |

## Logical responsibilities and enforceable boundaries

Keep trusted first-party research modules within the proposed modular monolith where practical. Observation admission, inference, history queries, evaluation and export need explicit input/output responsibilities and semantic checks. Preserve one coherent logical Bayesian belief state per research subject; evaluation labels and retrospective results are not competing current-state authorities. The future graph scheduler changes neither those semantics nor permissions and needs separate review.

| Boundary | Required enforcement and its current limit |
| --- | --- |
| Research → treatment | No real pump client, credentials, writable device route or shared control dependency. Keep treatment independently operated and physically disconnected from experimental command paths. Future observational access needs permission/device restrictions and non-interference evidence, including shared resources. The deny-all class is useful but cannot prove isolation of an arbitrary host. |
| Untrusted result/plugin → host | Typed, bounded data only; no evaluation as code or instructions. Untrusted executable plugins need an OS/process or equivalent capability boundary with denied credentials, files, devices and network by default. A Python module boundary or text instruction is insufficient; no such plugin host is implemented here. |
| Historical query → retained data | Current authorization and retention enforcement before search/ranking, payload access, dispatch and result admission, including caches and derived indexes. A reference or old consent cannot grant present access. This is proposed in PR #2, not implemented in main. |
| Evaluation/history → online predictions | Isolate truth labels and later interpretations; preserve original cutoffs and versions. Enforce in storage/query APIs and tests, not only plotting conventions. Current event-time replay lacks the proposed availability model. |
| Research → people/publication | Separate permission to analyze from permission to display/export. Remove unauthorized data and preserve uncertainty, purpose and limitations. Test receiver interpretation and attention burden; a disclaimer cannot guarantee that advice has no effect. |

Data and publication protection may require filesystem permissions, credentials scoped to read-only interfaces, process isolation and network restrictions. These controls require concrete deployment evidence. No administrative setting or new distributed service is selected here.

A deterministic software rule such as denying a command can be tested against its defined interface. Physiological uncertainty, ambiguous observations, correlated errors and delayed physical effects do not inherit such a deterministic safety envelope. Even calibrated probabilities leave model and applicability questions; accurate observation is different from safe intervention. A repository maintainer can decide what code is accepted, but that role does not provide another person's consent or constitute clinical authorization. Responsibilities across users, clinicians, device providers and research operators need explicit review for any future study rather than a copied municipal hierarchy.

## Semantics without an authority hierarchy of truth

Recommend a future contract review using two independent questions: **what kind of assertion is this?** and **who is authorized to perform which operation with it?** Existing PR #2 object classes are the starting point; this assessment adds no competing wire schema.

- A policy/authorization record specifies permitted behaviour and its issuer, scope and validity. It does not establish a physiological observation.
- Reference definitions (units, identifiers, schema/model versions) explain other records. A valid identifier or precise conversion does not improve the source measurement's reliability.
- An observation records what a source reported, with quality, uncertainty and time. “Confirmed” must name the confirming source and scope; a reported delivery is not proof of absorption or effect.
- Derived interpretations, Bayesian estimates, forecasts and advisory outputs retain their assumptions and input dependencies. Deterministic conversion and probabilistic inference are different transformations, but neither acquires more empirical support merely by being transformed.
- Promotion is not an in-place type relabel. A justified confirmation creates a separate record with independent supporting evidence, responsible process and transition rule, preserving the original and remaining uncertainty. No transition grants treatment authority.

Reject a single rank that mixes authority, reliability and confidence. A derived advisory may also carry an institutional approval for publication; those are different attributes. Unknown provenance should be quarantined or explicitly unknown, not automatically admitted as a weak observation. A fresh timestamp does not restore stale permissions. Old evidence about a historical event need not decay merely because time passed; current applicability, retention and target-specific relevance need separate rules. These qualifications need a semantic ADR before schema changes.

Preserve source identity, transformation/version lineage, event and availability times, target interval, units, uncertainty/calibration, policy scope and permitted retention across adapters and exports. A lossy translation must declare the loss and withhold unsupported downstream claims. PR #2 already supplies most of this proposal; verify it rather than duplicate it.

## Degradation and staged research exposure

| Failure or exposure | Proposed non-actuating response / evidence obligation |
| --- | --- |
| Sensor missing, stale or contradictory | Record availability/conflict; withhold unsupported updates or use a declared model with explicit assumptions. Do not fabricate a negative observation or universally increase/decrease a scalar confidence. |
| Provider timeout, refusal, malformed result or worker crash | Reject invalid results, bound retries, preserve the last snapshot with its age/status, and mark current estimate unavailable where needed. Never substitute certainty or an arbitrary probability for failure. |
| Communications fail or reconnect | Stop affected acquisition; recheck permissions and cutoffs before queued work resumes. Suppress stale/duplicate results and record gaps. No treatment failover command is issued. |
| History expires, is deleted or revoked | Return permissible unavailability/completeness information; no reconstruction from cache, logs or embeddings. Exact replay may become impossible. |
| Bayesian update is numerically invalid or model mismatch is unresolved | Quarantine the update, retain previous versioned evidence and explicit failure, and stop dependent research conclusions as necessary. A conservative label is not a proof of physiological safety. |
| Recovery | Revalidate dependencies, consent, model/version and time; replay only permitted inputs. Show discontinuities. Recovery must not quietly reauthorize capabilities. |

Begin with synthetic fixtures and fault injection. Any later offline personal-data study requires explicit purpose/data authorization and privacy review. A read-only live shadow study additionally needs measured non-interference, resource limits, stop/recovery procedures and appropriate oversight. Human-visible research output is a further exposure: test comprehension, automation bias, misuse and interruption cost before presenting it as useful support. A physically non-actuating system can still influence treatment through a person.

No successful stage obliges the next. Pausing research leaves established treatment independent; it is not a prescribed clinical fallback. Physical delay, uncertain effects and effects that persist after commands stop make software rollback an inadequate intervention-safety argument. Predictive accuracy and observation reliability cannot answer an unobserved counterfactual treatment outcome. These limits are already present in main's blueprint; the traffic analogy does not relax them.

## Gap analysis and focused process changes

| LIVE baseline | Gap exposed / proportionate addition |
| --- | --- |
| Main R01/R07/R12; NoPumpAccess and tests | Narrow denial evidence exists. No complete deployment capability or non-interference assessment exists. Link tests and inspections to a scoped claim, without calling them system-level proof. |
| Main R10/R19; PR #2 immutable lineage proposal | Current frozen Observation holds a mutable payload alias (reproduced in E02). Add a future contract/implementation review and mutation tests; do not claim immutability from the dataclass annotation. |
| Main R03/R17/R18; PR #2 permissions/dependence/failure proposals | Most safeguards are specified but unbuilt. Attach explicit verification plans and status to each claim. Existing TTL and audio-group tests do not verify retention deletion or general dependency handling. |
| Main chronology requirement; PR #2 online versus retrospective views | Main sorts by event time and has no availability cutoff. Record absence of leakage-verification evidence rather than equating deterministic replay with chronological validity. |
| PR #3 lifecycle, governance and security | Already requires actual outcomes and review. Add a small claims/evidence supplement, evidence validity and reverse links; do not duplicate policy or fabricate independent reviewers. |
| PR #3 modularity and Adaptive Perception Graph proposal | Code organization is not security isolation; graph edges are not statistical independence. Require affected-claim review when these designs become concrete. No graph architecture change now. |

The original main-based assessment left PR #3 files unchanged. Integration now adds short methodology/principles links, a conditional template reference and ADR 0002 to the shared register; AGENTS already references methodology. Add claim IDs to affected requirement verification entries when implementations are scoped. No new framework, compliance tool, duplicated contract or global ledger renumbering is warranted.

## Decisions requiring further review

1. Evaluate the accepted ADR 0002 trial after the first implementation; decide evidence sufficiency per scoped claim and measure upkeep. No independent human review has occurred.
2. Resolve semantic confirmation/authority rules and payload immutability through focused contract work, coordinated with PR #2.
3. Define executable-plugin isolation and permission/retention enforcement before any untrusted worker or live data integration.
4. Define prospective evaluation, human-visible output safeguards and escalation evidence for a particular future study; no study is authorized here.
5. Reconcile contract references after PR #2 and payload evidence after PR #5. ADRs 0001/0002 have explicit integration decisions; this assessment selects no transport or scheduler.
6. Independently validate any future source-domain deployment or risk assertion before citing it as evidence. Source publication permissions remain unresolved and are not needed to publish this general assessment.
