# ADR 0003: Snapshot Observation payloads as JSON values

- Status: **Accepted for the scoped synthetic payload safeguard, effective on PR #5 merge**.
- Decision authority: Project owner / current maintainer, through the explicit integration instruction of 2026-10-24; review was Codex-assisted, with no independent human approval.
- Date: 2026-10-24. Scope: synthetic Observation payload ownership; main R10/R19.
- Related: [PR #4 C-02/H-02/S-02/V-02 and E02 counterexample](https://github.com/thebookoftheway3/project-live/blob/932b258c524cf14f05b62a439d57508e9643fa48/docs/assurance/CLAIMS_MATRIX.md). This is an evidence addendum, not a copy of that matrix.
- Related accepted decisions: [ADR 0001](0001-modular-monolith-first.md) and [ADR 0002](0002-lightweight-assurance-traceability.md). This decision implements a scoped ownership safeguard; it does not implement the future virtual-sensor contract.

## Problem and alternatives

A frozen dataclass retains its payload reference. Mutating the input or a returned nested dictionary/list changes the stored observation. The desired behaviour is an isolated value snapshot through both `Observation.parse` and direct construction, preserving the existing dict/list interface.

| Approach | Assessment |
| --- | --- |
| Shallow copy | Fails for nested mutable objects. |
| Deep copy on construction only | Detaches input but callers can still mutate stored state through `event.payload`. |
| Deep copy on construction and every read | Viable, but retains a mutable internal tree and needs the same access mediation and type validation. Arbitrary Python objects can invoke custom copying hooks. |
| Recursively immutable mappings/tuples | Viable, but changes list equality/types and ordinary JSON serialization; custom containers/export conversion add surface area. |
| Canonical JSON used as equality/storage contract | An immutable value representation is useful, but sorted-key/text equality would change insertion order and Python numeric equality (`1 == 1.0`). No new canonical wire format is needed. |
| JSON text snapshot with detached reads (chosen) | Uses existing JSON-compatible shapes and standard-library encoding; immutable internal text, new plain dict/list tree on each read. Generated dataclass equality still compares values. Cost: decode/allocation on each read. |

## Decision and bounded contract

Store validated JSON text at construction and return a detached payload tree on access. A small [descriptor-typed dataclass field](https://docs.python.org/3.11/library/dataclasses.html#descriptor-typed-fields) retains constructor arguments, required `payload`, field order, generated equality, `asdict`, `replace` and representation. Consumers still use `.get`, indexing and ordinary `json.dumps(event.payload)`. Mutating the returned copy is allowed and has **no effect** on the observation; payload identity across reads is intentionally not retained.

Accept only a built-in dict root, string keys, nested built-in dict/list values and exact built-in `str`, `int`, finite `float`, `bool`, `None`. Preserve insertion/list order and scalar types; shared subtrees become independent JSON values. Reject tuples, sets, bytes/bytearrays, custom objects/container or scalar subclasses, non-string keys, cycles and non-finite numbers with `ValueError`; do not silently normalise them. Excessive nesting rejected by the interpreter becomes `ValueError`. Ordinary JSON scalar size/recursion limits still apply. This tightens formerly unchecked Python payload inputs to the existing JSONL value domain, including for direct construction.

The snapshot is compact JSON, not a new canonical-serialization standard. Same-input serialization and explicitly sorted-key JSON exports are deterministic under the tested runtimes. No new equality/hash semantics are introduced; Observation remains unhashable in practice because payload values are dictionaries. Timestamp handling and synthetic-only parsing are unchanged. No pump/device interface, replay algorithm or dependency changes.

This is an ownership safeguard for ordinary Python API access, not a sandbox. Hostile code using reflection, `object.__setattr__`, class mutation or internal attributes can defeat Python object protections. Concurrent mutation of input during construction, resource exhaustion, persistent storage and the future virtual-sensor pipeline are outside this claim. Large payloads may require a separately measured representation change; avoid a cache of shared mutable decoded values.

## C-02 traceability update and evidence E04

| Link | Scoped update |
| --- | --- |
| Claim C-02 | After successful construction, input and returned payload references cannot change the stored observation's JSON value. Does not establish future storage/virtual-sensor immutability. |
| Hazard H-02 | External aliases or downstream edits alter the original value without changing its identity. |
| Safeguard S-02 | Implemented immutable JSON snapshot and detached reads in `project_live/events.py`; strict validation rejects unsupported objects instead of retaining aliases. |
| Verification V-02 | `tests/test_observation_payload.py` exercises parse/direct input mutation, returned nested references, JSON types/order, equality, dataclass export/copy, shared subtrees, unsupported values/keys, cycles and JSONL round trips. |
| Evidence E04 | At regression-only commit `33c41fa`, two tests produced **four failing subtests** on Python 3.12.14. After the safeguard, all **15 tests** (7 existing + 8 new) pass locally on Python 3.12.14. Remote supported-version results are recorded in the implementation PR. |
| Scope/review | Limited software evidence for C-02/H-02/S-02/V-02 under the cases above; independent human review pending. E02 remains a valid historical counterexample at its old revision. Other C-02 storage/transform safeguards remain unverified. |

Reverse trace: E04 → V-02 → S-02 → H-02 → C-02 → R10/R19. The regression names and this record identify the forward path back to evidence. The integrated [claims matrix](../assurance/CLAIMS_MATRIX.md) links this addendum and retains E02 as historical; no other claim becomes supported by this fix. Evidence is tied to the implementation PR revision and must be reconsidered when payload construction/access, accepted types, serialization or consumers change.

Validation commands (Python 3.11/3.12 are the CI-supported matrix):

```sh
python3 -m unittest discover -s tests -p test_observation_payload.py -v
python3 -m unittest discover -s tests -v
python3 -m project_live.cli replay data/synthetic_example.jsonl
git diff --check
```

The bundled local interpreter was Python 3.12.14. The original and fixed replay outputs are byte-identical after `json.dumps(replay(...), sort_keys=True, separators=(',', ':'))`: SHA-256 `50b6cec3972c03832aea38c69a22c3cdee33d94f16eab6407c0b0197c19ed8ca`; all six records deny pump authorization. The existing deterministic replay test remains unchanged. This evidence does not establish clinical safety or future-information leakage prevention.

The owner-authorized integration accepts the bounded safeguard after diff review and successful required checks; no separate independent approval is claimed. Revisit if measured payload size/read frequency makes decoding costly or a new payload type is justified; retain the regression and explicit value/ownership contract in any replacement.

## Integration evidence — 24 October 2026

Updated against main `a243867` after PRs #3, #4 and #2. Merge commits retain regression-only `33c41fa` and safeguard `5dec906` without rewriting or squashing them. A fresh isolated extraction of the regression-only revision again produced two tests with four failing subtests on Python 3.12.14; the integrated branch passes all 15 tests. Runtime tree `e398586eac1e7e0f44dc52059336d994a7d45945`, test tree `c6cbbbdfcfd981fc3787c557a29b2a2af7268f78` and fixture tree `c341b599736322f8d5deded4a8b3c1ddc0416da0` are identical to `5dec906`. Its [Python 3.11/3.12 evidence](https://github.com/thebookoftheway3/project-live/actions/runs/40118084733) remains applicable to those artifacts; required CI is also rerun on this integration revision before merge. Replay retains the recorded digest above.

The C-02 forward/reverse links made the counterexample, safeguard and bounded tests reviewable without adding a framework. The integration exposed stale proposal/status references, now reconciled; upkeep time was not measured, and independent assurance remains absent. Reassess method cost during LIVE-022 rather than expanding the matrix for every trivial edit.
