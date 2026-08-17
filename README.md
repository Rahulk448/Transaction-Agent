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

**Current Stage: Stage 3 — Research and Problem Refinement**

The project is currently focused on researching the transaction decision problem, identifying useful evidence, and challenging the initial assumptions about the agent.

### Completed

- Selected the Transaction Agent problem.
- Defined the hidden states as legitimate or fraudulent.
- Defined the initial observable transaction information.
- Defined the available actions: approve, question/hold, or stop.
- Defined the basic probability-based decision process.
- Started human outreach on Reddit.
- Created the initial research and discussion records.

### Current Work

- Research transaction fraud decision signals.
- Continue human discussions with practitioners.
- Examine assumptions about evidence, uncertainty, and decision costs.
- Refine the probability model.

### Next Stage

**Stage 4 — Probability Model and Decision Rule**

The next stage will turn the research findings into an explicit probability model, decision thresholds, and testable cases.

