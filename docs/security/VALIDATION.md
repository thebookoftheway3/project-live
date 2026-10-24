# Governance/security change validation

Prepared 24 October 2026 on `codex/governance-security`, branched from public main `0a99fa78ed9d2a7c818f90933afc93a448375de5`. Traceability: R20 and LIVE-016, plus the requested governance/security foundation. The [security baseline](BASELINE.md) records configuration observations independently of these software/documentation checks.

## Local results

| Check | Actual outcome |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | First invocation used system Python 3.9.6 and passed 7 tests, but that runtime is below the declared minimum and is not supported-version evidence. Repeated with bundled Python **3.12.14**: all **7 tests passed**. |
| `python3 -m project_live.cli replay data/synthetic_example.jsonl` | Python 3.12.14: **6 records**, every `pump_authorization` false. No live data/device access. |
| `git diff --check` and whitespace check of new text files | Passed. |
| Relative Markdown links and fragments | Checked repository Markdown paths and heading anchors against tracked and new non-ignored files; passed. External URL availability is not covered by this local check. |
| YAML and issue-template front matter | Ruby `YAML.safe_load` parsed Dependabot, issue chooser, four issue templates and the unchanged test workflow successfully; inspected required template fields and Dependabot configuration. No GitHub-rendered issue submission was tested. |
| CODEOWNERS | Locally inspected all-file coverage, syntax and owner; every ownership entry names only verified administrator `@thebookoftheway3`. GitHub validation on the branch is checked after publication; see PR evidence. Ownership is not independent review. |
| Scope | No changes to `project_live/`, `tests/`, `data/`, `pyproject.toml`, the existing workflow, blueprint, SYSTEM.md, direction, requirements ledger or backlog. No perception implementation or insulin-research architecture modification. |
| Agent guidance | Root AGENTS.md is 57 lines, under the requested 100-line target. |

For the supported local run, `python3` above was explicitly invoked as `$RUNTIME_PYTHON`, pointing to the desktop-bundled Python 3.12.14 executable; no dependency installation was needed. Reproduce the first two commands using any configured Python 3.11+ interpreter, then `git diff --check`. YAML parsing command:

```sh
ruby -e 'require "yaml"; ARGV.each { |p| text = File.read(p); text = text.split(/^---\s*$\n/)[1] if p.end_with?(".md"); YAML.safe_load(text); puts "PASS #{p}" }' .github/dependabot.yml .github/ISSUE_TEMPLATE/config.yml .github/ISSUE_TEMPLATE/*.md .github/workflows/shadow-tests.yml
```

## Remote checks and limitations

This record is prepared before publishing the commit; use the PR's checks and description for the actual remote Python 3.11/3.12 results and branch CODEOWNERS validation. Do not infer a remote pass from local tests.

PR #2 was verified open at `2c31186f753e5f6d1bfbcb3de075325bfd3915e1` before this work; its branch is not a parent of this governance branch. The final PR evidence must confirm it remains unchanged and open. Neither PR is authorized for merge.

No independent human review, clinical validation, hostile-fork test, exhaustive secret/privacy scan, OpenSSF Scorecard run, Best Practices badge assessment, reproducible release build or organization migration was performed. GitHub settings, administrative privileges, credentials and the non-actuating runtime boundary were not changed. The proposed Dependabot file will request update PRs only after adoption; it is not evidence that security updates are enabled.

## Integration review — 24 October 2026

The earlier no-merge authorization statement above records preparation-time scope. The project owner has now explicitly authorized reviewed integration in order #3, #4, #2, #5. PR #3 is current with main `0a99fa7`; no review submissions, discussion comments or unresolved review threads were returned. ADR 0001 records acceptance of the initial implementation preference effective on merge and the independent-review gap. Governance changes add no privileges, credentials or runtime capability. Disabled security controls remain tracked administrator actions, not asserted safeguards. Required CI must pass on this reconciled revision before merge; actual remote results are recorded in PR #3.
