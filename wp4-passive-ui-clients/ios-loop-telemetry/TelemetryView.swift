// SPDX-License-Identifier: AGPL-3.0-only
import SwiftUI

// View-only scaffold: injected synthetic display state; no pump manager or BLE.
struct TelemetryView: View {
    let observationCount: Int
    let sourceStatus: String
    let requestSyntheticClearance: (Int) -> Void
    @State private var clearanceMinutes = 5

    var body: some View {
        Form {
            Text("Research preview — not treatment advice")
                .font(.headline)
            Text("Source: \(sourceStatus)")
            Text("Observations: \(observationCount)")
            Stepper("Preview clearance: \(clearanceMinutes) min",
                    value: $clearanceMinutes, in: 1...15)
            Button("Request synthetic clearance") {
                requestSyntheticClearance(clearanceMinutes)
            }
            Text("A request is not acknowledgement or delivery.")
        }
    }
}
