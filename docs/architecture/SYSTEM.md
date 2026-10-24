# Bayesian shadow-system architecture — Revision 2

Governing reference: `PROJECT_BLUEPRINT.md`, especially sections 4, 6, 10–14. These are design requirements; the current starter implements only synthetic replay and illustrative meal inference.

## Data flow

```text
Independent observations and confirmed action history
                  |
       timestamps / provenance / quality
                  |
  Bayesian filtering: latent state x, discrete modes m
       predict -> observe -> update -> check fit
                  |
    posterior predictive distributions and explanations
           /
  evidence gaps                  shadow evaluation
       |                              |
 acquisition planner            prospective outcomes
       |
 authorized sensor requests / possible human clarification
       |
 new observations return through the same ingestion boundary
```

No output path reaches a live pump. Actual treatment continues independently. A shadow recommendation never enters confirmed action history unless an independently recorded real action establishes what occurred.

## Belief representation

Maintain `p(x_t, m_t | y_1:t, u_1:t-1)`, including dependencies between latent variables and discrete hypotheses. Observations are not latent states; modes are hypotheses, not diagnoses. Preserve multimodality when several explanations fit.

Document research priors, process transitions, source-specific likelihoods, missingness mechanisms and limitations of identifiability. Distinguish slow parameters, rapidly changing states and possible change points. Keep per-person posterior state separate from shared model code and population research priors.

Two CGMs can have common-mode and temporally correlated errors. Do not blindly multiply likelihoods or erase disagreement by averaging. Wearable signals and images remain indirect evidence. A consumption-volume distribution must allow zero when ingestion is unconfirmed.

## BeliefSnapshot contract to specify

- `inferred_at`, `evidence_cutoff`, `model_version`.
- Observed sources, freshness, quality and provenance.
- Posterior state summaries, credible intervals and retained distribution/mode representation.
- Discrete hypotheses and probabilities, including competing explanations.
- Glucose posterior predictive distributions by horizon.
- Supporting and contradictory evidence, mismatch flags, OOD flags and calibration status.
- Evidence needed to reduce uncertainty.
- `shadow_only: true`, `may_actuate_insulin: false`.

This is a required interface design, not an implemented API. Late-arriving data must produce traceable revisions without changing what was known at an earlier forecast's evidence cutoff.

## Active information gathering

The planner should identify which uncertainty matters, which authorized source could reduce it and whether acquisition is worth its privacy, energy and attention costs. Evaluate actual improvement against passive acquisition. Repeated evidence is not automatically independent evidence. Record failed requests and source unavailability.

Human clarification is a candidate mechanism, with interaction design still open. An unanswered prompt remains unknown. When no useful evidence is obtainable, the belief state must retain uncertainty rather than invent certainty.

## Evaluation and development gates

Start with a transparent CGM/confirmed-action baseline with predictive intervals. Use known-state synthetic cases, chronological holdouts and prospective predictions before introducing richer models. Compare Bayesian variants to simpler and non-Bayesian baselines.

Measure appropriate proper scoring rules, interval coverage by horizon, Brier/log loss for discrete events, rare-mode calibration, mismatch detection and marginal value of each sensor. Include shared CGM bias, missing data, late evidence, mode collapse, site-change hypotheses and distribution shift. Agreement with a person's decisions does not identify the outcome of an unperformed alternative intervention.

The starter's grouped log-odds calculation is an illustrative component, not this joint state estimator. Preserve its useful tests while replacing or extending it in measured steps.
