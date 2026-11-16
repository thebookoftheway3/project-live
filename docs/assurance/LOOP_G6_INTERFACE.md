# Loop G6 research observation interface v1

This implements the local Project LIVE consumer for the owner's selected route: **existing Dexcom G6 phone connection → restricted Loop research build → LIVE**. Independently operating treatment is unchanged. No CSV adapter, replacement CGM application or pump simulation is part of this change. Structure follows [ADR 0001](../decisions/0001-modular-monolith-first.md), evidence follows [ADR 0002](../decisions/0002-lightweight-assurance-traceability.md), and observation ownership follows [ADR 0003](../decisions/0003-observation-payload-snapshots.md).

## Producer boundary

The producer is a research scheme of the existing Loop target, reusing the G6 manager/settings and glucose chart. Its separate fork changes require their own build/package evidence. This Python consumer cannot prove phone isolation, transmitter coexistence or correct signing. No pump manager, command, treatment setting or credential is exposed by the interface.

The intended G6 path passively observes the official Dexcom app on the same iPhone. [LoopDocs](https://loopkit.github.io/loopdocs/loop-3/add-cgm/#dexcom-g5-g6-one) documents that prerequisite. [Tandem's guidance](https://www.tandemdiabetes.com/support-center/software-and-apps/tandem-tslim-mobile-app/article/using-tslim-app-with-dexcom-mobile-app) describes simultaneous phone and medical-device connections. These sources support feasibility, not proof that the modified research app has run without interference. No transmitter re-pairing, sensor restart or treatment configuration change is authorized by an interface document.

## Wire record

One UTF-8 JSON object per line, exactly these keys:

```json
{"schema":"project-live.cgm-observation","schema_version":1,"id":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","event_at":"2026-01-01T10:00:00Z","received_at":"2026-01-01T10:00:03Z","source":"loop.dexcom-g6","source_version":"loop-g6-passive-v1","unit":"mg/dL","glucose":100,"quality":{"is_display_only":false,"was_user_entered":false,"condition":null,"trend":null},"synthetic":true,"shadow_only":true,"may_actuate_insulin":false}
```

The example is synthetic. Real producer records set `synthetic=false`. IDs are stable lowercase SHA-256 identifiers; transmitter serials are not exported. All optional quality fields are explicitly present, with null where unavailable. Unknown schemas/fields, non-finite numbers, unsupported units/sources, invalid timestamps and any actuation authority are rejected. Input errors disclose line numbers and reason categories, never the offending record.

These are **processed G6 readings**, not raw electrical sensor signals. The pinned G6 integration clamps numeric values and carries range/quality conditions. The consumer preserves those labels and excludes any non-null condition, display-only or user-entered flag from its model. Upstream `wasUserEntered` is derived from display-only state; it does not independently prove a manual entry.

`event_at` identifies the measurement; `received_at` records actual phone reception, including delayed backfill. The consumer separately records its local Mac availability time. A phone-reception replay is not an original LIVE Mac forecast. Repeated IDs with identical content are idempotent; repeated reception retains the earliest reception. Conflicting contents fail. Different IDs for the same event are not independent evidence. Simultaneously conflicting readings are withheld; a later conflict does not rewrite an earlier snapshot.

## Local execution

Demonstrate with synthetic records first, writing outside Git:

```sh
python3 -m project_live.cli loop-replay data/synthetic_loop_g6_v1.jsonl --synthetic --output /private/tmp/live-g6-demo-report.json
```

Use a new output filename for each run. Existing reports are never overwritten. The command prints only completion, not observations. The input file is unchanged; the derivative is created with owner-only permissions. This interface has no networking capability.

After the verified research app receives real readings and the owner enables its local export, copy `observations-v1.jsonl` from that app's local files to a private, non-cloud folder outside this repository. No passwords, transmitter identifier, readings or screenshots need to be posted to GitHub or chat. Then run locally:

```sh
python3 -m project_live.cli loop-replay '/absolute/private/path/observations-v1.jsonl' --consent-local-health-data --output '/absolute/private/path/new-research-report.json'
```

Consent is explicit for each invocation before file access. Real-data mode is forbidden in GitHub Actions. Symlinks, known cloud-sync paths and nonregular inputs are rejected; reads are bounded to 25 MB and 50,000 records. Private input/output must be outside Git. These checks are not a sandbox or a complete inventory of sync software: choose a folder you know is local, protect the Mac account and remove private files when no longer needed. No automatic private-data upload or CI artifact is configured.

## Research replay and evidence E08

`loop_observations.py` preserves observation history and quality, replays by phone reception, and emits linked Bayesian local-level snapshots and prediction-versus-observation comparisons. A delayed older sample remains in history without retroactively changing a previously issued belief. Backfill is not scored as if received before the measurement. Five-minute cadence and a 7.5-minute gap flag are declared research assumptions, not a guarantee of backfill completeness.

The scalar Gaussian baseline assumes process variance 4 mg²/dL²/minute and measurement variance 25 mg²/dL², with no fitted physiological parameters. It reports means and variances, labelled unvalidated. Predictions are formed before assimilation; comparisons require the prior phone reception to precede the target measurement. No meal inference, insulin simulation, dosing output or treatment recommendation is produced. Existing synthetic beverage/history models remain unchanged and synthetic-only.

Executed locally on Python 3.12.14: **61 tests pass**, including 14 interface tests. The independent rational-number oracle checks the Bayesian update. Negative cases cover malformed/command-like records, quality exclusion, future availability, backfill, repeated/conflicting evidence, local consent, CI refusal, immutable input, exclusive owner-only output, Git/cloud/symlink rejection and nonregular inputs. Three additional mutation probes remove consent/CI refusal, availability filtering and quality exclusion; all are detected, bringing the suite to 21 probes. CI runs the same suite on Python 3.11/3.12. No real observations have been used for these tests.

A read-only agent review found missing cloud-source refusal and unbounded/nonregular input reads; both were fixed and tested. No independent human approval is claimed. E08 partially supports C-01/H-01/S-01/V-01, C-02/H-02/S-02/V-02, C-04/H-04/S-04/V-04, C-06/H-06/S-06/V-06, C-07/H-07/S-07/V-07, C-08/H-08/S-08/V-08 and C-09/H-09/S-09/V-09 in the [matrix](CLAIMS_MATRIX.md). It does not validate the phone producer, live coexistence, retention/erasure, clinical calibration or arbitrary host isolation. The containing commit pins this evidence's source, fixture and tests.
