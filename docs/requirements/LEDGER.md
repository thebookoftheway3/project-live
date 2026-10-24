# Requirements ledger — Revision 2

Source: the governing blueprint plus explicit project direction. Proposed architecture is not marked implemented merely because it is documented.

| ID | Requirement | Status | Required evidence |
| --- | --- | --- | --- |
| R00 | Return attention, preserve human competence and support recovery | Confirmed goal | Workload, sleep, interruption and recovery evaluation |
| R01 | Preserve independently operating treatment during initial research | Initial boundary | No runtime pump transport; non-interference evidence for future adapters |
| R02 | Interpret context with history | Illustrative starter only | Temporal inference and prospective comparisons |
| R03 | Respect control over sensing resources and data | Design pending | Permissions, retention, provenance and availability |
| R04 | Accessible low-burden interaction | Design pending | User research across contexts and abilities |
| R05 | Modular home/office/car/mobile context | Environment tracking only | Real adapter validation and context uncertainty |
| R06 | Environment cannot grant dosing authority | Synthetic tests pass | Preserve boundary in each implementation |
| R07 | Treatment remains independent of experimental infrastructure | Architectural requirement | Dependency and failure analysis |
| R08 | Progressive, replaceable sensor integrations | Initial schema only | Capability contracts and missing-device behavior |
| R09 | Read-only CGM acquisition | Not implemented | Supported interfaces, time quality and non-interference |
| R10 | Distinguish observations, beliefs, actions and outcomes | Partial replay | Versioned schemas and immutable prediction cutoffs |
| R11 | Distinguish command intent, delivery and uncertain effect | Design pending | Confirmed action semantics and ambiguity tests |
| R12 | Initial software cannot actuate insulin | Synthetic implementation | No real pump client or credentials; boundary tests |
| R13 | Actively seek useful evidence | Confirmed requirement | Measured uncertainty reduction versus acquisition and attention cost |
| R14 | Carefully design possible clarification prompts | Open design | Timing, accessibility, burden and unanswered cases |
| R15 | Maintain joint Bayesian belief over hidden states and discrete modes | Required; not implemented | Priors, transitions, likelihoods, updates and known-state reference cases |
| R16 | Report posterior predictive distributions and competing explanations | Required; not implemented | Horizon-specific distributions, multimodality and evidence audit |
| R17 | Model dependent evidence and source missingness | Required; not implemented | Shared CGM bias, lag, repeated and unavailable signals |
| R18 | Expose model mismatch, OOD and calibration status | Required; not implemented | Prospective proper scores, interval coverage and rare-context checks |
| R19 | Audit BeliefSnapshot fields | Required; not implemented | Evidence cutoff, version, provenance, hypotheses and shadow flags |
| R20 | Enable open reuse and contributions for the diabetes community | Public foundation | Open-source license, accessible documentation and contribution workflow |
| R21 | Separate per-person calibration from general claims | Required; not validated | Population scope, held-out people/contexts and subgroup evaluation |

D08 remains open: the long-term division of human and automated control. Public benefit does not imply that the present prototype is validated for all people with diabetes.
