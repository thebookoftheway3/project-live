# LIVE-022 bounded historical increment

Status: executable synthetic increment for review; LIVE-022 remains incomplete. Continues the [first increment](LIVE022_INCREMENT.md) and [existing slice](../design/SYNTHETIC_VIRTUAL_SENSOR_SLICE.md) under accepted [ADR 0001](../decisions/0001-modular-monolith-first.md), [ADR 0002](../decisions/0002-lightweight-assurance-traceability.md) and the detached-value ownership rule of [ADR 0003](../decisions/0003-observation-payload-snapshots.md). No architecture decision, runtime dependency, live acquisition or treatment authority is added.

## Run it

```sh
python3 -m project_live.cli history data/synthetic_history_v1.json
python3 -m project_live.cli history data/synthetic_history_v1.json --cutoff 2026-10-24T14:30:00+02:00
python3 -m unittest discover -s tests -v
```

The first command emits three views: `online_1230`, `online_1430` and `smoothed_1230_at_1431`. The second emits only the two original views and makes zero provider calls. Results include the sealed supplied forecast stimulus, evidence manifests, selected/stop reasons, retrieval exclusions and incomplete-coverage status, one local mock interpretation and call/read counters. All treatment authorization remains denied. JSON exports are detached; replaying at later cutoffs does not rewrite either earlier view or its supplied forecast.

## Implemented scope and assumptions

`history.py` adds one bounded in-memory episode to the existing sensing/Bayesian modules. A one-hour metadata query filters event window, actual availability, current permission, retention, source, representation and payload presence before ranking eligible frames. The existing inert provider checks permission/retention again at dispatch and completion. No reference inside a fixture is opened. Its payload-read counter represents a mock scalar lookup; the JSON fixture itself is loaded into memory. This is not a persistent index, erasure system, authenticated policy service or process sandbox.

The fixture records a cheap door/audio observation at 12:30, an uninterpreted retained frame, and a scripted mismatch at 14:30. The mismatch is one evidence item and also a planner trigger; the trigger does not add another likelihood. Declared fixture utility selects bounded history (0.7) over fresh acquisition (0.2), similar episodes (0) or stopping (0), subject to permission, threshold and the single-call budget. These are assumptions, not measured information gain. Fresh acquisition and similar-episode execution are not implemented.

The historical query runs at 14:30:06. Its one-second mock inference runs at 14:30:10–11, reusing the first increment's provider; this intentionally compresses the design sketch's longer execution. The interpretation records source leaves, target time, actual availability, sensor version/availability and question version. An earlier result cutoff prevents dispatch. The sensor-version introduction must predate the first online snapshot: later-invented versions require retrospective reanalysis rather than smoothing under the original model, and are stopped in this increment. A metadata-only, denied, expired, late or incompatible frame is unavailable history, never a negative consumption label. Coverage is always `partial` or `unavailable`, with completeness explicitly unestablished.

The model `history-two-node-toy-v1` enumerates 108 joint states: the existing 27 identity × quantity × actor states at the earlier episode, paired with four later explanations. This is a static two-node trajectory, not a physiological transition model. The original beverage command and likelihoods remain unchanged.

| Toy table | Explicit probabilities |
| --- | --- |
| Earlier beverage prior | Same product prior as the first increment: identity (0.25, 0.25, 0.5), quantity (0.5, 0.3, 0.2), actor (0.4, 0.3, 0.3) |
| Later explanation conditional on regular, nonzero quantity, self | Earlier beverage/activity/sensor-or-model-error/unresolved = (0.6, 0.15, 0.15, 0.1) |
| Later explanation otherwise | (0.05, 0.3, 0.3, 0.35) |
| Mismatch likelihood given explanation | (0.8, 0.6, 0.4, 0.2) |
| Opening/image observation likelihood | Reuses the declared first-increment table conditioned on earlier beverage state |

Filtering and smoothing normalize products over this same joint distribution. Evidence is applied once by ID and withheld when leaves or declared dependence groups overlap. Later interpretation reweights the earlier state and later explanation jointly; it does not retroactively improve an old forecast. The explanation labels and hand-authored likelihoods do not establish causation, calibration or whether an intervention would help. Evaluation truth is excluded from model inputs. No actor, quantity or explanation becomes certain.

## Executed evidence E07

Baseline: merged PR #9 at `d7b6a064d134af090ff7440daa7a0a370a29b145`. Local interpreter: Python 3.12.14; Python 3.11/3.12 remain the required CI matrix on the exact PR revision. The containing Git commit pins runtime, fixture, tests and this report. No independent human approval is recorded. A read-only agent review found a smoothing/reanalysis label ambiguity for sensor versions introduced between the online snapshot and query; this case now stops, with a regression test.

| Command or check | Observed local outcome |
| --- | --- |
| `python -m unittest discover -s tests -v` | 47 passing tests: 35 baseline plus 12 historical tests |
| Independent `Fraction` trajectory enumeration | All 108 probabilities in each of three snapshots agree to 14 decimal places; all alternatives remain nonzero |
| `python -m coverage run -m unittest discover -s tests -v`, appended legacy replay, `python -m coverage report` | 91% combined statement/branch coverage; missing paths reported, not treated as verified |
| `python tools/check_negative_controls.py` | 18 detected temporary-copy mutations; four new probes remove evidence cutoff, query cutoff, metadata-only refusal or sensor availability gate |
| Cutoff/immutability tests | Earlier serialized snapshots and supplied forecast unchanged after the historical interpretation; mutated exports cannot change stored values |
| Permission/retention/dependence tests | Zero forbidden dispatch/read after pre-dispatch denial; completion-time denial withholds result; duplicate query/evidence idempotent, conflicts rejected, shared leaves/groups withheld |
| Failure controls | Timeout/refusal/unknown/invalid or inert malicious reference cannot create evidence; missing history does not change the posterior |

An initial mutation rerun exposed stale Python bytecode when two temporary edits had the same size and timestamp. Python mutation subprocesses now disable bytecode writes; the copies exclude existing caches. The full suite of probes was rerun. A failed probe infrastructure run is not counted as successful detection.

For this fixture, the earlier-beverage explanation marginal moves from 0.0988889 (12:30) to 0.1834106 (mismatch) to 0.2745254 (retrospective image). Activity, sensor/model error and unresolved alternatives retain probability. These values reproduce the declared toy tables; they are not empirical confidence estimates.

Trace: E07 → C-01/H-01/S-01/V-01 (no actuation), C-02/H-02/S-02/V-02 (detached views), C-04/H-04/S-04/V-04 (current mock permission), C-05/H-05/S-05/V-05 (retention eligibility), C-06/H-06/S-06/V-06 (unique/dependent evidence), C-07/H-07/S-07/V-07 (as-of and separate smoothing), C-08/H-08/S-08/V-08 (unknown/failure), C-09/H-09/S-09/V-09 (inert references). The [matrix](CLAIMS_MATRIX.md) links back here. All conclusions are scoped synthetic evidence and become stale on relevant source, fixture, policy, likelihood or test changes.

## Remaining executable work

Next small LIVE milestone: versioned next-day reinterpretation of compatible retained frames, preserving the original interpretation and availability, with an explicit shared-leaf replacement/withholding rule and tests excluding later versions from earlier views. Then compare fresh-only and history-enabled policies under equal budgets and knowledge cutoffs. Similar-episode search, feature/training leakage, multiple episodes, sensor-version comparison and the full scenario family remain unimplemented.

No persistent retention/deletion, authenticated consent, external worker isolation, real observations, physiological forecast, clinical calibration or human/treatment validation is established. The scripted forecast is a fixture constant, never generated from the later observation. A simulated software result cannot validate real-world insulin control.
