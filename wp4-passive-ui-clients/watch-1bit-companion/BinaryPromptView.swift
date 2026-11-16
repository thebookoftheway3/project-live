// SPDX-License-Identifier: AGPL-3.0-only
import SwiftUI
#if os(watchOS)
import WatchKit
#endif

struct BinaryPromptView: View {
    let question: String
    let expiresAt: Date
    let reply: (Bool) -> Void
    @State private var answered = false

    var body: some View {
        VStack {
            Text(question)
            Button("Yes") { respond(true) }
            Button("No") { respond(false) }
        }
        .disabled(answered)
        .onAppear {
            #if os(watchOS)
            if Date() < expiresAt { WKInterfaceDevice.current().play(.notification) }
            #endif
        }
    }

    private func respond(_ answer: Bool) {
        guard !answered, Date() < expiresAt else { return }
        answered = true
        reply(answer) // transport must preserve prompt identity; no answer is unknown
    }
}
