# Setup evidence — 24 October 2026

## Public foundation

The project direction is public open-source research for people with diabetes. Revision 2 is the governing specification. Original source documents and the earlier private bootstrap are preserved separately; the public repository begins with a clean history without participant device details.

- Public project address: `thebookoftheway3/project-live`.
- Public upstream forks: `thebookoftheway3/LoopWorkspace` and `thebookoftheway3/Loop`.
- Loop forks have unchanged `research/project-live` branches at the pinned research baseline. Their GitHub Actions remain disabled; no signing or deployment credentials were added.
- LoopWorkspace `v3.14.9`: `548b33245198eaae165c094c9c68fe333cb69c05`.
- Full recursive checkout completed: 21 top-level component revisions and one nested dependency recorded in `UPSTREAM_BASELINE.json`.
- Project LIVE's implementation remains the synthetic Python starter. Updating the specification does not implement the Bayesian state estimator.

## Established validation

- Seven baseline unit tests passed locally on Python 3.12.14.
- Synthetic replay produced six records, all with pump authorization denied.
- Public root commit `99199a173fddb2b84fd9e25833c538a9d12eec63` passed CI on Python 3.11 and 3.12: https://github.com/thebookoftheway3/project-live/actions/runs/40099087438 .
- Xcode 26.4.1 (17E202) and Swift 6.3.1 were detected. A successful simulator build is still pending.
- Python 3.11 or later is required. Contributors should select an appropriate runtime rather than assuming the system Python meets the requirement.

## Repository controls verified

- Repository is public and GitHub detects the MIT license.
- Main requires pull requests and passing `Python 3.11` and `Python 3.12` checks against an up-to-date branch.
- Protection applies to administrators; force pushes and branch deletion are disabled. Conversations must be resolved.
- Independent approval count is currently zero. This enforces PRs and CI, not independent human review; establish reviewer ownership as contributors join.
- The original private bootstrap is archived and remains private. Public main has no ancestors from that history.

## Remaining evidence
- Establish an unmodified Loop simulator build/test baseline.
- Review individual upstream component licenses before redistribution or changes.
- Live sensor acquisition, glucose forecasting, Bayesian filtering, active acquisition and product prompting are not yet implemented.

Tests establish only the exercised software behavior, not clinical performance or counterfactual treatment safety.
