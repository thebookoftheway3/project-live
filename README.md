# Project LIVE

**Open-source research for people with diabetes. North star: how much human life does the system give back?**

Project LIVE develops a context-aware insulin research system that models history, actively seeks useful evidence, preserves uncertainty and reduces the attention required for diabetes management. The work is public so people can study it, contribute, adapt it and benefit from it.

The **Context-Aware Insulin System blueprint**, including Revision 2’s Bayesian foundation and the general-purpose virtual-sensor and Active Historical Investigation extensions, governs the design. Its explicit foundation is a Bayesian belief state: distributions over plausible hidden states and competing explanations, updated as evidence arrives. A virtual sensor is a testable question about authorized evidence, independent of hardware. Cheap detectors trigger selective deeper inference; the same planner can also retrieve and reinterpret retained historical evidence to investigate a prediction mismatch. Original online snapshots remain distinct from later retrospective understanding, and the planner can stop with uncertainty. The Codex starter contributes useful scaffolding, not the project's ambitions.

The first deliverable is a non-actuating shadow system. Current code is a synthetic research example, not a treatment system. The broad mission is to benefit people with diabetes; usefulness and suitability across different people, diabetes types, therapies and devices still require evidence.

## Start here

- [Full public blueprint](PROJECT_BLUEPRINT.md)
- [Project direction and open decisions](docs/PROJECT_DIRECTION.md)
- [Virtual-sensor and Bayesian architecture](docs/architecture/SYSTEM.md)
- [Proposed first synthetic slice](docs/design/SYNTHETIC_VIRTUAL_SENSOR_SLICE.md)
- [Requirements and evidence](docs/requirements/LEDGER.md)
- [Implementation backlog](docs/BACKLOG.md)
- [Contributing](CONTRIBUTING.md)
- [Governance](GOVERNANCE.md), [code of conduct](CODE_OF_CONDUCT.md) and [security reporting](SECURITY.md)
- [Engineering methodology](docs/METHODOLOGY.md), [architectural decisions](docs/decisions/README.md) and [modularity principles](docs/architecture/PRINCIPLES.md)
- [Agent operating rules](AGENTS.md) and [verified security baseline / administrator checklist](docs/security/BASELINE.md)
- [Source provenance](docs/SOURCE_MANIFEST.json), [pinned upstream baseline](docs/UPSTREAM_BASELINE.json), and [setup evidence](docs/SETUP_STATUS.md)

The public blueprint retains the technical specification with personal history omitted. Original supplied documents remain in an ignored local archive.

## What runs today

The Python starter handles synthetic events, environment expiry, illustrative meal-context inference, deterministic replay and denial of all pump actions. Its hand-selected likelihood ratios do **not** implement the specified joint Bayesian state estimator or virtual-sensor framework. Live acquisition, glucose predictive distributions, calibration, active acquisition planning and product clarification prompts remain to be built.

The first [LIVE-022 beverage increment](docs/assurance/LIVE022_INCREMENT.md) adds a separate executable, 27-state synthetic Bayesian example: door/audio detection, one permission-checked mock image query, scale evidence and immutable online snapshots. It uses declared toy likelihoods and a small ambiguity heuristic, with no live inputs or treatment output. Historical investigation and the full LIVE-022 milestone remain incomplete.

With Python 3.11 or later:

```sh
python3 -m unittest discover -s tests -v
python3 -m project_live.cli replay data/synthetic_example.jsonl
python3 -m project_live.cli beverage data/synthetic_beverage_v1.json
```

CI runs the baseline on Python 3.11 and 3.12. Tests need no medical devices or personal records.

See the [CI and assurance review](docs/assurance/CI_REVIEW.md) for automated gates, [executed verification evidence](docs/assurance/CI_VALIDATION.md), and the separate [administrator checklist](docs/security/CI_ADMIN_CHECKLIST.md). Passing checks remain bounded synthetic evidence.

## Repositories and contributions

- [Project LIVE](https://github.com/thebookoftheway3/project-live): public design, sensing, shadow evaluation and synthetic tests.
- [LoopWorkspace fork](https://github.com/thebookoftheway3/LoopWorkspace): upstream build workspace and pinned components.
- [Loop fork](https://github.com/thebookoftheway3/Loop): upstream application source for reviewed modifications.

Contributions in modelling, accessibility, human factors, sensor integration, testing and documentation are welcome. Discuss substantial changes in an issue and submit focused PRs with reproducible evidence. Share synthetic examples rather than personal health records. No signing or deployment workflows are enabled in the Loop forks during research setup.

## License and data

Original Project LIVE code and documentation are provided under the [MIT License](LICENSE). Separate upstream projects and assets retain their own licenses; see [third-party provenance](THIRD_PARTY_NOTICES.md).

Open source means shared software and methods. Health records, raw recordings, identifiers, credentials and signing material stay outside version control. The initial research runtime cannot command a pump.

Engineering methodology and evidence: [safety methodology transfer assessment and evidence traceability](docs/assurance/TRANSFER_ASSESSMENT.md). This assessment does not establish clinical validation or authorize actuation.

Run the next bounded historical increment with `python3 -m project_live.cli history data/synthetic_history_v1.json`. It preserves online snapshots and emits a separate retrospective view; [executed evidence and remaining gaps](docs/assurance/LIVE022_HISTORY.md).
