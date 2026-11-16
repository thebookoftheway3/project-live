# WP3 — Local context research

This package currently contains dependency-free numerical/privacy experiments and
an unintegrated Lua interaction scaffold. No camera, microphone, model weights or
remote inference provider is accessed.

| Track | Executable today | Integration and evidence still needed |
| --- | --- | --- |
| [Top-down quantifier](topdown-quantifier/README.md) | Four-point homography, rectified metric height-grid integration, candidate cadence | Lens/metric calibration, SAM 2 masks, Depth Anything V2 height conversion, held-out food measurements |
| [Room graph](topological-room-graph/README.md) | Budgeted four-stage cascade, expiring portal continuity and strict synthetic export envelope | Local models, consent lifecycle, ambiguity/occlusion handling and enforced egress isolation |
| [Halo/Frame bridge](brilliant-halo-bridge/README.md) | Lua feature/prompt/reply scaffold | Device-specific IMU/acoustic processing, verified audio hardware, BLE and on-device tests |

The [verification plan](../docs/GRANT_VERIFICATION_PLAN.md) distinguishes source
allowlists from actual zero-media-egress evidence. No raw video or biometrics are
stored or exported by these examples; that does not prove a future deployed node
has no other network path.
