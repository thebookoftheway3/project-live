# WP4 — Passive clients

The [iOS view](ios-loop-telemetry/TelemetryView.swift) displays injected research
status and emits a bounded synthetic-clearance request through a supplied closure.
The [watch view](watch-1bit-companion/BinaryPromptView.swift) offers Yes/No, rejects
expired replies and requests a watch haptic when a current prompt appears.

These are SwiftUI source scaffolds, not signed or installable applications. They
have no pump manager, Bluetooth stack, clinical alarm suppression or autonomous
actuation. Prompt identity, authentication, acknowledgements, accessibility,
background delivery and phone/watch transport need dedicated integration tests.

The existing restricted Loop fork remains a separate upstream checkout; it is not
copied or relicensed here. Its versioned observations are consumed only by the
[consent-gated interface](../docs/assurance/LOOP_G6_INTERFACE.md). No app signing,
deployment or phone pairing is part of this refactor.
