# CI verification evidence E05

Executed 24 October 2026 on `codex/ci-assurance-gates`, based on main `22f01c0edf1d156d798b825c18bdf204e9490b49`. This record supports **C-01/H-01/S-01/V-01** for the current synthetic starter. Forward link: [claims matrix](CLAIMS_MATRIX.md); rationale and limitations: [gap review](CI_REVIEW.md). Existing E01–E04 remain historical evidence at their stated subjects. No claim is upgraded to system-level supported.

## Local execution

Interpreter: Python **3.12.14**. Tools: Ruff **0.17.2**, zizmor **1.31.1**, rumdl **0.3.0**, coverage.py **7.17.0**, pip-audit **2.10.1**, PyYAML **6.0.3**. The hash-locked graph is in [ci.txt](../../requirements/ci.txt); [ci.in](../../requirements/ci.in) identifies direct tools. Commands below used the isolated tool environment's interpreter/binaries, not the unsupported system Python 3.9.6.

| Exact command/check | Observed result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 23 tests pass: 15 existing regressions, 2 architecture, 3 non-actuation, 3 traceability/lock checks. |
| `python -m coverage run -m unittest discover -s tests -v` then `python -m coverage run --append -m project_live.cli replay data/synthetic_example.jsonl` | Suite passes; six CLI records, all `pump_authorization: false`. |
| `python -m coverage report` | 193 statements, 10 missed; 68 branches, 10 partial; combined displayed coverage 92%. Missed cases include invalid prior/feature, missing/invalid environment, several malformed observation paths, recursion-limit handling and blank JSONL lines. No new assertions are inferred from line execution. |
| `ruff check project_live tests tools` / `ruff format --check project_live tests tools` | Pass after formatting/import sorting. No research logic edits. |
| `zizmor --offline --no-progress --strict-collection --persona auditor .github` | No findings. Offline-only audits; no GitHub security settings or upstream Action source audit implied. |
| `rumdl check .` / `python tools/check_templates.py` | Local file/fragment/reference links and YAML/template front matter checked. External URLs and GitHub template rendering are outside this check. |
| `python tools/check_negative_controls.py` | Eleven synthetic mutations rejected with nonzero exit and expected diagnostics, listed below. |
| `python tools/check_negative_controls.py --audit-only` | Known-vulnerable `django==1.2` metadata returned vulnerabilities and exit 1; no vulnerable package was installed or imported. |
| `python -m pip install --require-hashes --only-binary=:all: -r requirements/ci.txt` then `python -m pip_audit --no-deps --disable-pip -r requirements/ci.txt --format json -o audit.json` and `python tools/ci_summary.py --check-audit` | Installation succeeds; all 34 pinned packages audited, none skipped, no known vulnerabilities reported. Clean CI installation still needs the remote matrix result. |
| `git diff --check` | Pass. CI also compares committed changes to PR base/push-before SHA; a clean working-tree check alone is insufficient. |

Runtime source comparison against `origin/main` found all seven ASTs identical after normalizing only import statement/name ordering. Canonically exported replay retains SHA-256 **50b6cec3972c03832aea38c69a22c3cdee33d94f16eab6407c0b0197c19ed8ca**, matching ADR 0003. The synthetic fixture is unchanged. This supports unchanged tested behaviour, not a proof for every possible input.

## Negative controls and failed attempts retained

All mutations occur in temporary copies. No synthetic violation is committed into the runtime, workflow or claims record.

| Mutation | Expected observed rejection |
| --- | --- |
| Undefined Python symbol | Ruff `F821`, exit 1 |
| Unformatted Python statement | Ruff format `would be reformatted`, exit 1 |
| Observation module imports replay | Architecture unittest `unreviewed import edge`, exit 1 |
| Context module imports socket transport | Architecture unittest `unreviewed import edge`, exit 1 |
| Missing Markdown file | rumdl `MD057`, exit 1 |
| Missing heading fragment | rumdl `MD051`, exit 1 |
| Action SHA replaced with tag | zizmor `unpinned-uses`, exit 14 |
| Workflow token changed to write | zizmor `excessive-permissions`, exit 14 |
| C-01 points to undefined E99 | Traceability unittest `undefined evidence`, exit 1 |
| Deny authorization changed to allow | Non-actuation unittest `True is not False`, exit 1 |
| Execute method returns instead of denying | Non-actuation unittest `PermissionError not raised`, exit 1 |

The first format probe expected an older Ruff diagnostic spelling and correctly refused to count that run as verified; the expectation was corrected. An initially unquoted YAML command ending in `:all:` failed parsing; it is now a YAML block scalar. zizmor's regular persona suppressed the synthetic top-level write-permission finding, so the real gate and probes now use the auditor persona. Both genuine findings and harness problems are retained here rather than counted as successful checks. No unsafe runtime mutation survived a completed control run.

Expanding the scan from workflows to all `.github` definitions also found insufficient Dependabot cooldowns in both ecosystems. Explicit seven-day version-update cooldowns resolve those findings. No repository security setting was changed.

## Evidence boundaries and remote verification

E05 demonstrates static import restrictions and tested denial/inert-input behaviour only. Reflection, hostile in-process code, independent treatment deployment isolation, full semantic traceability, private data handling and future workers remain unverified. The mock observer detects calls to the current exposed execute method; it cannot observe an unknown transport. That is why the separate import/dependency inventory and independent review matter.

The PR's checks record actual Python **3.11 and 3.12** executions at their workflow revision. Local Python 3.12 evidence alone does not establish Python 3.11 support. Remote results and dependency audit outcomes are recorded after execution below. Job summaries distinguish step success/failure/skipped states, measured missing coverage and unchanged claim limitations. Missing reports are labelled unavailable. No independent human review, clinical evaluation, standards compliance, deployment or release approval is asserted.

Re-run and reassess applicability on changes to runtime, tests, fixture, tools, permissions, workflows or claims. CI logs may expire; retain the source commands/lock and meaningful counterexamples, and rerun at the review revision rather than silently reusing an older pass.
