# LIVE-022 first executable increment

Status: partial synthetic implementation, prepared for review on 24 October 2026. This implements the first independently reviewable beverage increment allowed by [LIVE-022](../BACKLOG.md) and the [slice plan](../design/SYNTHETIC_VIRTUAL_SENSOR_SLICE.md). It does not complete that milestone. Responsible review role: maintainer; no independent human review or clinical validation is recorded.

## Run and inspect

```sh
python3 -m project_live.cli beverage data/synthetic_beverage_v1.json
python3 -m project_live.cli beverage data/synthetic_beverage_v1.json --cutoff 2026-01-01T10:00:02Z
python3 -m unittest discover -s tests -v
```

Python 3.11/3.12 are the CI matrix. The first command emits one deterministic JSON record containing observed metadata, typed evidence outcomes, candidate decisions, mock call/read counters, simulated costs, five detached online snapshots, a denied pump authorization and an explicit list of missing capabilities. The cutoff command makes no mock call because the result would become available after its deadline. No files referenced inside the fixture are opened; the image reference is an inert string mapped by a local mock.

The normal fixture makes one mock call, admits three evidence records and retains all 27 possible identity × quantity × actor states. A scale decrease is ambiguous; neither consumption nor an actor becomes certain. The fixture's evaluation-only truth labels never reach the estimator. The original `replay` command remains unchanged.

## Implementation and assumptions

This is a scoped implementation under accepted [ADR 0001](../decisions/0001-modular-monolith-first.md), using separate in-process sensing, Bayesian state and orchestration modules. The static import inventory explicitly permits only these new edges. There is no new runtime dependency, plugin host, external provider, transport, command capability or accepted general-purpose sensor API. Preserving existing contracts and proving a small pure-Python composition was preferred over implementing a service framework or claiming the full proposed architecture exists.

- `sensing.py`: immutable scalar fixture samples, explicit availability/order/permission/retention, versioned inert provider, bounded one-call policy and dispatch/completion checks. Input declarations are synthetic test controls, not authentication or operating-system isolation.
- `bayes.py`: normalized joint table over 3 identities, 3 quantity classes and 3 actors, declared synthetic observation probabilities, conservative leaf/dependence-group withholding and immutable snapshots with manifests. Actor probabilities intentionally remain unchanged by these findings. `none` remains possible after a weight decrease.
- `pipeline.py`: a single scripted beverage episode with door/audio trigger, optional image query and scale comparison. It orders actual availability then recorded sequence; event time cannot make late evidence eligible. Mock execution advances a serial logical clock by one second. A consumed provider cannot be reused for a fresh run.

The model and likelihood versions are `beverage-toy-v1` and `synthetic-table-v1`. Sensor/policy versions appear in the output. Likelihoods are explicitly hand-authored probabilities for this experiment, not a conversion from provider confidence, fitted measurements or calibrated physiological evidence. Distinct declared dependence groups are assumed conditionally independent given the toy state; that assumption is unvalidated. Shared leaves/groups are withheld, not arbitrarily downweighted. Identical observation repeats are idempotent; conflicting IDs and ambiguous equal-time sequence keys fail.

The acquisition heuristic ranks a unit-cost mock image by current identity ambiguity against zero-benefit repeat-audio/stop candidates, then enforces threshold, permission, deadline and budget. This is not measured information gain or a general task planner. Revocation/expiry before dispatch produces zero provider reads. Revocation/expiry during the simulated call withholds the result; it does not erase historical snapshots or implement a retention store. Timeouts/refusals/invalid output are logged as failure, not negative evidence. Numerical impossible evidence returns unknown rather than a confident distribution.

## Executed verification: E06

Subject: this implementation's versioned fixture, runtime and tests, with the reviewed PR revision and exact hashes recorded below. Baseline is `3baa4a855dfe327dad90cf99d7feb13cc5ab0979`. Local interpreter: Python 3.12.14; tool versions remain in [the CI lock](../../requirements/ci.txt). Run the same gates on the exact PR revision in both CI matrix jobs before integration.

| Procedure | Actual local result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 35 tests passed: 23 baseline tests and 12 new tests |
| `python -m coverage run -m unittest discover -s tests -v`, followed by coverage-appended legacy replay | 91% combined statement/branch execution coverage; uncovered lines remain visible in CI |
| Independent rational-number posterior oracle | All 27 probabilities agree to 14 decimal places; actor uncertainty and nonzero alternatives preserved |
| Negative tests | Late arrival/deadline, duplicate/conflicting IDs, shared leaves/groups, denied/expired access, mid-flight revocation/expiry, budget, timeout/refusal/unknown/malformed output, mutable references and malformed numeric inputs exercised |
| `python tools/check_negative_controls.py` | 14 temporary-copy mutations detected, including removal of dependence withholding, completion permission/retention check and availability cutoff |
| Legacy replay | Six denied pump authorizations; unchanged canonical digest `50b6cec3972c03832aea38c69a22c3cdee33d94f16eab6407c0b0197c19ed8ca` |

The mock call/read positive control returns `(1,1)` before denied cases assert `(0,0)`. The malicious string test prevents fixture-reference file opens and observes an unchanged posterior; static boundary checks additionally reject network/device imports. These are bounded observations, not proof against adversarial Python code or arbitrary host effects. An initial mutation-harness run failed because formatting changed its exact replacement target; the target was corrected and all 14 probes rerun. That infrastructure failure is not counted as successful mutation detection.

E06 partially supports C-01/H-01/S-01/V-01 (non-actuation), C-02/H-02/S-02/V-02 (detached snapshots), C-04/H-04/S-04/V-04 (mock dispatch/admission checks), C-05/H-05/S-05/V-05 (mock expiry only), C-06/H-06/S-06/V-06 (declared dependence), C-07/H-07/S-07/V-07 (online availability cutoff), C-08/H-08/S-08/V-08 (typed failures), and C-09/H-09/S-09/V-09 (inert mock strings). See the [claim matrix](CLAIMS_MATRIX.md). These conclusions become stale when the relevant runtime, fixture, policy, likelihoods or tests change; rerun and review the argument.

## Remaining acceptance work

LIVE-022 is incomplete: no historical index/query, scripted 14:30 mismatch investigation, retrospective smoothing, next-day backfill, version migration, multiple episodes or comparative acquisition policies. No generic media processing, live sensing, physiological forecast, calibration, retention/deletion store, external-worker isolation, human interaction or device integration is implemented. Permission flags are not credentials. Statistical and independent security review remain absent. No inference can authorize insulin, and no treatment connection is introduced.

## Exact evidence subject

SHA-256 of the locally tested inputs below (the containing PR commit also pins all repository files):

| File | SHA-256 |
| --- | --- |
| `project_live/bayes.py` | `9da6e07c53be8f0683a30a7092318d73b384aee59a05304cad8d52255bae7690` |
| `project_live/sensing.py` | `d673672b2c6007b22312b27a61a8703f18789391469a977d67dd81f4e4feb48c` |
| `project_live/pipeline.py` | `a3304df714d4e38a598b194251813b7cf819735a9a531bfc63e15595b1c1ee28` |
| `project_live/cli.py` | `bd8a698f3f3527ddefb075c05d0b16a86c70984ed7cefb4b949f493f3cd0dbb1` |
| `data/synthetic_beverage_v1.json` | `9e760a82ef3e9ee499a74ef4c6d2d0bb14d97ad60d6480aaa33371fd78e61d9d` |
| `tests/test_bayesian_pipeline.py` | `898a06fde12783bcb6fd5ba73c40b8dfe871b424bf7b7437fd469f079b9d2956` |
| `tests/test_architecture.py` | `befdd384ddf82784e390b763cc77c341752e70374abbb9c7bfb0938e40199a0c` |
| `tools/check_negative_controls.py` | `3d8cbea7c5eb09071fd75e2a80f5c12ec46e898495886d580febd08c6970749b` |
