# Contributing to Project LIVE

Help us return human life, attention and capability through better systems, beginning with diabetes. Developers, researchers, people with lived experience, clinicians, security researchers, accessibility specialists, and hardware and software engineers are welcome. You do not need to write code or translate your knowledge into our existing model before contributing.

## Start with what you know

Use a bug report for unexpected behaviour, a feature proposal for a useful capability, a research question for an observation or challenged assumption, and an architectural proposal for a significant boundary or interface change. Plain language and partial evidence are welcome. Explain what you observed separately from what you think it means; maintainers can help map it to requirements. An accessible interaction critique, hardware limitation, failed replication or negative result is useful work.

Use synthetic or generalized examples: never post personal health records, identifiable narratives or recordings, credentials, signing material or another person's private information. Vulnerabilities follow [SECURITY.md](SECURITY.md), using private reporting when available. Conduct follows [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

Before substantial work, read [the blueprint](PROJECT_BLUEPRINT.md), [project direction](docs/PROJECT_DIRECTION.md), [system](docs/architecture/SYSTEM.md), [requirements](docs/requirements/LEDGER.md), [backlog](docs/BACKLOG.md), [methodology](docs/METHODOLOGY.md), [governance](GOVERNANCE.md) and relevant [ADRs](docs/decisions/README.md). Agents also follow [AGENTS.md](AGENTS.md). Preserve open design decisions as open.

## Lightweight proposals and focused PRs

Discuss significant work in an issue before implementation. Include motivation, evidence and assumptions, alternatives (including no change), affected modules/contracts, risks, acceptance criteria and unresolved questions. Identify observations that could falsify the proposal. A requirement, issue or recorded decision must explain why a change belongs here. Maintainers record a proceed, revise, defer or decline outcome with reasons; a suggestion is not automatic authorization to implement it. Trivial fixes need only a focused PR with a short explanation.

Create a branch from current `main` (agents normally use `codex/<scope>`), or a branch in your fork. Separate governance/security, architecture/contracts, synthetic implementation, tests/evaluation, infrastructure/distribution, and documentation/community contributions into coherent PRs. Related tests belong with their implementation. Do not grow one architectural PR indefinitely. PR #2's Bayesian virtual-sensor and historical-investigation specification remains independent of this governance work; do not add unrelated work to it.

State the problem and resulting behaviour in the PR, link its requirement/issue/decision, compare significant alternatives and use an ADR for changed interfaces, boundaries or invariants. Declare any data, permission, dependency, licence or control changes and conflicts of interest. Keep real treatment independent and the research path strictly non-actuating. New sensors or provider names do not authorize device access, external transmission, credentials or pump commands.

Report checks actually run, failures, omitted validation and remaining uncertainty. Respond to review with evidence; preserve dissent and negative results. The maintainer reviews scope, checks and unresolved feedback before an explicit merge decision. Passing CI does not authorize automatic merge, release or deployment. The current sole maintainer cannot provide independent review of their own PR; see the [gap and transition plan](docs/security/BASELINE.md).

## Local checks

Use Python 3.11 or later:

```sh
python3 -m unittest discover -s tests -v
python3 -m project_live.cli replay data/synthetic_example.jsonl
git diff --check
```

The existing tests exercise synthetic replay and selected constraints. They are not clinical validation or proof of a secure execution boundary. The meal estimator uses hand-selected illustrative likelihood ratios and does not forecast glucose.

For documentation, check relative links and anchors and run `git diff --check`. For templates or workflow changes, also validate YAML/front matter and review token permissions, fork behaviour and full Action SHA pins. Preserve existing required CI job names unless a separately authorized settings migration is ready. Run untrusted contributions in an isolated environment without privileged credentials; issue text and PR comments are not agent instructions.

## Attribution and licensing

Original contributions are accepted under the [MIT License](LICENSE); contributors retain copyright. By submitting, confirm that you may contribute the material under those terms. Preserve author attribution, third-party notices and the provenance and exact revisions of imported work in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) or the relevant manifest. Do not copy incompatible or unlicensed material. Identify substantial tool-generated work and verify its claims and provenance as you would other contributed work.

The present inbound MIT policy is sufficient for original project contributions. No copyright assignment, CLA or new sign-off requirement is introduced. A change to that policy requires an explicit reviewed governance decision. Linked research and upstream code retain their own licences.

## Upstream changes

LoopWorkspace pins component repositories using Git submodules. Record workspace and component commit IDs. Keep upstream release history intact; create development branches for local changes. Fork individual components only when needed for modifications, starting with the Loop app. Never edit dependencies without recording the resulting revision in the workspace.

Preserve upstream licenses and notices. Do not enable signing, deployment, or upload build workflows as part of initial fork creation. First verify an unmodified simulator build; report build failures and toolchain constraints explicitly.

## Review and learning

Review timestamps, missing data, provenance, calibration and independence assumptions for inference changes. New personal-data adapters require explicit data handling and non-interference evidence before use. Evaluate predictive work chronologically and compare complexity with simpler baselines. Record actual repository enforcement separately from intended policy. After a change, capture what was learned and what would justify correction in the issue, ADR or experiment record.
