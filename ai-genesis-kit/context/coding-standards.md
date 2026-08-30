# Coding Standards

These conventions reflect the current repository: a small Python research prototype with Markdown planning and research notes. Update this file if the project becomes a web app, API service, notebook workflow, or packaged library.

## Python

- Target clear, standard-library Python first. Add dependencies only when a feature needs them.
- Keep probability, evidence, cost, and decision logic deterministic and easy to inspect.
- Use `dataclasses` or typed dictionaries for core data structures when the shape is stable.
- Prefer explicit names such as `fraud_probability`, `approval_cost`, and `evidence_likelihoods` over abbreviations.
- Keep functions small and focused: profile summarization, evidence extraction, belief update, cost calculation, and decision selection should be separate units.
- Do not let an LLM response stand in for a probability. LLM output may describe or extract evidence, but probability updates must come from explicit model inputs.

## File Organization

- Source code lives under `src/`.
- Use importable module names with underscores, not hyphens, for new Python files.
- Keep experiment fixtures under `experiments/` unless a later package layout introduces a dedicated `tests/` or `fixtures/` directory.
- Keep research notes in Markdown. Do not mix research prose into runtime modules.
- If the current `src/transaction-agent.py` becomes executable code, replace it with an importable module name such as `src/transaction_agent.py`.

## Data And Modeling

- Represent the hidden state explicitly as legitimate or fraudulent.
- Treat approve, hold, and stop as distinct actions. Hold is a first-class state, not a fallback label.
- Store assumptions where reviewers can see them: priors, likelihoods, evidence weights, action costs, and timeout behavior.
- Preserve intermediate values in decision reports so results can be audited.
- Handle missing, weak, and conflicting evidence deliberately. Do not silently convert missing evidence into fraud evidence.
- Keep customer verification as new evidence that flows back into the belief update step.

## Testing

No test runner is configured yet. Add pytest through `$tests` when logic-bearing implementation begins or when the project needs a formal test gate.

When tests are configured:

- Use pytest.
- Put tests close to the logic they verify, or under `tests/` if the project grows into a package.
- Test pure functions with fixed inputs and outputs: profile summaries, evidence extraction, Bayesian updates, expected-cost calculations, decision selection, and timeout handling.
- Include edge cases for missing fields, conflicting evidence, extreme transaction amounts, unusual times, no customer response, and equal expected costs.
- The test command documented in `AGENTS.md` is the source of truth once it exists.

## Verification

- Until a test runner exists, verify behavior by running the local Python command introduced by the relevant feature and checking the printed decision trace.
- If a feature adds tests, run the documented test command before review.
- If a feature adds packaging, linting, type checking, or CI, document the exact commands in `AGENTS.md`.
- Do not invent npm, Next.js, browser, or deployment commands for this repo unless the stack actually changes.

## Documentation

- Keep `README.md` as the project-facing explanation of the transaction agent.
- Keep `research-file.md` and `discussion-record.md` as research/history artifacts.
- Update `ai-genesis-kit/project-plan.md` when product direction, users, data, stack, monetization, UI/UX, or deployment changes.
- Update `ai-genesis-kit/build-plan.md` when feature order or scope changes.

## Comments

Write code that explains itself. Use comments sparingly for non-obvious modeling assumptions, mathematical decisions, or safety constraints. Do not add comments that restate the code.

## Writing

- Use ASCII punctuation in generated content.
- Do not use em dashes, en dashes, or the ellipsis character.
- Use `term - description` for concise separators.
