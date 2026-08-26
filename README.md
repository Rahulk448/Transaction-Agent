# Transaction Agent

A small probability-based AI agent that makes transaction decisions under uncertainty.

## Problem

A financial transaction arrives with incomplete information. The agent must decide whether to approve, question/hold, or stop the transaction because the true legitimacy of the transaction is not directly known.

## How the Agent Thinks

The agent follows a simple decision process:

Transaction  
↓  
Observe available evidence  
↓  
Estimate belief about the hidden state  
↓  
Receive additional evidence  
↓  
Update belief  
↓  
Consider the cost of each possible decision  
↓  
Choose an action

### Hidden State

For the initial version, the hidden state is simplified to:

- Legitimate
- Fraudulent

### Observable Evidence

The initial model considers information such as:

- Transaction amount
- Transaction time
- Merchant history
- Recent transaction activity

These features may change as research and human discussions provide new information.

### Actions

The agent can:

1. Approve
2. Question / Hold
3. Stop

## Probability Model

The agent begins with a prior belief about the hidden state.

For example, an initial simulation may use:

- Legitimate: 90%
- Fraudulent: 10%

These numbers are currently treated as assumptions and will be replaced or justified using appropriate evidence.

When new evidence arrives, the agent updates its belief and uses the updated probability to make a decision.

## Decision Costs

The agent does not treat every mistake equally.

For example:

- Approving a fraudulent transaction can cause financial loss.
- Stopping a legitimate transaction can cause customer friction.
- Holding a transaction can create verification cost and delay.

The experiment will investigate how these costs should affect the decision rule.

---

## Project Stage

Current Stage: **Stage 3 — Research and Problem Refinement**

The project is currently focused on testing the assumptions behind the transaction decision problem and turning the initial agent model into something that can eventually be implemented and evaluated.

### Completed

* Selected the Transaction Agent problem.
* Defined the hidden states as legitimate or fraudulent.
* Defined the initial observable transaction information.
* Defined the available actions: approve, question/hold, or stop.
* Defined the basic probability-based decision process.
* Identified that new evidence should update the agent's belief rather than being treated as an isolated signal.
* Identified decision cost as an important part of choosing an action.
* Started human outreach and collected external feedback on the problem.
* Recorded the initial research and discussion findings.

### Current Work

* Refine which transaction signals should affect the agent's belief.
* Examine how uncertainty and new evidence should change the decision.
* Investigate whether a single fixed probability threshold is appropriate for every transaction.
* Consider transaction context and decision costs when choosing between approve, hold, and stop.
* Turn the refined decision process into a small testable agent.

### Next Stage

Stage 4 — **Probability Model and Decision Rule**

The next stage will turn the research findings into an explicit probability model and decision rule, followed by testable transaction cases.
