# Build Plan

## Completed Research Baseline

- [x] 1. **Problem selection** - selected the Transaction Agent problem: deciding whether to approve, hold/question, or stop a transaction under uncertainty
- [x] 2. **State and action framing** - defined the hidden states as legitimate/fraudulent and the available decisions as approve, hold, and stop
- [x] 3. **Evidence direction** - identified transaction amount, transaction time, merchant history, recent transaction activity, customer profile, and historical behavior as relevant evidence
- [x] 4. **Belief update direction** - established that the agent should maintain and update belief about the hidden state rather than treat each signal as isolated
- [x] 5. **Decision-cost direction** - established that decisions should consider expected cost and transaction context rather than a single fixed threshold
- [x] 6. **Hold-state refinement** - incorporated human feedback that hold/review should be a first-class action when evidence is weak, missing, conflicting, or low-confidence
- [x] 7. **Initial evaluation baseline** - completed the original 15-case evaluation with 11/15 correct decisions, about 73.3% accuracy
- [x] 8. **V2 evaluation work** - created existing v2 / 35-test-case work for the next evaluation pass

## Preservation Rules

- [x] 9. **Do not recreate original 15-case evaluation** - preserve the 15-case result as historical baseline evidence, not as new implementation work
- [ ] 10. **Locate and preserve v2 cases** - identify where the existing v2 / 35 test cases live, document the source, and avoid overwriting them

## MVP Implementation

- [ ] 11. **Domain model** - add Python data structures for transactions, customer profiles, evidence signals, beliefs, action costs, decisions, verification responses, and pending/timeout outcomes
- [ ] 12. **Profile summary** - derive normal customer behavior from historical transactions, including typical amounts, merchants, times, locations, and spending patterns
- [ ] 13. **Evidence extraction** - compare an incoming transaction with the customer profile and produce explicit evidence without inventing missing information
- [ ] 14. **Belief update engine** - update legitimate/fraudulent probabilities from priors and observed evidence
- [ ] 15. **Expected-cost decision engine** - calculate expected cost for approve, hold, and stop, then choose the lowest-cost action
- [ ] 16. **Dynamic decision threshold behavior** - account for transaction context and cost differences so the agent does not rely on one fixed threshold for every transaction
- [ ] 17. **Hold and verification loop** - model hold/question behavior, customer verification, no-response timeout, and a second belief update from new evidence
- [ ] 18. **V2 evaluation runner** - evaluate the decision process against the existing v2 / 35 test cases and compare results to the 15-case 73.3% baseline
- [ ] 19. **Decision trace output** - show evidence, prior belief, updated belief, expected costs, selected action, and follow-up belief updates in an inspectable report

## Later / Open

- [ ] 20. **Configurable assumptions** - decide whether priors, likelihoods, thresholds, and costs should live in code, config, or data
- [ ] 21. **Dataset experiment path** - decide whether to use public fraud datasets such as IEEE-CIS or Fraud Detection Handbook simulated data after the prototype is stable
- [ ] 22. **LLM role definition** - decide whether an LLM should extract evidence, explain decisions, simulate verification, or remain outside the core decision engine
- [ ] 23. **Interface decision** - decide whether the project should remain a script/prototype or become a CLI, notebook, API, or web UI
