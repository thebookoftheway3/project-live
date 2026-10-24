> Imported source inventory. Its original verification labels are unverified source assertions until independently checked for this project.

# Source inventory — inherited research leads, 24 October 2026

This is a retrieval/indexing ledger, not an endorsement of clinical claims. Clinic handouts may contain earlier internal dates and may be changed in place; retain both index modified date and document-internal date when inspecting. The project's own code stays separate from upstream licensed work.

## BCDiabetes handouts

| Document | Index last modified | Stable handout link | Research use | State |
| --- | --- | --- | --- | --- |
| Handouts index | live | https://www.bcdiabetes.ca/handouts/ | Master catalogue | Indexed |
| Looping at BCDiabetes | 2026-08-21 | https://www.bcdiabetes.ca/handouts/?file=1JDlk6fCqUXsIZiHFL4SY3rM3QkZGqahSIj8JadgJzPg | Clinical service, installs, workflow, follow-up | Initial text and page inspection |
| Looping with Omnipod 5 pods | 2026-08-29 | https://www.bcdiabetes.ca/handouts/?file=1CUXvBqt7gqWwEat1xZbOXN73NL0Z06SX2XLIsCU6v6s | Integration context | Initial text and page inspection; handout describes June status before official release |
| Omnipod 5 vs Loop | 2026-06-26 | https://www.bcdiabetes.ca/handouts/?file=1cv5l-4cEOBBHsym48VEvG98hVbrIOMG_SGeQ2wsMxg8 | Architecture comparison | Indexed; full review pending |
| Loop Affiliate Program | 2026-02-02 | https://www.bcdiabetes.ca/handouts/?file=1-47-2mnS2_eqGWdqY7T-LdhIYkly2fESzZPc5DMMYgM | Shared expertise/clinical support | Initial page inspection |
| Additional Loop Resources | 2025-10-05 | https://www.bcdiabetes.ca/handouts/?file=1mwAXwL-k6LIwQhKzOIZtozmG2YAzMU_F1vJniVbXAwY | Further training and support | Indexed |
| Looping in hospital | 2026-07-13 | https://www.bcdiabetes.ca/handouts/?file=1B0-rPxsUAfiqq0kC-fqYk5JZ6sX4atBKANrpcGBY0BE | Continuity / backup | Indexed |
| Looping in hospital letter | 2026-07-13 | https://www.bcdiabetes.ca/handouts/?file=1SAX0cdAo0e-58jYu7Aqsestqh9QgUu63Ie7sJEY-7uk | Clinical service continuity | Indexed |
| FINESSE — undeclared meals | 2026-06-25 | https://www.bcdiabetes.ca/handouts/?file=1Cf29lIHM0fyljxxl2hlmiPRE4GF3NB-nrgNZki7wQ5A | Meal model research | Indexed |
| Setting Expectations with AID | 2026-01-16 | https://www.bcdiabetes.ca/handouts/?file=1DIA5pceVN4iOU254uRrXO2ZEsbGIHJaAQ6vy3ibPKLg | Human factors / limitations | Indexed |
| Omnipod faults / 203 fault | 2026-08-23 | https://www.bcdiabetes.ca/handouts/?file=1xXvbhzxNAk_ogELsTBdqMTCKX6HdOSv0PktYmVhRUR4 | Device failures | Indexed, full review pending |

Other handouts in index to examine later: adult consent and waiver, Loop safety/emergency, OLIVER trial, Loop presets, children at school, DASH training, AID options, BCDiabetes clinical outcome reports. Links to each can be resolved from the main index as needed.

## Upstream code and documentation

- LoopWorkspace releases: https://github.com/LoopKit/LoopWorkspace/releases . v3.14.9 released 2026-10-05; v3.14.7 introduced Omnipod 5 support on 2026-09-15. **Pin exact tag/commit in Mac checkout**.
- Loop application: https://github.com/LoopKit/Loop
- LoopKit: https://github.com/LoopKit/LoopKit
- OmnipodKit integration: https://github.com/LoopKit/OmnipodKit
- LoopDocs current: https://loopkit.github.io/loopdocs/
- LoopDocs CGM compatibility: https://loopkit.github.io/loopdocs/build/cgm/
- LoopDocs add CGM: https://loopkit.github.io/loopdocs/loop-3/add-cgm/
- LoopDocs simulator: https://loopkit.github.io/loopdocs/version/simulator/
- LoopDocs Omnipod questions: https://github.com/LoopKit/loopdocs/blob/main/docs/faqs/omnipod-faqs.md
- Dexcom G6 HealthKit delay: https://www.dexcom.com/en-us/faqs/how-do-i-share-glucose-data-from-dexcom-g6-app-to-apple-health-app

## Evidence boundaries

Loop's iOS Omnipod 5 integration and BCDiabetes' clinic-supported use demonstrate technical feasibility; neither validates a new bespoke controller. BCDiabetes is a clinical-operational reference; LoopDocs/upstream source are the implementation authority for the particular released version. No device communication protocol or dosing algorithm has been copied into this starter.
