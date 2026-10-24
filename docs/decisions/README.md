# Architectural decision records

Use sequential, never-reused numbers: `0001-short-title.md`. Copy [the template](0000-template.md); `0000` is a template, not a decision. Link each ADR to requirements, proposals and affected contracts. Check existing ADRs before adding one.

| State | Meaning |
| --- | --- |
| Proposed | Under discussion; does not authorize implementation or claim acceptance. |
| Accepted | Explicitly approved by the responsible maintainer after review; record date, decision-maker and actual reviewers. |
| Superseded | Replaced by a linked accepted ADR; retain the old record and reciprocal links. |
| Rejected | Considered and declined with reasons, evidence and any conditions for reopening. |

A document merge alone does not silently change a proposed ADR to accepted. Preserve substantial revisions, objections and negative evidence through Git history and linked discussion. Revisit accepted decisions with a new proposal when assumptions fail. Security-sensitive details can have a restricted record plus a redacted public rationale.

Changes to interfaces, architectural boundaries or invariants require an ADR or an explicit link to an existing applicable decision. Use ADRs for modular monolith versus microservices, event transport, model ownership, inference-provider interfaces, sensor plugin isolation and future distributed execution. A small internal refactor that preserves contracts need not generate an ADR.

| ADR | Status | Scope |
| --- | --- | --- |
| [0001](0001-modular-monolith-first.md) | Accepted | Initial implementation structure and criteria for later distribution |
| [0002](0002-lightweight-assurance-traceability.md) | Accepted | Proportionate research claim traceability and evidence validity |

Existing blueprint decision identifiers (such as D08) retain their meaning; ADR numbering does not renumber them. PR #2 integrates design requirements; its concrete contract choices remain in the [open-decision register](../PROJECT_DIRECTION.md#unresolved-engineering-decisions). The Adaptive Perception Graph remains a separate proposed design.
