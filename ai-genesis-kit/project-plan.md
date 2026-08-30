# Project Plan

## 1. Problem - What problem are we solving?

A financial transaction arrives with incomplete information, and the true state is hidden: the transaction is either legitimate or fraudulent. The project studies how a transaction decision agent can use evidence, belief updates, decision thresholds, expected cost, and customer verification to choose between approve, hold, and stop.

The goal is not to build a simple fraud/legitimate classifier. The project is about sequential decision making under uncertainty.

## 2. Users - Who is this for?

The established user is the project builder/reviewer evaluating the Transaction Agent research prototype.

Possible future users, such as fintech researchers, fraud-risk analysts, or engineers, are not yet established as product users and should remain an open question.

## 3. Completed Research Work

- Selected the Transaction Agent problem.
- Defined the hidden states as legitimate and fraudulent.
- Defined the main actions: approve, hold/question, and stop.
- Established that hold is a real action/state for weak, missing, conflicting, or insufficient evidence.
- Defined the core loop: observe transaction evidence, update belief, evaluate decision cost, choose an action, and update belief again if new evidence arrives.
- Identified historical behavior, customer profile, transaction amount, time, merchant history, recent activity, and location as relevant evidence areas.
- Identified Bayesian belief updates as the intended belief model direction.
- Identified expected-cost decision making as central to choosing between approve, hold, and stop.
- Recorded human feedback that a single fixed threshold is likely insufficient because transaction context and cost of wrong decisions matter.
- Recorded human feedback that low confidence should not be collapsed into approve or stop.
- Completed an initial 15-case evaluation with 11 correct decisions out of 15, about 73.3% accuracy.
- Created existing v2 / 35-test-case work that should be preserved and used as the next evaluation source.
- The original 15-case evaluation is historical baseline evidence and must not be recreated as new work.

## 4. Features - What does the MVP need?

- Preserve the existing research direction and evaluation history.
- Represent transactions, customer profiles, evidence signals, beliefs, action costs, decisions, and verification responses.
- Convert historical transaction behavior into a customer profile.
- Extract evidence by comparing an incoming transaction against the customer profile.
- Update legitimate/fraudulent belief from explicit evidence and prior assumptions.
- Calculate expected costs for approve, hold, and stop.
- Support hold/question behavior when evidence is weak, missing, conflicting, or too costly to decide immediately.
- Use customer verification or no-response/timeout as additional evidence for a follow-up belief update.
- Evaluate the decision process against the existing v2 / 35 test cases.
- Keep the original 15-case, 73.3% result as the baseline for comparison, not as a fixture set to recreate.

## 5. Data - What are we storing?

No durable database is established.

Current and planned project data should remain local/research-oriented unless a later decision changes that:

- Historical transactions
- Incoming transactions
- Customer profile summaries
- Evidence signals
- Prior probabilities
- Evidence likelihoods or evidence weights
- Updated legitimate/fraudulent beliefs
- Action costs
- Approve/hold/stop decisions
- Customer verification responses
- Pending/timeout outcomes
- 15-case baseline evaluation result: 11/15 correct, about 73.3%
- Existing v2 / 35 test cases and their evaluation outputs

The exact storage format for v2 / 35 test cases is an open question unless already present in a source file not found during this adoption pass.

## 6. Tech - What stack are we using?

The current repository is a Python research/prototype project with Markdown documentation. No package manager, dependency file, app framework, lint command, test runner, CI workflow, database, or deployment target is currently established.

Use standard-library Python first unless a later feature justifies dependencies. Add pytest only through the explicit `$tests` workflow if the project needs a formal test gate.

## 7. Monetize - How will this make money?

Not established. Leave monetization as an open question.

## 8. UI/UX - How should this look and feel?

No UI is established.

For the current project, the useful experience is a transparent research/prototype interface: clear inputs, visible evidence extraction, belief updates, expected-cost calculations, final approve/hold/stop decisions, and evaluation comparison against the 15-case baseline and v2 / 35 test cases.

Whether this becomes a CLI, notebook, API, or web UI is an open question.

## 9. Deployment - Where and how will this ship?

Deployment is not established. The project currently runs, or is expected to run, locally as a Python research prototype.

There is no known build command, start command, health check path, domain, database, worker, cron job, environment variable, Render config, or Vercel config.

## Open Questions

- Where is the existing v2 / 35-test-case source stored, if not in the currently visible repository files?
- Who is the intended evaluator beyond the project builder/reviewer?
- Should the first runnable version be a CLI, notebook, API, or small web UI?
- Should priors, likelihoods, thresholds, and costs be hand-authored assumptions, derived from research, learned from data, or loaded from config?
- Which evaluation target matters most next: accuracy, false positives, false negatives, expected cost, consistency, explainability, or another metric?
- What should the timeout rule be when the customer does not respond?
- What role, if any, should an LLM have beyond evidence explanation or extraction?
