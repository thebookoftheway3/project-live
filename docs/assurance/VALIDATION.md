# Transfer assessment validation and limitations

Prepared 24 October 2026 on `codex/safety-methodology-transfer`, based on main `0a99fa78ed9d2a7c818f90933afc93a448375de5`. This is documentation validation and bounded evidence for the [claims matrix](CLAIMS_MATRIX.md), not clinical validation, certification or proof of equivalent residual risk.

## Evidence subject and reproduction

E01/E02 refer to unchanged main code: runtime Git tree `2b57b7b444da627b1eb1729a86cffb18c0470432`, test tree `cf9d4cb82fcb7eddc0314b83654efc1d224c338f`. Fixture `data/synthetic_example.jsonl` SHA-256: `f0200775e891e794db6ae32a26277613f7e50d00b44f17bdcc614abc9ce3186e`. Run date: 24 October 2026. Executor: Codex-assisted local session; no independent human reviewer. Python **3.12.14**, using the desktop-bundled interpreter directly; examples below assume `python3` selects that supported interpreter.

```sh
python3 --version
python3 -m unittest discover -s tests -v
python3 -m project_live.cli replay data/synthetic_example.jsonl
git diff --check
```

E01 observed: all **seven tests passed**; replay emitted **six records**, each with `pump_authorization: false`. The suite exercises only the starter's specified cases. No virtual-sensor, historical-query, permission-revocation or provider-worker acceptance tests were added or executed. E01 does not establish those safeguards.

E02 source inspection covered `events.py`, `context.py`, `replay.py`, `safety_boundary.py` and the tests. The following independent synthetic probe reproduced shallow payload mutability:

```python
from project_live.events import Observation
obj = {"schema_version": 1, "id": "synthetic-mutability-check",
       "at": "2026-10-24T10:00:00Z", "kind": "vision_feature",
       "source": "synthetic-check", "synthetic": True,
       "payload": {"feature": "vision_table_eating"}}
event = Observation.parse(obj)
original = event.payload["feature"]
obj["payload"]["feature"] = "vision_food_preparation"
print(event.payload is obj["payload"], event.payload["feature"] != original)
```

Actual result: **True True**. This is a counterexample to deep observation immutability, not a failed existing unit test or evidence that a virtual-sensor implementation exists. The probe used only an in-memory synthetic object and wrote no research data. No runtime fix is included; preserve the finding for separately scoped contract/implementation review.

## Documentation and provenance checks

- E03 inspected main and the relevant documents in both PR change sets, including the specified methodology, architecture, contracts, ledger, backlog and graph proposal documents. PR #2 was open at `2c31186f753e5f6d1bfbcb3de075325bfd3915e1`; PR #3 was open at `5886ed63c37fed876dd0a54c20ebd3c7ef224905`. The PR description records the final remote check after publication.
- Locally inspected the relevant engineering sections of the privately supplied traffic reference in place. Source publication rights, traffic deployment, regulatory approval and test-result claims remain unverified. No original was copied into the repository or published; commercial/partner-specific material was excluded from the assessment.
- One-off local Python documentation check passed: **27 relative Markdown file/heading links**, nine complete C/H/S/V rows, E01–E03 definitions and whitespace. Protected-file comparison against main passed; `git diff --check` passed. No YAML, workflow or executable configuration was changed.
- Reviewed the public diff for source quotations, original-source attachments/paths, partner terms, personal data and unsupported claims. Local overlap screening found **zero contiguous 15-word matches** between the five new documents and the private source. This limited screening does not establish publication rights, prove independence of ideas or replace content review; the scoped review is not an exhaustive secret/PII audit.
- No runtime, test, fixture, dependency, AGENTS, blueprint, architecture contract, requirement ledger or existing PR file was changed other than the small main README navigation addition. New files are the assessment, method, matrix, this record and proposed ADR 0002.

Local check outcomes are separate from remote CI. The PR's checks/description will record actual Python 3.11/3.12 CI results for its published revision; a local pass does not imply a remote pass.

## Limits and next review

No new safeguards have been implemented. No device access, treatment automation, data upload, live provider call, deployment, merge or administrative change was performed. Public research-method references were consulted without sending the private traffic source to them. Source-domain assertions are not independent evidence for LIVE. No clinical study, formal proof, sandbox validation, deployment-isolation audit or independent human safety review was performed.

Recheck affected evidence on changes to code, contracts, permissions, model versions, fixtures, exposure or assumptions. Merge status and proposed decisions must be reconciled with PRs #2/#3 before any follow-on implementation. ADR 0002 remains proposed, and a documentation merge alone would not accept it.

## Integration review — 24 October 2026

The preceding record preserves the original preparation-time scope and E01–E03 evidence. The owner subsequently authorized integration. PR #3 merged as `4ab8501`; PR #4 was updated against it without runtime changes. ADR 0002 now records explicit acceptance of the lightweight trial, linked from the shared methodology, principles, template and ADR register. Pinned earlier proposal snapshots remain historical; acceptance of the method does not establish the claims. Source restrictions and the independent-review gap remain. Required Python 3.11/3.12 CI must rerun on the reconciled revision before merge.
