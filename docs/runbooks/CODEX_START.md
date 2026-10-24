# Contributor setup

Start with the root [AGENTS.md](../../AGENTS.md) and its required context, including the blueprint, direction, contributor workflow, governance, security, methodology and ADRs. The blueprint governs the research design; the original starter supplied a synthetic replay foundation. Root instructions follow [Codex's AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md); they are behavioural guidance, not security enforcement.

```sh
git clone https://github.com/thebookoftheway3/project-live.git
cd project-live
python3 -m unittest discover -s tests -v
python3 -m project_live.cli replay data/synthetic_example.jsonl
```

Use Python 3.11 or later. No sensor, pump, account credentials or personal data is needed for these checks.

For Loop investigation, use a separate checkout of LoopWorkspace and the exact revisions in `docs/UPSTREAM_BASELINE.json`. Retrieve recursive submodules and establish an unmodified simulator build before changes. Do not run signing or device deployment as a side effect of setup.

Use feature branches and PRs. Keep physiological records, recordings, identifiers and signing material out of Git. The current parser accepts synthetic data only.
