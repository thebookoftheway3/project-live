# Optional Decisions provider — documentation feasibility

Checked 24 October 2026 using the fetched [official Decisions guide](https://developers.openai.com/api/docs/guides/decisions). No API call, account access check or integration was performed.

## Verified interface facts

The guide documents `POST /v1/decisions` with `gpt-6-luna` as the currently supported model. Requests contain `model`, shared `input` and named `questions`; responses contain typed `answers`. Question types are `predicate`, `choice` and `score`. Predicates return an estimated probability; choices and scores return distributions and separate confidence values. [Source](https://developers.openai.com/api/docs/guides/decisions#how-decisions-work).

Supported evidence includes text, images and user-role JSON parts. Images can use inline data URLs or public image URLs. Files, audio and item references are unsupported; `file_id` is unavailable. Refusals must be handled. The guide recommends separate requests for questions dependent on earlier answers and application-labelled data to choose thresholds. [Source](https://developers.openai.com/api/docs/guides/decisions#evaluate-a-conversation), [image inputs](https://developers.openai.com/api/docs/guides/decisions#check-an-image-for-visible-damage), [question sequencing](https://developers.openai.com/api/docs/guides/decisions#ask-multiple-questions).

## Project interpretation and limits

Decisions is a candidate for bounded questions about selected frames and structured context, such as container presence or regular/diet/unknown classification. The fetched guide does not establish continuous video tracking or medical calibration. Audio requires a different provider or separately authorized feature extraction; converting sound to features does not make it direct audio support.

Keep provider serialization inside an adapter. The generic contract must not require OpenAI-specific fields or models. A provider probability is not automatically a calibrated observation likelihood for the joint Bayesian model. Do not multiply it into a posterior without a documented evidence model.

No image is to be made publicly accessible merely to satisfy an API input option. Any later external inference requires explicit purpose/destination permission, minimal selected data, retention review and checks for other people present. API capability is not permission to upload.

## Work remaining — LIVE-020

Before implementing a live adapter, recheck the guide and linked API reference, availability for the intended account/region, current SDK/interface and costs. Define label/score mapping, refusal and invalid-output normalization, deadline/cancellation behavior, measured latency, usage accounting, consent revocation and calibration evaluation. Do not infer account eligibility or data controls from general product availability.

The first vertical slice uses a mock provider only. Raw-media uploads, paid calls, API keys and live integration are outside this architecture task. Local algorithms and other providers remain equally valid implementations.
