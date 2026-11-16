# WP2 — Bayesian inference and attention research

`src/project_live` preserves the baseline package and its consent-gated Loop G6
consumer byte-for-byte. The root `project_live` link preserves source-checkout CLI
commands; installed packages use setuptools' physical source path. On platforms
without symlink support, install the package or put this directory's `src` on
`PYTHONPATH`. Do not bypass the consumer to feed private data to the HTTP service.

The new modules are separate experiments:

- `detector_health.py`: first-12-hour variance hypothesis, stale/unknown handling
  and nocturnal low/motion co-occurrence labels. ARTIFACT_SUSPECT never establishes
  that a low is false or authorizes suppression of an established medical alarm.
- `voi_attention_gate.py`: finite-state EVSI in declared utility units compared
  with time/context-dependent attention cost. Consent, duplicate evidence,
  cooldown and rolling 24-hour candidate budgets gate synthetic Yes/No prompts.
  An unanswered candidate still consumes budget. Persistent state and multi-user
  dispatch remain future work; no clinical alarm enters this gate.
- `preemption_api.py`: optional FastAPI session harness, with strict synthetic
  schemas, bearer authentication, idempotent requests and non-renewable active
  clearance intervals. Voice callbacks record answers/next-level candidates;
  **no external voice call is made**. Neither an API acknowledgement nor a manual
  input means a device command was delivered.
- `surfer_session.py`: shared home/nomadic evidence, one pending question,
  illustrative 25-minute cooldown and 180-second timeout, unknown replies and
  bounded manual attention clearance. The older Surfer OS examples inspire these
  experiments; they do not define current clinical contracts. See the
  [updated product design](../docs/SURFER_OS.md).

From root, test the optional API in a separate environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r wp2-bayesian-voi-engine/requirements-service.txt
PYTHONPATH=wp2-bayesian-voi-engine/src .venv/bin/python -m unittest discover -s wp2-bayesian-voi-engine/service_tests -v
```

The service dependencies are separate from the dependency-free core. Update their
lock with `pip-compile --generate-hashes`; review changes before installing.
The optional Compose profile has FastAPI, Mosquitto and Ollama on an internal
network, with only loopback API exposure and no private-file mounts. It is a local
development composition suitable for later VPS verification, **not a verified VPS
deployment**. A model and model licence must be selected and staged explicitly;
Ollama starts without a VLM. MQTT has no application publisher/subscriber yet.
Use a single API worker; restart loses synthetic session state.

```sh
export LIVE_RESEARCH_API_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
docker compose -f wp2-bayesian-voi-engine/docker-compose.yml up --build
```

This starts local containers only when invoked by the owner. It does not authorize
cloud transfer, real observations, camera capture or device control. See the
[API test approach](https://fastapi.tiangolo.com/tutorial/testing/) and
[Docker internal networks](https://docs.docker.com/reference/compose-file/networks/).
