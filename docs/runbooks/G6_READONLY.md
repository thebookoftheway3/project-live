> Historical starter material. The Context-Aware Insulin System blueprint governs; use this document selectively. See the root PROJECT_BLUEPRINT.md and docs/PROJECT_DIRECTION.md. Setup commands here are not current completion evidence.

# Dexcom G6 read-only data intake — research task, not yet implemented

Dexcom G6 is one candidate read-only integration. Preserve the independently operating treatment arrangement while building simulation and replay. No participant equipment is specified by this runbook.

## Findings to verify in a development environment

- LoopDocs describes local G6 reading using the Dexcom G6 application running on the same iPhone as Loop; internet need not be involved.
- Dexcom's official G6 -> Apple Health path delays readings by about three hours, so it is **not a real-time feed**.
- An independent interface for a separate Python backend has **not yet been demonstrated**. Do not assume one exists or change Dexcom pairing to find out.
- Data lineage must include sensor timestamp, receive timestamp, quality, any missing-data interval and configuration/version.
- Review Xcode simulator CGM sources, LoopKit CGM manager interfaces, Loop export/replay formats and approved read-only logging. A real G6 observation bridge requires separate design and testing.

## Phases

1. Replay **synthetic** CGM observations via existing parser.
2. Inspect Loop's simulator and available sample/test fixtures (no live devices).
3. Agree on a read-only adapter and verify non-interference with Tandem/Dexcom.
4. Only then test *passive* observations. External sensors and personal data are excluded from Git.

No claims of compatibility or medical safety are established by this repository.
