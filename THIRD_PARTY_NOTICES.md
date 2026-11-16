# Source and license provenance

Project LIVE's original code and documentation are offered under the root MIT License. The initial synthetic Python code came from the project-supplied Codex starter archive; source hashes are recorded in `docs/SOURCE_MANIFEST.json`. The governing specification comes from the project-supplied Context-Aware Insulin System blueprint, Revision 2; the public adaptation omits personal history and records subsequent project direction.

Loop and its dependencies remain separate repositories. No Loop source, binaries or graphics are vendored in Project LIVE. The pinned workspace and component revisions are listed in `docs/UPSTREAM_BASELINE.json`.

The upstream Loop license includes MIT terms and exceptions for particular frameworks and graphics. These notices are preserved in the fork. Project LIVE's MIT License does not replace any upstream license or grant rights in third-party material.

- Loop license: https://github.com/LoopKit/Loop/blob/c30b5c89b1dc4151628f33f1384dd4796eaeeec2/LICENSE.md
- MIT license reference: https://opensource.org/license/mit

Review each component's own notices before copying or redistributing it. Linked research documents retain their original ownership and are not relicensed by this repository.
# Surfer OS refactor provenance (2026-11-16)

The WP1–WP4 additions are Codex-assisted original research scaffolding; no Loop,
OmnipodKit, camera/model implementation or device SDK was copied into these paths.
Supplied design references are identified in [the source manifest](docs/SOURCE_MANIFEST.json),
with private context omitted from the public derivative. Existing attribution and
MIT notices remain intact after relocation.

New AGPL-marked source scopes and the commercial-rights limitations are described
in [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md). The full AGPL licence text is
copied unmodified from GNU. Optional FastAPI/uvicorn/httpx dependencies and their
transitive packages retain their own licences; exact versions/hashes are in
`wp2-bayesian-voi-engine/requirements-service.txt`. Public Python, Mosquitto and
Ollama container index digests are recorded in that package's `image-lock.json`.
Neither pinning nor this record grants rights to third-party model weights.
SAM 2, Depth Anything V2, Re-ID and Brilliant device implementations are referenced
but not vendored or downloaded. Review each selected checkpoint/SDK licence before
future integration or OEM packaging.
