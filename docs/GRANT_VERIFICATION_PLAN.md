# Surfer OS / Project LIVE — 60-day verification plan

**Status: proposed measurements, not achieved results or a funded study.** This
plan makes WP1–WP4 reviewable for discussions with Almi Väst / Vinnova. It does not
assert current programme eligibility, an award, regulatory exemption or clinical
readiness. See [product design](SURFER_OS.md) and [FMEA](FMEA_SAFETY_ANALYSIS.md).

The clock starts only when fixtures, protocols, versions and necessary reviewers
are ready. Bench work uses synthetic signals and simulated endpoints. Any human
field observation requires its own consent, privacy and study review; independent
treatment and its alarms remain unchanged. No real pump actuation is in this plan.

## Targets and definitions

| WP | Target | Measurement and denominator | Present evidence / acceptance gap |
| --- | --- | --- | --- |
| WP1 | 0 upward violations | Count simulated outputs above the schedule across the complete predefined fault campaign; report cases, duration, reset states and seeds | Bounded host tests only; independent hardware enforcement unverified |
| WP1 | Wi-Fi → LTE-M failover <3 s | Time from controlled loss of usable Wi-Fi MQTT delivery to first acknowledged, deduplicated message over LTE-M; report max, p50, p95, failures and cold/warm registration separately | Bearer selection oracle only; no measured radio failover |
| WP1 | 100% 30-minute watchdog expiry in defined blackout cases | All predefined blackout/reset/clock scenarios reach the specified simulated expiry; retain timing traces | Software timing assertions only; pod fallback and physical watchdog behavior unknown |
| WP2 | >80% fewer daily research interruptions | `100 * (1 - candidate_interruptions / matched_baseline_interruptions)` on identical exposure windows; denominator zero means undefined | Synthetic candidate counts only; no field result or medical-alarm reduction claim |
| WP2/WP4 | >85% binary response rate | Valid timely answers / all delivered eligible questions; timeouts and delivery failures reported separately | Session timeout/reply tests only; delivery, accessibility and burden unmeasured |
| WP3 | Volume error <12% | Predeclare normalized MAE = `100 * sum(abs(estimate-reference)) / sum(reference)` across held-out nonzero volumes; also report MAE in cm³ and per-item relative errors | Numerical box oracle only; no food/model performance result |
| WP3 | 0 bytes raw video/biometrics leaving edge | Network capture at every permitted interface during normal/fault/restart scenarios, plus schema and process-egress inspection | Export allowlist unit tests only; whole-node isolation unverified |
| WP4 | Independent setup <30 min | Fresh supported host to documented synthetic demo, recording prerequisites, downloads, elapsed time and failures | One-command local script; no independent reviewer timing |

These are engineering targets. Avoid hiding missed events by eliminating prompts:
compare false negatives, task relevance, calibrated prediction quality and burden
alongside interruption counts. Established clinical alerts are excluded from the
gate and must never be disabled to improve a KPI. Zero observed failures does not
establish zero failure probability; publish sample counts and uncertainty bounds.

## Schedule and evidence

| Days | Work | Exit evidence |
| --- | --- | --- |
| 1–10 | Freeze source/tag, requirements, parameter assumptions, fixtures, consent boundaries and measurement protocols | Independent protocol review or recorded missing-review blocker; reproducible baseline |
| 11–20 | MMU host fault campaign and isolated dummy-load hardware feasibility | Reset/clock/NaN/gap tests, timing instrumentation plan; no device attached to a person |
| 21–35 | Matched attention replay and calibrated object-volume experiments | Frozen training/calibration split; held-out scoring, ablations and failure artifacts |
| 36–50 | Local-only integration and home/nomadic continuity simulation | Network captures, consent/revocation tests, duplicate/offline/restart cases and delivery acknowledgements |
| 51–60 | Replication, analysis and evaluator package | Exact revisions, commands, denominators, negative results, limitations and independent reviewer findings |

Publish synthetic fixtures, methods, aggregate results and hashes. Keep authorized
private evidence outside Git with access/retention records. Preserve original
predictions before outcomes and later reinterpretations separately. A model chosen
after scoring cannot claim prospective benefit. Raw captures are never grant
attachments by default. If a prerequisite fails, stop that measurement and report
the failure rather than silently changing a threshold or denominator.

Responsibilities must be assigned before field work: engineering measurement,
privacy/security, human factors, statistical evaluation and qualified clinical
oversight where applicable. No independent specialists are currently recorded as
having reviewed this refactor. Actual checks are in
[WP verification evidence](assurance/WP_REFACTOR_VALIDATION.md).
