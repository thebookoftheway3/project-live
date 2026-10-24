# Project LIVE governance

Project LIVE exists to return human life, attention and capability through better systems. It creates reusable knowledge and software for humanity, beginning with diabetes. No contributor, company, model, maintainer or existing architecture is immune to correction.

## Current authority and roles

This is initially a maintainer-led project. The repository is owned by the personal GitHub account **[@thebookoftheway3](https://github.com/thebookoftheway3)**, the sole verified administrator and current maintainer. That account currently handles security coordination and release decisions as well. No committee, additional maintainer or independent security team is established. See the dated [security baseline](docs/security/BASELINE.md) for verified access and enforcement.

| Role | Responsibility and authority |
| --- | --- |
| Contributor | Submit observations, questions, research, code and corrections; no write permission is implied. |
| Reviewer | Examine evidence and changes, disclose conflicts and recommend an outcome; review alone does not grant merge rights. |
| Maintainer | Steward agreed scope, resolve routine proposals, review and merge eligible PRs, and record decisions. |
| Security maintainer | Handle confidential reports, coordinate fixes and disclosure; access is limited to what the role needs. Currently performed by the sole maintainer. |
| Repository administrator | Manage access, protections, integrations and repository ownership. Administrative capability does not make a technical claim correct. |

One person may hold several roles, but these responsibilities remain distinct. GitHub permissions are recorded separately from social roles. Agents may assist; they do not vote, confer authority or count as independent human reviewers.

## Proposals and decisions

Use public issues for observations and proposals and focused PRs for reviewable changes, following [CONTRIBUTING.md](CONTRIBUTING.md). People may challenge assumptions in their own terms without adopting our model or writing code. Security disclosures and personal information follow [SECURITY.md](SECURITY.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), not public technical debate.

Routine changes may be accepted by a maintainer after applicable checks, scope review, attribution review and resolution of material feedback. Explain rejected changes respectfully. The current zero-approval configuration is a disclosed single-maintainer limitation, not evidence of independent review. Authors must not represent self-review or agent review as an independent approval. No automatic merging is authorized by this policy.

For consequential architecture, use a numbered [ADR](docs/decisions/README.md): state evidence, competing alternatives, dissent, tradeoffs and criteria that would reopen the decision. Seek relevant reviewers and normally allow at least seven calendar days for discussion. The maintainer currently makes the final decision and publishes its rationale. Lack of comments is not consensus. Unresolved safety or privacy concerns block implementation until explicitly resolved with evidence; unsupported confidence is not a resolution. A rejected proposal can be reopened with new evidence. Preserve prior decisions and negative results.

Security-boundary, governance, permissions and release-authority changes need explicit review of their threat model, affected authority, recovery and rollback. Seek a qualified independent human reviewer; where none exists, record that gap publicly and defer privilege expansion or relaxation of security boundaries. Policy documentation and improvements that preserve the existing boundary may proceed through the normal PR process with the limitation disclosed. Urgent containment may be performed by an authorized administrator, recorded privately as necessary and followed by a redacted public explanation and later review. This does not authorize agents to change settings or merge.

## Maintainer lifecycle and continuity

Anyone may nominate a willing contributor, including themselves, in a public governance issue. Describe sustained contributions, review judgement, collaboration, security awareness, proposed scope, affiliations and conflicts. Allow at least fourteen calendar days for feedback. The current maintainer records the decision and the nominee's explicit acceptance; an administrator then grants only the permissions needed in a separately authorized action. Update this roster and CODEOWNERS through a PR. Review or triage responsibility should normally precede write access. Donations and volume of commits do not qualify someone automatically.

Maintainers may step down. Inactivity, misuse of permissions, repeated misconduct or inability to meet responsibilities can justify removal. Document concerns, provide an opportunity to respond and seek review by uninvolved maintainers where available. Publish the decision and effective permission changes while protecting private reports. Administrators may suspend access promptly for an active compromise, then review the action. Appeals go to an uninvolved maintainer when one exists. Today no independent appeal body exists, and a personal-account owner cannot be removed by a document; this is a material governance limitation.

As participation grows, recruit at least two independent maintainers with different affiliations where possible, establish an additional security contact and a second trained administrator, and test handover and recovery. Review roles and access at least every six months and after departures or incidents. Preserve public history, attribution and build instructions; establish reproducible release builds and recovery documentation before distributing releases. A future organization may improve continuity but requires the [separate transition review](docs/governance/ORGANIZATION_OPTIONS.md).

## Conflicts, sponsorship and project capture

Maintainers and reviewers disclose relevant employment, financial interests, sponsorship, vendor relationships and other conflicts on affected decisions. Recuse from deciding their own material conflicts and seek an unconflicted reviewer. If the only maintainer is conflicted, record the limitation and defer the consequential decision until appropriate review is available. Do not publish unnecessary personal information.

Disclose accepted project sponsorship, its recipient, purpose and material conditions in a public governance record before accepting terms that affect project work. No financial contribution automatically grants technical privileges, roadmap control, release rights or validation endorsements. No sponsorship roster is asserted by this document; affiliations and funding are not independently audited by the security snapshot.

| Concept | What it means |
| --- | --- |
| Open-source licensing | MIT permits reuse, modification, forks and commercial use subject to its terms; this governance policy adds no restrictions to those rights. |
| Repository ownership | Control of this GitHub repository and its permissions; distinct from contributors' retained copyright. |
| Maintainer authority | Stewardship under this process, open to challenge and correction. |
| Technical decisions | Evidence-based choices recorded in public ADRs, not ownership or financial entitlement. |
| Release authority | Explicit approval of an identified artifact and release process; not granted by ordinary contribution or sponsorship. |
| Clinical validation claims | Require evidence specific to population, intended use, version and evaluation. Neither MIT, a merge, sponsorship nor passing synthetic tests establishes clinical validation. |

Original contributions remain under MIT without copyright assignment or a contributor licence agreement. The current inbound MIT policy is sufficient for the present original-code/documentation scope; imported work requires separate provenance and licence review. Any proposed change needs a public, explicitly reviewed governance decision. This policy cannot prevent forks or commercial reuse allowed by MIT.

## Changing this model

Propose significant governance changes in an issue and focused PR with motivation, alternatives, effects on rights and authority, conflicts, transition and reversal plan. Allow at least fourteen calendar days for public feedback and request independent review; record who actually reviewed and decided. Changes to ownership, security or release authority require explicit administrator authorization as well as this review. Confidential incident details stay private; publish redacted outcomes and reasons. Revisit the model as the community grows rather than inventing inactive committees.
