# Current Feature

## Title

Domain model

## Type

Feature

## Build-plan item

11. **Domain model** - add Python data structures for transactions, customer profiles, evidence signals, beliefs, action costs, decisions, verification responses, and pending/timeout outcomes

## Goal

Create the first importable Python domain model for the Transaction Agent so later profile summary, evidence extraction, belief update, expected-cost decision, hold/verification, and trace-output work can share stable typed structures.

The model should make the core research concepts explicit:

- hidden states: legitimate and fraudulent
- actions: approve, hold/question, and stop
- incoming transactions
- historical transaction records for customer profiles
- evidence signals without invented missing data
- legitimate/fraudulent beliefs
- action costs
- decisions and expected costs
- customer verification responses
- pending and timeout outcomes

## Out of scope

- Do not implement profile summarization.
- Do not implement evidence extraction rules.
- Do not implement Bayesian belief updates.
- Do not implement expected-cost decision selection.
- Do not implement the hold/verification loop.
- Do not read or modify `experiments/transaction_agent_test_cases_v2.csv`.
- Do not recreate the original 15-case evaluation.
- Do not add a package manager, external dependency, dev server, CI workflow, or deployment setup.

## Build steps

- [x] 1. Replace the placeholder `src/transaction-agent.py` with an importable module path.

  Rename or supersede the hyphenated placeholder with `src/transaction_agent.py` so future Python code can import the domain model normally. Keep the existing placeholder from becoming executable product logic.

  **Done when** `src/transaction_agent.py` exists, can be imported by Python, and no runtime behavior beyond definitions has been added.

  **Evidence** Completed import verification in Git Bash using the installed Python 3.14 executable:

  ```bash
  python -c "import sys; sys.path.insert(0, 'src'); import transaction_agent; print('ok')"
  ```

  Output:

  ```text
  ok
  ```

- [ ] 2. Define core enumerations for states, actions, evidence, verification, and outcomes.

  Add explicit enum values for legitimate/fraudulent hidden states, approve/hold/stop actions, evidence direction or strength as needed by later extraction, verification response values, and pending/timeout outcomes.

  **Done when** the domain module exposes named enum members for the established states and actions, plus typed values for verification and timeout handling.

- [ ] 3. Add transaction and historical profile data structures.

  Use standard-library dataclasses for incoming transactions and historical transactions with fields for identifiers, customer id, amount, merchant, timestamp, location, and optional contextual fields where the existing research identifies them. Missing information must be representable as `None` or an explicit optional value.

  **Done when** callers can construct an incoming transaction and a historical transaction without inventing unavailable amount, merchant, time, location, or recent-activity details.

- [ ] 4. Add profile, evidence, belief, and cost data structures.

  Define structures for customer profile summaries, evidence signals, belief probabilities, and action costs. Include lightweight validation where it directly protects the model, such as probability bounds and non-negative costs.

  **Done when** the module can represent a prior belief, an updated belief, explicit evidence signals, and per-action costs without performing the later update or decision calculations.

- [ ] 5. Add decision and verification result data structures.

  Define structures for selected decisions, expected-cost snapshots, customer verification responses, pending review state, timeout/no-response outcome, and final follow-up outcome.

  **Done when** the model can represent approve, hold/question, stop, pending verification, received verification, timeout/no-response, and a final decision trace container.

- [ ] 6. Add minimal import smoke verification.

  Add a small standard-library Python entry point or command-compatible smoke check only if needed to prove the module imports and representative objects can be constructed. Do not add pytest in this feature because the test gate is not yet on.

  **Done when** a documented Python command can import the module and instantiate representative domain objects without errors.

## Testing

The test gate is not on. No pytest coverage is expected for this feature.

If the project later enables tests through `$tests`, this domain model should receive focused tests for enum values, probability validation, non-negative cost validation, optional missing evidence fields, and representative construction of transaction, belief, cost, decision, verification, and timeout objects.

## Verify

Use standard-library Python only.

Required evidence for implementation review:

```powershell
python -c "import sys; sys.path.insert(0, 'src'); import transaction_agent; print('ok')"
```

If the implementation adds a smoke-construction command, run that exact command too and record the output in the review packet.
