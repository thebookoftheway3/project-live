# Project LIVE

**Open-source research for people with diabetes. North star: how much human life does the system give back?**

Project LIVE develops a context-aware insulin research system that models history, actively seeks useful evidence, preserves uncertainty and reduces the attention required for diabetes management. The work is public so people can study it, contribute, adapt it and benefit from it.

The **Context-Aware Insulin System blueprint**, including Revision 2’s Bayesian foundation and the general-purpose virtual-sensor addendum, governs the design. Its explicit foundation is a Bayesian belief state: distributions over plausible hidden states and competing explanations, updated as evidence arrives. A virtual sensor is a testable question about authorized evidence, independent of hardware. Cheap detectors trigger selective deeper inference; the planner asks the next useful question and can stop with uncertainty. The Codex starter contributes useful scaffolding, not the project's ambitions.

The first deliverable is a non-actuating shadow system. Current code is a synthetic research example, not a treatment system. The broad mission is to benefit people with diabetes; usefulness and suitability across different people, diabetes types, therapies and devices still require evidence.

## Start here

- [Full public blueprint](PROJECT_BLUEPRINT.md)
- [Project direction and open decisions](docs/PROJECT_DIRECTION.md)
- [Virtual-sensor and Bayesian architecture](docs/architecture/SYSTEM.md)
- [Proposed first synthetic slice](docs/design/SYNTHETIC_VIRTUAL_SENSOR_SLICE.md)
- [Requirements and evidence](docs/requirements/LEDGER.md)
- [Implementation backlog](docs/BACKLOG.md)
- [Contributing](CONTRIBUTING.md)
- [Source provenance](docs/SOURCE_MANIFEST.json), [pinned upstream baseline](docs/UPSTREAM_BASELINE.json), and [setup evidence](docs/SETUP_STATUS.md)

The public blueprint retains the technical specification with personal history omitted. Original supplied documents remain in an ignored local archive.

## What runs today

The Python starter handles synthetic events, environment expiry, illustrative meal-context inference, deterministic replay and denial of all pump actions. Its hand-selected likelihood ratios do **not** implement the specified joint Bayesian state estimator or virtual-sensor framework. Live acquisition, glucose predictive distributions, calibration, active acquisition planning and product clarification prompts remain to be built.

With Python 3.11 or later:

```sh
python3 -m unittest discover -s tests -v
python3 -m project_live.cli replay data/synthetic_example.jsonl
```

CI runs the baseline on Python 3.11 and 3.12. Tests need no medical devices or personal records.

## Repositories and contributions

- [Project LIVE](https://github.com/thebookoftheway3/project-live): public design, sensing, shadow evaluation and synthetic tests.
- [LoopWorkspace fork](https://github.com/thebookoftheway3/LoopWorkspace): upstream build workspace and pinned components.
- [Loop fork](https://github.com/thebookoftheway3/Loop): upstream application source for reviewed modifications.

Contributions in modelling, accessibility, human factors, sensor integration, testing and documentation are welcome. Discuss substantial changes in an issue and submit focused PRs with reproducible evidence. Share synthetic examples rather than personal health records. No signing or deployment workflows are enabled in the Loop forks during research setup.

## License and data

Original Project LIVE code and documentation are provided under the [MIT License](LICENSE). Separate upstream projects and assets retain their own licenses; see [third-party provenance](THIRD_PARTY_NOTICES.md).

Open source means shared software and methods. Health records, raw recordings, identifiers, credentials and signing material stay outside version control. The initial research runtime cannot command a pump.
