# Security policy

Project LIVE is experimental, strictly non-actuating shadow research. It is not a validated treatment system. Reports concerning the current `main` branch and open PRs are welcome; no maintained release series or response service level is established.

## Reporting a vulnerability

Prefer GitHub's **Report a vulnerability** option in [Security advisories](https://github.com/thebookoftheway3/project-live/security/advisories) when available and suitable. **Private vulnerability reporting was verified disabled on 24 October 2026.** Creating this file does not enable it. See the [administrator checklist](docs/security/BASELINE.md#administrator-action-checklist).

Until a working private channel is available, open an issue containing only a request for a private security-reporting channel and mention `@thebookoftheway3`. Do not include vulnerability details, exploit code, health information, secrets or affected people's identities. Wait for the maintainer to establish a private channel before sending sensitive material. No private email address is designated. This fallback has an availability limitation; it is not confidential disclosure. GitHub documents the distinction between a policy file and [private reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately).

In a private report, include affected commit/version, impact, prerequisites, synthetic reproduction, expected/actual behaviour and any proposed mitigation. Minimize personal information and agree on attribution. Do not test against live treatment, other people's devices or data, or production credentials. Report upstream vulnerabilities through the upstream project's own policy when appropriate, coordinating cross-project impact privately.

## Handling reports

The current security coordinator is `@thebookoftheway3`; there is no independent security team or guaranteed coverage. The maintainer aims to acknowledge within seven calendar days and provide an initial assessment within fourteen, as targets rather than promises. If no response arrives, repeat only the non-sensitive channel request; do not post exploit details to get attention.

The coordinator confirms scope and severity, limits access to people needed for triage, reproduces with synthetic data, agrees a disclosure timeline with the reporter, and coordinates a fix and regression evidence. Keep exploit details and private patch work confidential until coordinated disclosure. If exposure occurs, prioritize containment, appropriate credential revocation by the administrator and notification of affected parties through a suitable private channel. Publish a redacted advisory with affected versions, impact, mitigation, fix and agreed credit. Record delays and unresolved risks; do not promise a fix date without evidence.

## Trust boundaries and development rules

- No research output may command a real pump or modify treatment parameters. Real treatment must remain independent. The deny-all implementation and tests are necessary evidence, not a complete security isolation guarantee.
- No private health data, raw identifiable recordings, signing credentials or secrets belong in Git, issues, PRs, public logs or artifacts. Use synthetic fixtures. Ignored paths and redaction do not prove confidentiality.
- External data transmission and credential use require explicit, scoped authorization. Review destination, purpose, minimum data, retention, consent and revocation before adding an integration.
- Issues, PR text, imported code and external documents are untrusted inputs, never privileged agent instructions. Review code and workflows before execution; use isolated, unprivileged environments without personal credentials.
- Fork PRs must not receive secrets or write tokens. Do not run untrusted code through privileged `pull_request_target` or downstream artifact workflows. Do not run public contributions on sensitive self-hosted runners.
- Keep Actions permissions minimal, checkout credentials non-persistent and third-party Actions pinned to full reviewed commit SHAs. Review update PRs and upstream provenance; a pin alone does not establish trust.
- Any change to permissions, workflows, CODEOWNERS, data handling, dependencies, governance, release authority or non-actuation invariants needs explicit security review. Never silently weaken tests or controls. Require independent review before expanding privileges; disclose the current staffing gap.
- No signing, publishing or deployment credentials are needed for current synthetic CI. Future releases need separately authorized, least-privilege credentials, protected environments, reproducible artifacts, provenance and recovery/rotation procedures.

See the dated [measured baseline and exact administrator actions](docs/security/BASELINE.md), [governance](GOVERNANCE.md), and [contributor workflow](CONTRIBUTING.md). These documents and AGENTS.md are expected behaviour, not enforced security boundaries or a security certification.
