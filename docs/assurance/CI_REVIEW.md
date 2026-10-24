# CI and software-assurance gap review

Reviewed 24 October 2026 against fetched public main **22f01c0edf1d156d798b825c18bdf204e9490b49**, after PRs #2–#5. Scope: the synthetic Python starter and its verification pipeline. This is a research-stage engineering assessment, not certification, a complete standards assessment, a safety case or clinical validation. No release, device, live sensing or treatment capability is introduced.

Basis: [security baseline](../security/BASELINE.md), [methodology](../METHODOLOGY.md), accepted ADRs [0001](../decisions/0001-modular-monolith-first.md), [0002](../decisions/0002-lightweight-assurance-traceability.md) and [0003](../decisions/0003-observation-payload-snapshots.md), [requirements](../requirements/LEDGER.md) R01/R06/R07/R10/R12/R19/R20, LIVE-001/LIVE-016 in the [backlog](../BACKLOG.md), and the [claim matrix](CLAIMS_MATRIX.md). The architecture's future virtual-sensor contracts remain proposed APIs. This PR verifies existing boundaries; it does not accept new ones.

## Observed practices and focused changes

| Area | Evidence on reviewed main | Change and remaining gap |
| --- | --- | --- |
| Baseline CI | Required `Python 3.11` and `Python 3.12` jobs run 15 unittests and synthetic replay. No release/deploy jobs. | Keep names and both versions; add gates inside these already-required jobs. `requires-python >=3.11` is a package minimum, not evidence for every newer interpreter. |
| Static checks | No lint, formatting or type-check gate. | Ruff checks syntax/name/import issues, import ordering and explicit exec/eval rules; formatter enforced. Existing runtime edits are formatting/import ordering only. Full type checking and broad security analysis remain absent. |
| Dependencies | No runtime third-party dependencies; Actions Dependabot updates already configured. No Python audit. | Hash-locked, wheel-only development tools; pip-audit of all locked transitive packages; weekly pip updates. Runtime dependency additions fail the architecture test until capability/audit scope is reviewed. A clean audit covers known advisories only; it is not a malicious-package detector. |
| Actions | Existing full SHA pins, `contents: read`, hosted runners, timeout and non-persistent checkout. | Offline zizmor with strict collection and auditor findings. No new Actions or credentials. Pinning does not audit upstream source, transitive downloads or the hosted runner image. |
| Architecture | Documented non-actuation and modular monolith; no mechanical import boundary. | An explicit AST import inventory for all seven runtime modules rejects reversed edges, new modules, transport imports and direct dynamic-execution names. Current evidence/context/environment modules cannot depend on replay/CLI; the denial module has no transport dependency. This detects static violations, not reflection, arbitrary native code or a malicious change to both code and checks. |
| Forbidden paths | Tests already deny four actions in four environments and reject nonsynthetic parsing. | Add unknown/override commands, rejected command event kinds and inert command-like payloads during verified-home/high-confidence inference. An observer positive control precedes the no-execute assertion. Arbitrary host isolation and user interpretation remain unverified. |
| Traceability/docs | Nine C/H/S/V rows, E01–E04, accepted ADR register, prior one-off documentation checks. | Tests enforce unique/retained IDs, populated rows, requirement references, evidence resolution/reverse links and ADR status consistency. rumdl checks local paths, fragments and reference links; PyYAML parses configs/templates. No semantic proof, external URL availability check or automatic claim promotion. |
| Evidence reporting | Console test results; no measured coverage or explicit CI gap report. `git diff --check` on a clean checkout inspected no committed diff. | Step outcomes, branch/missing-line coverage and recorded claim limitations appear in each job summary; missing/skipped results stay visible. Whitespace check compares the actual base/push revision. Logs and summary are tied to the workflow SHA and Python version. |

The implementation deliberately uses maintained tools for generic checks. Import-linter would model local layering, but would still need a separate capability inventory for this seven-file, standard-library-only starter. A short AST unittest expresses both existing constraints without a framework. Markdown remains the source of claim status; a second compliance database or percentage-of-claims score would add maintenance and false confidence. Coverage is reported without a numeric pass threshold: new assertions and mutation detection are more useful than padding line execution.

## OpenSSF and OWASP comparison

The [OpenSSF concise development guide](https://best.openssf.org/Concise-Guide-for-Developing-More-Secure-Software) recommends complementary automated checks, negative testing, dependency scrutiny, vulnerability monitoring and enforced review. LIVE already has bounded tests and pinned Actions; this PR adds missing checks and their negative controls. The remaining material gaps are private vulnerability intake, secret detection, dependency alerts and independent review enforcement. Release signing, provenance and an SBOM need an authorized release design when distributable artifacts exist. No Scorecard score or Best Practices badge assessment was performed.

The [OWASP CI/CD Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html) emphasizes pipeline trust boundaries, minimal privilege, dependency integrity and useful logging. The PR preserves hosted, disposable PR jobs, read-only tokens, no secrets, non-persistent checkout and no privileged downstream workflow. Tools install pinned wheels with hashes; pip-audit queries package/version advisory metadata only. Logs use synthetic fixtures. Pull requests can change their own tests and workflows: CI is evidence for review, not an independent security boundary. Enforced independent review of those files is still missing.

## Proportionate use of medical-software standards

These are engineering recommendations inferred from the standards' publicly available scope descriptions, not a clause-by-clause evaluation of licensed normative texts. No software safety class, regulatory status, acceptable clinical residual risk or conformance level is assigned.

| Reference | Useful discipline now | Escalation before broader exposure; not supplied by this PR |
| --- | --- | --- |
| [IEC 62304:2006 + AMD1:2015](https://webstore.iec.ch/en/publication/22794), software lifecycle processes | Maintain bounded requirements, architecture, configuration/version records, change impact, anomaly records and reproducible unit/integration verification. Existing ADRs and C/H/S/V records are a proportionate starting point. | Qualified review of intended use, software classification, maintenance/release processes and third-party software evaluation before a medical-software program. CI success does not validate a final device. |
| [ISO 14971:2019](https://www.iso.org/standard/72704.html), risk management | Extend affected hazards with trigger, hazardous situation, potential harm, control and verification argument. Preserve counterexamples and new risks introduced by controls. C-01 tests cover command denial only. | Risk estimation/acceptability criteria, residual-risk evaluation and lifecycle feedback require appropriate expertise and intended-use evidence. Do not invent clinical probabilities from synthetic test counts. The matrix is not a completed risk-management file. |
| [IEC 62366-1:2015 + AMD1:2020](https://webstore.iec.ch/en/publication/67220), safety-related usability | Identify intended users/tasks/environments and foreseeable misunderstanding of research output, especially `review_possible_meal`. Record assumptions and formative comprehension questions; make CI's missing evidence legible to contributors. | Before human-visible advice/studies, evaluate use-related hazards, accessibility, interruptions, recovery and comprehension with relevant users and qualified oversight. No usability study or summative validation was performed; non-actuation does not remove behavioural influence. |
| [IEC 81001-5-1:2021](https://webstore.iec.ch/en/publication/63293), secure health-software lifecycle | Maintain threat boundaries, least privilege, dependency inventory/update process, security verification and vulnerability handling. The administrator checklist addresses observed configuration gaps. | Before providers, personal data, untrusted workers or deployment, establish security requirements/threat analysis, enforced capabilities, fault/abuse testing, incident response and independent review. Neither an offline workflow scan nor a pin establishes end-to-end cybersecurity. |

## Operating and reviewing the gates

On each supported version (3.11 and 3.12), use an isolated environment without personal credentials:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes --only-binary=:all: -r requirements/ci.txt
ruff check project_live tests tools
ruff format --check project_live tests tools
zizmor --offline --no-progress --strict-collection --persona auditor .github
rumdl check .
python tools/check_templates.py
python -m coverage run -m unittest discover -s tests -v
python -m coverage run --append -m project_live.cli replay data/synthetic_example.jsonl
python -m coverage report
python tools/check_negative_controls.py
python -m pip_audit --no-deps --disable-pip -r requirements/ci.txt --format json -o audit.json
python tools/check_negative_controls.py --audit-only
git diff --check
git diff --check origin/main HEAD
```

The ordinary unittest command still requires only Python's standard library. The extra verification tools are development dependencies, not imported by the research runtime. Audit failures or unavailable advisory services fail the job rather than being described as clean. zizmor is offline: online advisory/SHA-origin audits are not performed. No external scanning service, token, paid service or artifact upload is added.

Update tools intentionally: edit `requirements/ci.in`, regenerate `ci.txt` with `pip-compile --generate-hashes --allow-unsafe --strip-extras --output-file requirements/ci.txt requirements/ci.in` (pip-tools 7.6.2 used here), review all transitive changes/hashes and rerun both Python jobs. Hashes bind package bytes, not trustworthiness. Review lock refreshes and upstream provenance; dependency updates do not auto-merge. A compromised PR can alter its own gate; repository protection and independent review remain separate controls.

Both Dependabot ecosystems use a seven-day version-update cooldown, flagged by the expanded zizmor audit. GitHub documents that [cooldowns do not delay security updates](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#cooldown); enabling those updates remains an administrator action. `python tools/ci_summary.py --check-audit` additionally rejects skipped or missing packages in the advisory report, rather than treating incomplete coverage as clean.

See [executed results and limits](CI_VALIDATION.md) and the separate [administrator checklist](../security/CI_ADMIN_CHECKLIST.md). No settings change is included. Revisit this review when dependencies, imports, permissions, exposure, workflows or claim scope change. No independent human assurance review was available.
