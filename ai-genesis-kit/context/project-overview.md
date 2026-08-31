# Project Overview

## Product

Transaction Agent is a Python research/prototype project for transaction decisions under uncertainty. A financial transaction arrives with incomplete information, and the true state is hidden: the transaction is either legitimate or fraudulent.

The project is not a simple fraud/legitimate classifier. Its purpose is to study a sequential decision-making agent that maintains belief about the hidden state, updates that belief from evidence, compares expected decision costs, and chooses between approve, hold/question, and stop.

## Users

The established user is the project builder/reviewer evaluating the Transaction Agent research prototype.

Possible future users, such as fintech researchers, fraud-risk analysts, or engineers, are not yet established as product users and remain an open question.

## Core Behavior

The established decision loop is:

1. A transaction arrives.
2. Available evidence is observed or extracted.
3. The agent updates its belief about whether the transaction is legitimate or fraudulent.
4. The agent evaluates decision thresholds, transaction context, and expected cost.
5. The agent chooses approve, hold/question, or stop.
6. If the transaction is held, customer verification or no-response/timeout behavior can provide new evidence.
7. New evidence flows back into another belief update and decision.

```text
Evidence -> belief update -> expected-cost decision -> new evidence/verification -> belief update
```

Hold/question is a first-class action. It exists for weak, missing, conflicting, insufficient, or low-confidence evidence, especially when the cost of a wrong approve or stop decision is high.

## Research Direction

The established research direction is:

- Bayesian belief updating for `P(Legitimate | Evidence)` and `P(Fraudulent | Evidence)`.
- Expected-cost decision making for approve, hold, and stop.
- Dynamic decision threshold behavior instead of one fixed threshold for every transaction.
- Sequential updates from customer verification or timeout/no-response.
- Explicit evidence handling for amount, time, merchant history, recent activity, location, customer profile, and historical behavior.

LLM confidence must not be treated as the actual transaction probability. Evidence extraction must not invent missing transaction information.

## Current State

Completed research work includes:

- Selected the Transaction Agent problem.
- Defined hidden states as legitimate and fraudulent.
- Defined actions as approve, hold/question, and stop.
- Established hold/question as a real action/state.
- Defined the evidence, belief update, expected-cost decision, and follow-up evidence loop.
- Identified historical behavior, customer profile, transaction amount, time, merchant history, recent activity, and location as relevant evidence.
- Identified Bayesian belief updates as the intended belief model direction.
- Identified expected-cost decision making as central to choosing between actions.
- Recorded human feedback that one fixed threshold is likely insufficient.
- Recorded human feedback that low confidence should not be collapsed into approve or stop.
- Completed the original 15-case evaluation.
- Located the existing v2 / 35-case evaluation source.

## Evaluation Sources

The original 15-case evaluation is historical baseline evidence:

```text
Correct decisions: 11 / 15
Accuracy: 73.3%
```

This 15-case evaluation MUST NOT be recreated as new work. Future evaluation should compare against this baseline rather than rebuilding or overwriting it.

The existing v2 / 35-case evaluation source is:

```text
experiments/transaction_agent_test_cases_v2.csv
```

Preserve this CSV as the source of record for the next evaluation pass. Do not overwrite, recreate, or replace it while implementing the evaluation runner.

## Stack

The repository is currently a Python research/prototype project with Markdown documentation.

No package manager, dependency file, app framework, lint command, test runner, Verify command, CI workflow, database, or deployment target is currently established.

Use standard-library Python first unless a later feature justifies dependencies. Add pytest only through the explicit `$tests` workflow if the project needs a formal test gate.

## Artifacts

Established artifacts include:

- `README.md` - project-facing explanation of the Transaction Agent problem and stage.
- `research-file.md` - research notes, terms, architecture direction, prompts, AI error risks, baseline evaluation, and research direction.
- `discussion-record.md` - human feedback and resulting design changes.
- `experiments/transaction_agent_test_cases_v2.csv` - existing v2 / 35-case evaluation source.
- `ai-genesis-kit/project-plan.md` - project plan.
- `ai-genesis-kit/build-plan.md` - numbered build-plan checklist.
- `ai-genesis-kit/context/project-overview.md` - durable AI-facing source of truth generated from the planning docs.

## Planned Work

Completed build-plan items:

- Problem selection.
- State and action framing.
- Evidence direction.
- Belief update direction.
- Decision-cost direction.
- Hold-state refinement.
- Initial 15-case evaluation baseline.
- V2 evaluation work.
- Preservation of the original 15-case evaluation.
- Location and preservation of the v2 / 35-case evaluation source at `experiments/transaction_agent_test_cases_v2.csv`.

Pending MVP work:

- Add Python data structures for transactions, customer profiles, evidence signals, beliefs, action costs, decisions, verification responses, and pending/timeout outcomes.
- Derive normal customer behavior from historical transactions.
- Compare incoming transactions with customer profiles and produce explicit evidence.
- Update legitimate/fraudulent probabilities from priors and observed evidence.
- Calculate expected cost for approve, hold, and stop, then choose the lowest-cost action.
- Account for transaction context and cost differences so the agent does not rely on one fixed threshold.
- Model hold/question behavior, customer verification, no-response timeout, and a second belief update from new evidence.
- Evaluate the decision process against `experiments/transaction_agent_test_cases_v2.csv` and compare results to the 15-case, 73.3% baseline.
- Show evidence, prior belief, updated belief, expected costs, selected action, and follow-up belief updates in an inspectable report.

Later or open work:

- Decide whether priors, likelihoods, thresholds, and costs should live in code, config, or data.
- Decide whether to use public fraud datasets such as IEEE-CIS or Fraud Detection Handbook simulated data after the prototype is stable.
- Decide whether an LLM should extract evidence, explain decisions, simulate verification, or remain outside the core decision engine.
- Decide whether the project should remain a script/prototype or become a CLI, notebook, API, or web UI.

## Constraints

- Preserve existing research work and evaluation history.
- Preserve `experiments/transaction_agent_test_cases_v2.csv` as the existing v2 / 35-case evaluation source.
- Do not recreate the original 15-case evaluation.
- Do not overwrite, recreate, or replace the v2 CSV while building the evaluation runner.
- Hidden states remain legitimate and fraudulent unless the project explicitly changes scope.
- Actions remain approve, hold/question, and stop unless the project explicitly changes scope.
- Hold/question remains a first-class action for weak, missing, conflicting, or insufficient evidence.
- The agent should use evidence, belief updates, decision thresholds, expected cost, and new evidence/verification loops.
- Bayesian belief updating is the current belief-model direction.
- Expected-cost decision making is the current decision-rule direction.
- A single fixed threshold should not be assumed as the final decision policy.
- LLM confidence must not be treated as the actual transaction probability.
- Evidence extraction must not invent missing transaction information.
- Unestablished product goals, users, metrics, UI, deployment, data storage, and model configuration should remain open questions.
- Do not modify product code, research files, test cases, or `README.md` when only updating planning context.

## Open Questions

- Who is the intended evaluator beyond the project builder/reviewer?
- Should the first runnable implementation be a script, CLI, notebook, API, or small web UI?
- Should priors, likelihoods, thresholds, and costs be hand-authored assumptions, derived from research, learned from data, or loaded from config?
- Which evaluation target matters most next: accuracy, false positives, false negatives, expected cost, consistency, explainability, or another metric?
- What should the timeout rule be when the customer does not respond?
- What role, if any, should an LLM have beyond evidence explanation or extraction?
