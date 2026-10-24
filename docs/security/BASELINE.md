# Repository security baseline and administrator actions

Snapshot: **24 October 2026**, repository `thebookoftheway3/project-live`, public `main` at `0a99fa78ed9d2a7c818f90933afc93a448375de5`. Scope: repository configuration and tracked source, not a penetration test, exhaustive history scan, clinical assessment or upstream audit. The GitHub connector verified repository identity and PR #2; authenticated, read-only `gh api` requests inspected administrative endpoints unavailable through that connector. No settings or privileges were changed.

## Verified observations

Endpoints below are relative to `GET /repos/thebookoftheway3/project-live/`. A successful empty response is distinguished from an inaccessible or error response. Settings can change after this snapshot.

| Area | Observed state and evidence |
| --- | --- |
| Identity/access | Repository metadata: public, MIT, personal-account owner `thebookoftheway3`. `collaborators?affiliation=all`: only that account, role `admin`. No independent maintainer verified. |
| Main protection | `branches/main/protection`: PRs required; strict/up-to-date required checks `Python 3.11` and `Python 3.12`, bound to GitHub Actions app ID 15368; conversation resolution required. |
| Review | Same endpoint: approving review count **0**; stale approvals dismissed; code-owner review **false**; latest-push approval **false**. PRs and tests are enforced, independent approval is not. |
| Admin/bypass | Administrator enforcement **true**; force pushes and deletion **false**. `rulesets`: empty. No bypass allowances were returned in branch protection; this does not fully inventory installed Apps, account tokens or their abilities. Administrators can still change settings. |
| Other branch controls | Required signatures and linear history **false**. These are observations, not changes requested automatically. |
| CODEOWNERS | Absent in audited main. This PR adds all-file coverage and explicit policy/workflow/boundary ownership for the only verified authorized account. The `codeowners/errors` endpoint returned 404 on main; no remote validation of the new file is claimed by that response. |
| Actions policy | `actions/permissions`: enabled, allowed Actions `all`, SHA pinning enforcement **false**. |
| Token defaults | `actions/permissions/workflow`: default **read**, Actions may approve PRs **false**. Existing workflow explicitly uses `contents: read` and checkout `persist-credentials: false`. |
| Fork execution | `actions/permissions/fork-pr-contributor-approval`: **first_time_contributors**. Existing workflow uses `push` / `pull_request`, not `pull_request_target`, and has no secret references or privileged follow-up workflow. Policy for repeat external contributors is therefore less restrictive than approval for all outside collaborators. No hostile-fork execution test was performed. |
| Actions source | `.github/workflows/shadow-tests.yml`: checkout pinned to `11d5960a326750d5838078e36cf38b85af677262`; setup-python to `a26af69be951a213d495a4c3e4e4022e16d87065`; hosted `ubuntu-latest`, ten-minute timeout, Python 3.11/3.12 checks. These pins do not establish that every transitive tool or runner image is immutable. |
| Dependency security | `vulnerability-alerts`: 404 explicitly says disabled; `dependabot/alerts`: 403 explicitly says alerts disabled. Repository metadata reports Dependabot security updates **disabled**. No Dependabot configuration in main. This PR proposes weekly GitHub Actions version-update PRs; it does not enable alerts/security updates or auto-merge. |
| Python dependencies/upstream | `pyproject.toml` declares no runtime dependencies; inspected runtime imports are standard-library/local. CI does not install the package. Loop code is not vendored; `THIRD_PARTY_NOTICES.md` and `docs/UPSTREAM_BASELINE.json` retain upstream notices and revisions. Component licences and reproducible upstream builds still need review. |
| Code scanning | `code-scanning/default-setup`: **not-configured**, listed languages `actions`, `python`. `code-scanning/analyses?per_page=1`: 404, “no analysis found.” No code-scanning workflow is tracked. This is no verified analysis evidence, not a clean scan. |
| Secret scanning | Repository metadata reports secret scanning, push protection, non-provider patterns and validity checks **disabled**. Secret-alert endpoint also reports scanning disabled. No claim of no historical secrets follows. |
| Private reporting | `private-vulnerability-reporting`: **enabled: false**. SECURITY.md describes a temporary non-sensitive channel request, not a working private inbox. |
| Release/deployment credentials | `actions/secrets`, `actions/variables`, `environments`, `keys`, `actions/runners`, `hooks` all returned empty inventories. `releases` returned none. No release/deploy workflow is tracked. These results do not inspect personal credentials, GitHub App credentials, local stores or external systems. |
| Public data/privacy | Tracked-file inventory contains source, documentation and a synthetic JSONL fixture; `.gitignore` excludes local originals, records, media and secrets. `NoPumpAccess` denies all commands; tests exercise synthetic-only input and denial. Inspection is not an exhaustive PII/secret scan and does not cover all public comments, logs, artifacts, forks or upstream repositories. |

The CLI appended generic scope advice to some error responses. No additional scopes were requested. Explicit server messages and independently returned configuration support the disabled findings; a bare 403/404 alone would be **unverified**, not disabled.

## What remains unverified

- Account 2FA/passkey/recovery settings, PAT/SSH-key inventory, authorized OAuth/GitHub Apps, their effective access and any external bot credentials.
- Absence of secrets or identifiable information across all history, other branches, comments, logs, artifacts and forks; absence of vulnerabilities in dependencies or Actions.
- Whether a private report can be successfully received and triaged (reporting is currently disabled); notification delivery and incident response coverage.
- Reproducible release builds, signing/provenance, external deployment infrastructure and complete upstream licence compliance.
- Independent review capacity. One owner's multiple accounts, bots and model reviews do not establish independence.

## Administrator action checklist

**Recommendations only; require explicit administrator authorization. Do not weaken existing protections.** UI labels can vary; use the named control and re-read the API to verify the resulting state. See GitHub's [private reporting configuration](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository), [Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) and [Actions permissions API](https://docs.github.com/en/rest/actions/permissions). Security settings live under Settings → Security and quality → Advanced Security in current GitHub documentation; older layouts may call this Code security and analysis.

| Priority / UI location | Current → desired action and verification |
| --- | --- |
| First: Settings → Advanced Security → Private vulnerability reporting | Disabled → enable; subscribe responsible maintainer to security notifications. Confirm endpoint `enabled: true` and the Report a vulnerability entry point. Agree a private receipt test; then update SECURITY.md and this dated finding. No private address should be invented. |
| First: Advanced Security → Secret Protection / secret scanning and push protection | Disabled → enable available secret scanning and push protection; inspect findings privately and verify metadata. Consider non-provider patterns and validity checks only after reviewing availability and data handling. Do not publish alert payloads. |
| First: Advanced Security → Dependency graph / Dependabot | Alerts and security updates disabled → verify dependency graph availability, enable alerts and security updates; confirm endpoints/metadata. Review the proposed Actions version-update configuration separately; all generated PRs still need review. |
| First: Settings → Actions → General → Fork pull request workflows | `first_time_contributors` → require approval for **all outside collaborators**. Verify `approval_policy: all_external_contributors`. Retain read-only tokens and no PR-approval permission. Inspect workflow/code before authorizing any run. |
| Next: Advanced Security → Code scanning → CodeQL default setup | Not configured / no analyses → review available Actions/Python default setup and required permissions, enable if suitable, confirm an actual completed analysis and triage results. Do not describe “enabled” as “secure.” |
| Next: Settings → Actions → General → Actions permissions | All Actions allowed, SHA enforcement false → restrict to GitHub-authored and explicitly reviewed Actions and require full commit SHAs where available. Preserve the current checkout/setup-python pins and required check names; verify a branch run still succeeds. |
| Preserve now; strengthen with staffing: Settings → Branches → main rule | Preserve strict `Python 3.11`/`Python 3.12` checks, stale-review dismissal, resolved conversations, admin enforcement, no force pushes/deletion. Once a willing independent maintainer with review rights is established, require at least one independent approval, code-owner approval and approval of the latest push. Verify settings and CODEOWNERS coverage together. With only the author as owner, switching this on would not create independence and can block merges. Do not substitute routine admin bypass. |
| Next: Settings → Collaborators, Rules/Branches, Integrations; account security settings | One admin, no rulesets and incomplete credential/App inventory → review authorized Apps, bot tokens, SSH/PAT access, bypasses, recovery and 2FA with the owner. Record minimal permissions and responsible people without exposing secrets. No permission changes in this PR. |
| Before any release: Settings → Environments / Secrets and variables / Deploy keys | Empty repository inventories and no release workflow → retain until a separate release design is approved. Require reproducible build inputs, provenance, scoped short-lived credentials where supported, protected release approval and recovery/rotation steps before adding them. |
| Ongoing: repository history and contribution review | Limited tracked-source inspection → arrange a scoped secret/privacy history audit and upstream licence/provenance review; handle findings privately. Recheck controls after security, access or workflow changes. |

## Review gap and future audits

CODEOWNERS routes responsibility; it neither grants permissions nor enforces review on its own. This PR's owner cannot approve their own PR. Recruit a willing independent maintainer using the public nomination process, record accepted scope and authorization, grant minimal permissions explicitly, update CODEOWNERS and then enable approval enforcement without bypassing it. Until then, keep the gap visible and defer privilege expansion as specified in GOVERNANCE.md.

Use [OpenSSF Scorecard](https://scorecard.dev/) for a later measured configuration audit and [OpenSSF Best Practices criteria](https://www.bestpractices.dev/en/criteria/0) for a documented project-practice review. Neither was run or awarded here. Record tool version, commit, timestamp, actual check results and limitations before claiming a score or badge. Follow [GitHub's workflow security guidance](https://docs.github.com/en/actions/reference/security/secure-use); do not add a credentialed audit workflow incidentally.

## Reproduction and validation

Read-only checks use `gh api repos/thebookoftheway3/project-live/<endpoint>` for the endpoints above. Do not paste credentials or sensitive alert responses into public evidence. Repository snapshot and recommendations are separate from local check results in [VALIDATION.md](VALIDATION.md). No administrative PUT/PATCH/POST/DELETE was performed for this audit.

## Integration follow-up — 24 October 2026

After governance integration, main contains CODEOWNERS and the weekly Actions version-update configuration. `codeowners/errors` returned an empty errors list; this verifies syntax, not independent review. Dependabot has generated Actions update branches; they require separate review and are outside the #3/#4/#2/#5 integration. These version updates do not enable vulnerability alerts or security updates. Rechecked private reporting remains disabled, secret scanning/push protection and Dependabot security updates remain disabled, CodeQL default setup is not configured, all Actions remain allowed without enforced SHA pins, and fork approval remains `first_time_contributors`. Read-only default tokens, disabled Actions PR approvals and the sole verified administrator are unchanged. No administrator setting was modified. Original snapshot findings and unverified account/App controls above remain dated evidence.
