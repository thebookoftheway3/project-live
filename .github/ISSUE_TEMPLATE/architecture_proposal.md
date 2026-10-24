---
name: Architectural proposal
about: Discuss a significant contract, boundary or infrastructure choice
title: ''
labels: ''
assignees: ''
---

Discuss before implementation. Do not include vulnerabilities or sensitive data; follow SECURITY.md. Use an ADR after the problem and alternatives are understood.

## Problem, motivation and evidence
Link relevant requirements or decisions. Separate observations from assumptions.

## Alternatives and tradeoffs
Include no change and a simpler baseline. Compare operational complexity, fault tolerance, recovery, security, privacy and measured need.

## Affected modules and contracts
Identify ownership, versions, evidence dependencies, replay and idempotency implications; unknown is acceptable.

## Risks and boundaries
Preserve one coherent logical belief state per research subject and strictly non-actuating shadow research. State permission, dependency and attention costs.

## Acceptance criteria, reversal and open questions
What would establish benefit, disprove assumptions or trigger reconsideration? Identify the intended ADR and separate implementation scope.
