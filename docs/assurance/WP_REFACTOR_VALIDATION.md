# WP1–WP4 / Surfer OS verification record (E09)

Date: 2026-11-16. Review branch: `codex/wp1-wp4-rd-monorepo`.
This record concerns the accompanying refactor tree; subsequent source changes
require rerunning affected checks. No independent human reviewer or clinical
validation is claimed. R01/R03/R07/R12/R14/R26/R27; partial C-01/C-04/C-06/C-07/
C-08/C-09, with [FMEA](../FMEA_SAFETY_ANALYSIS.md) and
[ADR 0004](../decisions/0004-work-package-research-monorepo.md).

## Baseline integration

| PR | Result | Merge revision |
| --- | --- | --- |
| #12 rumdl | Merged after original green CI | `be2a7ca9bcae16443c0b3377250eb44db3af81d5` |
| #14 zizmor | Resolved overlapping locks; fresh Python checks passed | `d5e7caa35cd16634be5af3b9860961a48bc724d4` |
| #15 Ruff | Preserved Dependabot's concurrent rebase; updated base and fresh Python checks passed | `6a0cb1f2597a084424a362bdf55e2a40faea9af0` |
| #11 consent-gated Loop consumer | Reviewed source/tests; fresh required Python 3.11/3.12 checks passed; merged cleanly | `0718c94402dceefb435c2adf06db3b7faf9b02dc` |

GitHub initially rejected #14 for conflicts and #11 for missing fresh required
checks. Neither protection was bypassed. A stale #15 push was rejected; the new
Dependabot head was fetched and retained. Baseline tests: 61 passed locally on
Python 3.12.14. All 21 mutation probes detected their intended violations; Ruff,
formatting, rumdl, templates and offline Zizmor passed. Tool-lock audit reported
no known vulnerabilities. PR #11's consent-before-read, CI real-data refusal,
bounded regular-file reads, private exclusive output and chronology were reviewed.

The annotated tag `v1.0-shadow-baseline` points to the #11 merge, with the requested
message `Baseline Bayesian shadow inference + read-only Loop consent ingestion`;
it is pushed to origin. The tag identifies the baseline committed tree.

## Exact move mapping

Executed after confirming #11 merged:

```sh
git mv project_live wp2-bayesian-voi-engine/src/project_live
ln -s wp2-bayesian-voi-engine/src/project_live project_live
```

All 12 original module names are unchanged: `__init__.py`, `bayes.py`, `cli.py`,
`context.py`, `environment.py`, `events.py`, `history.py`, `loop_observations.py`,
`pipeline.py`, `replay.py`, `safety_boundary.py`, `sensing.py`. Each maps from
`project_live/<name>` to `wp2-bayesian-voi-engine/src/project_live/<name>`.
Shared tests, fixtures, requirements and historical assurance documents stay at
root. New WP tests are included through `tests/test_work_packages.py`.

## Executed checks

Local interpreter: Python 3.12.14 in `/private/tmp/project-live-v2-venv`.
Verification tools: Ruff 0.17.4, rumdl 0.3.2, Zizmor 1.32.0, from the hash-locked
root requirements. `python3` below means that Python 3.12 interpreter on PATH;
the host's default `/usr/bin/python3` is 3.9.6 and is not used for these tests.

| Exact command / inspection | Observed result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` (via setup script) | 76 tests passed, including all 61 baseline tests |
| `python3 -m project_live.cli replay data/synthetic_example.jsonl` | Six deterministic records; pump authorization false in every record |
| `sh tools/check_mmu.sh` | C++17 compilation with warnings-as-errors and all host assertions passed |
| `PYTHONPATH=wp2-bayesian-voi-engine/src python3 -m unittest discover -s wp2-bayesian-voi-engine/service_tests -v` | Four API tests passed; in-process requests only |
| `ruff check .` | Passed with existing rule selection; all Python paths included |
| `ruff format --check .` | Passed, 34 Python files formatted |
| `rumdl check .` | Passed, 60 Markdown files checked, including WP documents |
| `python3 tools/check_templates.py` | All configured YAML and issue templates passed |
| `zizmor --offline --no-progress --strict-collection --persona auditor .github` | No findings |
| `python3 tools/check_negative_controls.py` | All 21 original mutation probes detected; relocated core still exercised |
| `python3 -m coverage run -m unittest discover -s tests -q`, followed by replay/API with `coverage run --append`, then `python3 -m coverage report` | Combined line/branch coverage 88%; 113 statements missed and 98 partial branches remain visible; no adequacy claim |
| `git diff --check` and `git diff --cached --check` | Passed |
| `LIVE_RESEARCH_API_TOKEN=<synthetic-test-token> docker compose -f wp2-bayesian-voi-engine/docker-compose.yml config --quiet` | Passed; no containers started |
| `python3 -m pip_audit --no-deps --disable-pip -r requirements/ci.txt` (JSON output saved outside Git) | No known vulnerabilities in baseline tool lock |
| `python3 -m pip_audit --no-deps --disable-pip -r wp2-bayesian-voi-engine/requirements-service.txt` | No known vulnerabilities in optional service lock |
| `swiftc -typecheck wp4-passive-ui-clients/ios-loop-telemetry/TelemetryView.swift wp4-passive-ui-clients/watch-1bit-companion/BinaryPromptView.swift -module-cache-path /private/tmp/live-swift-module-cache` | Passed on host SDK; Xcode cache/event-stream warnings; not an iOS/watch target build |
| Resolver environment: `python -m build --wheel --no-isolation --outdir /private/tmp/live-v2-dist` | Core wheel built; existing setuptools licence-table deprecation warning retained |
| Compare each of the 12 relocated module bytes against `git show v1.0-shadow-baseline:project_live/<name>` | All identical, including consent-gated consumer and CLI |
| Install the built wheel with `pip install --no-deps --target /private/tmp/live-v2-wheel-install`, then replay from `/private/tmp` with that target on `PYTHONPATH` | Passed; imported installed package outside checkout; wheel contains exactly the 12 baseline Python modules |

Local baseline and WP checks were also run together with
`PATH=/private/tmp/project-live-v2-venv/bin:$PATH sh tools/setup_research.sh`.
Python 3.11 verification for the refactor is delegated to the existing GitHub CI
matrix, not claimed as a local run. No subagents were used.

## Negative results and limitations

- Initial lint found two new import-order issues; fixed. The broadened Ruff scan
  also tried to format an old Markdown evidence example. Python file inclusion
  is now explicit, preserving the historical example and all existing lint rules.
- The first documentation check found six links to this not-yet-created record;
  the completed documentation is checked again before delivery.
- FastAPI's current Starlette TestClient warns that `httpx` support is deprecated.
  The pinned harness passes; replacing the client requires a separate dependency
  review. No warning is hidden.
- Host C++ assertions are bounded software evidence, not hardware unbypassability,
  DKA prevention, independent watchdog behavior or verified pump firmware fallback.
- G7/O5 BLE, +9 dBm, LTE-M/1NCE, ESP-IDF target build, physical enclosure fit,
  SAM 2/Depth Anything/VLM/Re-ID, Lua device execution and installable iOS/watch
  apps remain unverified integrations. Model weights and SDKs are not downloaded.
- The optional API has in-memory synthetic state, a single worker and no outbound
  voice call, clinical alert suppression or private Loop-data endpoint. Restart
  clears state; production persistence, transport/acknowledgement and external
  exposure are not established.
- Compose image metadata is pinned, but full stack build/runtime, image security
  scanning, modem timing and field KPIs are separate outstanding evidence.
- Synthetic geometry does not establish food accuracy; schema rejection does not
  establish whole-node zero-media egress. No human field study was conducted.
- New AGPL file scopes preserve the original MIT foundation. The OEM file records
  an option and rights dependencies, not an executed commercial agreement.

See [Surfer OS design](../SURFER_OS.md) and
[60-day plan](../GRANT_VERIFICATION_PLAN.md) for targets and unresolved choices.
