# Project Overview

## Product

Transaction Agent is the Week One Python research/prototype project for transaction decisions under uncertainty. The original research problem is that a financial transaction arrives with incomplete information, and the true state of the transaction is hidden.

The hidden states are:

- Legitimate.
- Fraudulent.

The available actions are:

- Approve.
- Hold/question.
- Stop.

The project is not a simple fraud/legitimate classifier. Its research direction is a decision-making agent that maintains belief about a hidden state, updates that belief from evidence, and chooses an action by considering expected cost.

## Core Decision Loop

The established loop is:

1. A transaction arrives.
2. Available evidence is observed or extracted.
3. The agent updates its belief about whether the transaction is legitimate or fraudulent.
4. The agent considers decision thresholds, transaction context, and the expected cost of each action.
5. The agent chooses approve, hold/question, or stop.
6. If the transaction is held, customer verification or no-response/timeout behavior can provide new evidence.
7. New evidence flows back into another belief update and decision.

This can be summarized as:

```text
Evidence -> belief update -> expected-cost decision -> new evidence/verification -> belief update
```

## Why Hold Is First Class

Hold/question is an established action, not an error state or a vague fallback. It exists because low confidence, weak evidence, missing evidence, conflicting evidence, policy conflict, or high cost of a wrong decision should not be collapsed directly into approve or stop.

The discussion record established that weak evidence should lead to review or verification when the system does not have enough proof for a stronger decision. This makes hold/question part of the agent's actual state machine and decision policy.

## Research Direction

The research direction is:

- Bayesian belief updating for maintaining `P(Legitimate | Evidence)` and `P(Fraudulent | Evidence)`.
- Expected-cost decision making for comparing approve, hold, and stop.
- Dynamic threshold behavior, because one fixed probability threshold is likely insufficient across different transaction contexts and transaction amounts.
- Sequential updates, because customer verification or timeout/no-response can become new evidence.
- Explicit evidence handling, including unusual amount, unusual merchant, unusual time, unusual location, merchant history, recent transaction activity, and customer profile behavior.

The central research question is whether a transaction agent can make more consistent decisions by maintaining an explicit belief about the hidden state, updating that belief with new evidence, and selecting actions according to expected cost.

## Completed Work

Completed Week One work includes:

- Selected the Transaction Agent problem.
- Defined the hidden states as legitimate and fraudulent.
- Defined the available actions as approve, hold/question, and stop.
- Identified historical transaction data and customer profile information as inputs for normal-behavior context.
- Identified current transaction evidence as the basis for belief updates.
- Identified Bayesian belief updates as the belief-model direction.
- Identified expected-cost decision making as the decision-rule direction.
- Established that additional evidence from customer verification can update the belief again.
- Established pending/timeout as the unresolved path when the customer does not respond.
- Recorded human feedback that transaction decisions should consider context and the cost of wrong decisions instead of relying on one fixed threshold.
- Recorded human feedback that hold/review should be a separate state when confidence is low or evidence is insufficient.
- Completed the original 15-case evaluation.
- Created existing 35-test-case/v2 work for the next evaluation source.

## Historical Evaluation Baseline

The original evaluation used 15 transaction test cases.

```text
Correct decisions: 11 / 15
Accuracy: 73.3%
```

This original 15-case evaluation is historical baseline evidence and MUST NOT be recreated as new work. Future evaluation should compare against this baseline rather than rebuilding or overwriting it.

## Current V2 Evaluation State

The project history establishes that 35-test-case/v2 work already exists and should be preserved. That v2/35-case work is the next evaluation source.

The current next step is to locate and preserve the v2/35-case source, document where it lives, and continue from there. Do not overwrite or replace it while locating it.

The exact visible file path and storage format for the v2/35-case source are not yet established in the current overview.

## Current Prototype And Artifacts

The current repository state is a Python research/prototype project with Markdown research artifacts.

Established artifacts include:

- `README.md` - project-facing explanation of the Transaction Agent problem and stage.
- `research-file.md` - research notes, terms, architecture direction, prompts, AI error risks, baseline evaluation, and research direction.
- `discussion-record.md` - human feedback and resulting design changes.
- `ai-genesis-kit/project-plan.md` - project plan.
- `ai-genesis-kit/build-plan.md` - build-plan checklist.
- `ai-genesis-kit/context/project-overview.md` - this durable AI-facing source of truth.

Current technical state:

- Language: Python.
- Project type: research/prototype.
- Product implementation: not yet established beyond the prototype/research direction.
- Test runner: not configured.
- Package manager: not configured.
- CI: not configured.
- Database: not established.
- Deployment target: not established.

Do not invent runtime behavior, package structure, app architecture, test results, or deployment details that are not present in the project.

## Pending Work

The next build-plan item is:

- Locate and preserve v2 cases - identify where the existing v2 / 35 test cases live, document the source, and avoid overwriting them.

Pending MVP work after that includes:

- Add Python domain models for transactions, customer profiles, evidence signals, beliefs, action costs, decisions, verification responses, and pending/timeout outcomes.
- Build profile summary logic from historical transactions.
- Extract evidence by comparing incoming transactions with customer profiles.
- Update legitimate/fraudulent probabilities from priors and observed evidence.
- Calculate expected cost for approve, hold, and stop.
- Account for transaction context and cost differences so the agent does not rely on one fixed threshold for every transaction.
- Model hold/question behavior, customer verification, no-response timeout, and a second belief update from new evidence.
- Evaluate the decision process against the existing v2 / 35 test cases.
- Compare v2 evaluation results to the original 15-case, 73.3% historical baseline.
- Show evidence, prior belief, updated belief, expected costs, selected action, and follow-up belief updates in an inspectable report.

## Established Constraints And Decisions

- Preserve existing research work and evaluation history.
- The original 15-case evaluation is historical baseline evidence and MUST NOT be recreated.
- The existing v2/35-case work must be located, preserved, and used as the next evaluation source.
- Hidden states remain legitimate and fraudulent unless the project explicitly changes scope.
- Actions remain approve, hold/question, and stop unless the project explicitly changes scope.
- Hold/question is a first-class action for weak, missing, conflicting, or insufficient evidence.
- The agent should use evidence, belief updates, decision thresholds, expected cost, and new evidence/verification loops.
- Bayesian belief updating is the current belief-model direction.
- Expected-cost decision making is the current decision-rule direction.
- A single fixed threshold should not be assumed as the final decision policy.
- LLM confidence must not be treated as the actual transaction probability.
- Evidence extraction must not invent missing transaction information.
- Unestablished product goals, users, metrics, UI, deployment, data storage, and model configuration should remain open questions.
- Do not modify product code, research files, test cases, or `README.md` when only updating planning context.

## Open Questions

- Where exactly is the existing v2/35-case source stored?
- What is the exact format of the v2/35-case evaluation source and expected outputs?
- Who, if anyone, is the intended evaluator beyond the project builder/reviewer?
- Should the first runnable implementation be a script, CLI, notebook, API, or small web UI?
- Should priors, likelihoods, thresholds, and costs be hand-authored assumptions, derived from research, learned from data, or loaded from config?
- Which next evaluation target matters most: accuracy, false positives, false negatives, expected cost, consistency, explainability, or another metric?
- What should the timeout rule be when the customer does not respond?
- What role, if any, should an LLM have beyond evidence explanation or extraction?
