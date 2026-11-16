# ADR 0004: Work-package research monorepo

- Status: Proposed
- Date: 2026-11-16
- Authority: owner-requested implementation on a review branch; acceptance awaits review/merge.
- Review: Codex-assisted; no independent human reviewer or clinical reviewer.
- References: R01/R03/R07/R08/R12/R14/R20/R26/R27; LIVE-014/016/019/021.
- Preserves: ADRs 0001–0003 and the non-actuating boundary.

## Problem and alternatives

Follow-up direction: Surfer OS is the product inspiration within Project LIVE;
its supplied specification is older and more comprehensive, not the governing
implementation contract. [The updated product design](../SURFER_OS.md) reconciles
it with the newer WP refactor. The source document is preserved unchanged.

Grant reviewers need identifiable deliverables, falsifiable KPIs and reproducible
verification. The supplied v2 specification mixes requested research with claims
of proven benefit, hardware interoperability, clinical protection and licensing
authority for which this repository has no evidence.

| Alternative | Benefit | Cost and decision |
| --- | --- | --- |
| Keep current layout | No migration | Does not expose WP ownership; rejected for this owner-requested refactor |
| WP directories with offline models and explicit integration contracts | Preserves the working core and isolates experimental dependencies | Selected for the review branch; models are not deployed hardware |
| Immediately connect pump, cameras, voice provider and cloud | Could test integration | Requires device protocol, consent, isolation, clinical and operational evidence absent here; deferred |

## Implementation boundary

Move the unchanged `project_live` package under WP2 using `git mv`. A root relative
symlink preserves checkout CLI compatibility; setuptools discovers the physical
source directory for installed packages. Shared tests and synthetic fixtures stay
at root. New WP tests are discovered from the root suite as well.

WP1 contains host-executable C++ **simulation** models. A pure transition function
takes explicit state; the watchdog and lockout necessarily retain timing history.
The 30-minute, 15-minute and 55%/180-minute values are owner-specified experimental
parameters, not validated clinical limits. A missing budget history inhibits the
experiment. No model has a pump driver, radio command encoder or device credential.
No assertion here proves an independent hardware interlock cannot be bypassed.

WP2 keeps the existing inference/Loop consumer unchanged. Detector health and EVSI
are separate pure research modules. A separately installed FastAPI service accepts
synthetic manual clearance and voice-callback events only. It cannot read private
Loop files or forward events to treatment. MQTT and Ollama are optional isolated
local services, not prerequisites for the core. FastAPI is justified by the
requested typed HTTP contract; Mosquitto/Ollama remain integration scaffolding.

WP3 contains local numerical/privacy experiments with injected model outputs.
SAM 2, Depth Anything V2, Re-ID and VLM models are not downloaded or represented as
integrated. Metric calibration is required before reporting cubic centimetres.
WP4 contains passive client source scaffolds; no signing or distribution occurs.

The API uses loopback binding, bearer authentication, bounded schemas, a single
worker, no outbound callbacks and synthetic inputs. Restart discards session state;
it is not a durable override service. Neither API nor network containers mount
private telemetry, cameras, radios or host credentials. Compose is a development
profile, not a verified VPS production deployment.

## Licensing and claims

Existing MIT grants and notices remain intact. New files explicitly marked
AGPL-3.0-only use that licence. A separate commercial agreement is an option only
where the relevant rights holders can grant it. No company identity, exclusive IP
ownership, grant award, regulatory exemption or clinical validation is asserted.
See [licensing scope](../../LICENSE-COMMERCIAL.md) and
[verification plan](../GRANT_VERIFICATION_PLAN.md).

## Verification, rollback and reopening

Preserve all 61 baseline tests and 21 negative controls. Test exact watchdog,
lockout and rolling-budget boundaries; clock regression; invalid numerics;
prompt cooldown/budget/consent; API authentication and replay; metric calibration;
and export-schema rejection. Keep lint/security checks and their required job names.
Record actual results in [verification evidence](../assurance/WP_REFACTOR_VALIDATION.md).

Rollback is a revert of the focused refactor commits; baseline tag
`v1.0-shadow-baseline` preserves the merged starting point. Reopen before any
device transport, real-data API, external voice call, permanent identity tracking,
clinical evaluation, production deployment or broader relicensing. The supplied
document is evidence of a proposal, not authority to change repository metadata
or conceal medical intended use.
