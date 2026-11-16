# Topological room graph

`room_graph.py` advances Zone → Pose → Targeted Re-ID → VLM only while unresolved,
consented and within a call budget. It does not implement these models. Portal
tokens carry zone continuity for at most 30 seconds, with no biometric identity.
Ambiguity must remain unknown; multi-person matching and token consumption/deduplication
are not implemented. Tokens are local objects and are not sent to cloud services.

The example export schema accepts only a version, enumerated event kind and
`synthetic=true`; video, audio, embeddings and arbitrary identifiers are rejected.
This narrow interface does not replace OS/network egress isolation or bystander
consent. Verify those separately before any real-room deployment.
