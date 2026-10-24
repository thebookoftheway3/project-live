# Development and evidence

Project LIVE is open-source research for people with diabetes. Contributions from developers, researchers, clinicians and people with lived experience are welcome. Read `PROJECT_BLUEPRINT.md` Revision 2 and `docs/PROJECT_DIRECTION.md` before interpreting original starter plans. Preserve open design decisions as open.

Original contributions are accepted under the project’s MIT License. Keep third-party notices intact and identify the provenance of imported work. Use synthetic examples in public issues and PRs; do not upload personal health records.

Use small feature branches and pull requests. Each behavior change should identify its requirement, expected behavior, validation evidence and remaining limitations. Keep observational work separate from any future treatment-controller work. Do not put personal observations, original health narratives, credentials, signing material or identifiable recordings in Git.

## Local checks

Use Python 3.11 or later:

```sh
python3 -m unittest discover -s tests -v
python3 -m project_live.cli replay data/synthetic_example.jsonl
git diff --check
```

The existing tests exercise synthetic replay and selected constraints. They are not clinical validation or proof of a secure execution boundary. The meal estimator uses hand-selected illustrative likelihood ratios and does not forecast glucose.

## Upstream changes

LoopWorkspace pins component repositories using Git submodules. Record workspace and component commit IDs. Keep upstream release history intact; create development branches for local changes. Fork individual components only when needed for modifications, starting with the Loop app. Never edit dependencies without recording the resulting revision in the workspace.

Preserve upstream licenses and notices. Do not enable signing, deployment, or upload build workflows as part of initial fork creation. First verify an unmodified simulator build; report build failures and toolchain constraints explicitly.

## Review expectations

Use CI checks for pull requests and protect the main branch when the account supports it. Record actual remote enforcement separately from intended policy. Review timestamps, missing data, provenance, model calibration and independence assumptions for inference changes. New personal-data adapters require explicit data handling and non-interference evidence before use.
