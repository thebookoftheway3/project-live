> Historical starter material. The Context-Aware Insulin System blueprint governs; use this document selectively. See the root PROJECT_BLUEPRINT.md and docs/PROJECT_DIRECTION.md. Setup commands here are not current completion evidence.

# Environment modules and experimental sensing matrix

The mobile node accompanies the person; home/office/car nodes provide *additional* context. All nodes publish timestamped observations with source, freshness, confidence, quality, and software version. A missing sensor is missing evidence, not evidence of no event.

| Node | Candidate sensors | Useful inferred context | Prototype interface | Early acceptance criteria |
| --- | --- | --- | --- | --- |
| Always-on mobile | G6 feed (read-only), phone motion, watch activity, location mode, microphone, output audio | Glucose, present activity, possible meal, sleep/wake | `Observation` JSONL then local authenticated stream | Data freshness visible, no pump connection, voice route test |
| Home | RTSP cameras, microphone array, PIR/mmWave occupancy, room conditions, BLE beacons | Kitchen use, table activity, meals, sleep/occupancy | LAN event broker | Sensor dropout/restart test; raw capture local only |
| Office | Workstation state, occupancy, desk audio, wearable, calendar | Focus session, meal breaks, posture/activity | Desktop node to broker | No forced manual tagging; false alerts measured |
| Car | Vehicle status/OBD-II (where permitted), motion, phone connection, seat occupancy, cabin microphone; optional camera | Driving, stopped, passenger presence, response to alert | Read-only vehicle bridge | Reliable driver state; avoid attention-demanding UI |

Environment identity is inferred with provenance and a timeout. Location recognition is an input to **support presentation** and sensor selection, never an insulin command authorizer.

## Sensor families to evaluate

- Audio acoustic features from speech/meal conversation and eating-related sounds; perform local feature extraction before any cloud transfer.
- Video features: table presence, food handling, occupancy, contextual gestures. Run local inference; storage of video is not required for inference.
- Motion and proximity: phone placed on table, hand/wrist activity, BLE/UWB proximity.
- CGM: timestamps, glucose trajectory, CGM data-quality indicators.
- Pump telemetry (future read-only): basal program, confirmed bolus delivery, command/pod status, delivery uncertainty. IOB is a model estimate, not directly measured.
- Sleep/context: phone/watch motion, overnight patterns, resting state, environmental cues.
- Vehicle: ignition/engine state, acceleration, motion, Bluetooth pairing, road context. Do not assume vehicle sensors give medical-grade information.

## Bayesian context engine

Separate observations (sensor reports) from hypotheses (likely eating). Correlated sensors must not be treated as independent; calibrate probabilities using representative data. Keep posterior estimate, evidence provenance, timestamp and competing hypotheses. Optimise useful support over months and years, not just accuracy on individual meals. Initial output is **advisory**.

## Open phone and infrastructure criteria

Test candidate Android/AOSP/GrapheneOS/Linux devices for background execution, audio routing, microphone access, local speech generation, real-time latency, battery, update control, security patching and low-level observability. Avoid assuming the most configurable option is necessarily the most dependable.
