# Revision 2 implementation backlog

The blueprint governs. Status refers to research implementation, not clinical validation.

| ID | Work | Status | Acceptance evidence |
| --- | --- | --- | --- |
| LIVE-001 | Synthetic replay foundation | Implemented | Existing seven tests and deterministic replay |
| LIVE-002 | Pin Loop workspace and dependencies | Implemented | Full commit manifest; unchanged research branches |
| LIVE-003 | Unmodified Loop simulator baseline | Pending | Reproducible build/test commands, exact toolchain and actual results |
| LIVE-004 | Timestamped observational contracts | Design next | Observed/received times, units, provenance, missingness, duplicates, late events |
| LIVE-005 | BeliefSnapshot and hypothesis contracts | Design next | Revision 2 fields; auditable evidence cutoff; hypotheses distinct from facts |
| LIVE-006 | Confirmed action history | Pending | Shadow recommendations excluded from actual action inputs; uncertain delivery preserved |
| LIVE-007 | Transparent baseline forecaster | Pending | Predictive intervals, chronological evaluation and documented assumptions |
| LIVE-008 | Known-state synthetic Bayesian cases | Pending | Analytic or known reference posterior; correlated errors, ambiguity and missing data |
| LIVE-009 | Sequential Bayesian prototype | Pending | Explicit prior, transition, likelihood and update; competing modes and fit checks |
| LIVE-010 | Calibration and model comparison | Pending | Proper scores, interval coverage, discrete-event scores, calibration by horizon/context |
| LIVE-011 | Dual-CGM quality model | Pending | Separate traces, common-mode faults, disagreement and source ablations |
| LIVE-012 | Active evidence acquisition design | Confirmed requirement; design pending | Information benefit, permissions, costs, failed acquisition and stopping behavior |
| LIVE-013 | Product clarification design | Open decision | Attention budget, timing, accessibility and unknown/no-response behavior |
| LIVE-014 | Read-only device feasibility | Pending | Supported interfaces and non-interference; no treatment change required |
| LIVE-015 | Generalisation and accessibility | Pending | Explicit target populations, missing-hardware conditions and subgroup evaluation plan |
| LIVE-016 | Public contribution and release process | Foundation | License, source provenance, CI, PR process and tracked limitations |

Do not start real device acquisition or implement product prompting merely because the specification names them. Implement bounded scenarios after defining their contracts and acceptance criteria. Preserve failed experiments and negative results.
