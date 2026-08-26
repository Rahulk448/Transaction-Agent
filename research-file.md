# Transaction Agent — Research

## 1. Problem Statement

A financial transaction arrives with incomplete information. The true state of the transaction is hidden: it is either **legitimate** or **fraudulent**.

The agent uses historical customer behavior and current transaction evidence to update its belief about the hidden state and choose one of three actions:

* Approve
* Hold
* Stop

If the available evidence is insufficient, the agent can hold the transaction, ask the customer for verification, and use the resulting information as new evidence.

---

## 2. Project Objective

Build a transaction decision agent that makes decisions under uncertainty using:

* Historical transaction data
* Customer profile information
* Current transaction evidence
* Bayesian belief updates
* Expected-cost decision making
* Additional evidence obtained through customer verification

The objective is to study a decision-making agent rather than a simple fraud/legitimate classifier.

---

## 3. Technical Terms

### Hidden State

The actual state of the transaction, which cannot be directly observed:

* Legitimate
* Fraudulent

### Historical Data

Previous customer transactions used to understand normal behavior.

Includes:

* Previous transaction amounts
* Fraud / legitimate labels
* Spending patterns

### Profile Summary

A summary of normal customer behavior derived from historical data.

Includes:

* Typical amounts
* Common merchants
* Typical transaction times
* Usual locations

### Evidence Extraction

The incoming transaction is compared with the customer's profile to identify relevant evidence.

Examples:

* Unusual amount
* Unusual merchant
* Unusual time
* Unusual location

### Prior Belief

The initial belief before considering the current transaction evidence:

```text
P(Legitimate) = 90%
P(Fraudulent) = 10%
```

### Bayesian Belief Engine

The belief engine combines the prior belief with the likelihood of the observed evidence and produces an updated belief:

```text
P(Fraudulent | Evidence)
P(Legitimate | Evidence)
```

When new evidence becomes available, the belief can be updated again.

### Expected Cost

Each possible action has a cost depending on the actual state of the transaction.

The decision engine uses:

* Updated probability
* Cost of each action
* Expected cost of each action

The action with the lowest expected cost is selected.

### Hold

The transaction is temporarily held when additional evidence is required.

The agent can ask the customer to verify the transaction.

### New Evidence

A customer response can provide additional evidence.

The new evidence is sent back to the Bayesian belief engine, allowing the agent to make a new decision.

### Pending / Timeout

If the customer does not respond to a verification request, the transaction remains pending until the defined timeout condition is reached.

---

## 4. Architecture

```text
Historical Data
      ↓
Profile Summary
      ↓
Evidence Extraction ← Transaction Arrives
      ↓
Bayesian Belief Engine
      ↓
Updated Probability
      ↓
Expected-Cost Decision Engine
      ↓
 ┌─────────┬─────────┬─────────┐
 │ Approve │  Hold   │  Stop   │
 └─────────┴─────────┴─────────┘
              ↓
         More Evidence
              ↓
       Ask / Verify Customer
          ↙          ↘
        Yes        No Response
         ↓              ↓
   New Evidence    Pending / Timeout
         ↓
Bayesian Belief Engine
```

---

## 5. Search Queries

* Bayesian belief updating for fraud detection
* Bayesian decision theory for transaction fraud
* expected cost fraud detection
* cost-sensitive fraud detection
* customer behavioral profiling fraud detection
* transaction fraud detection using historical behavior
* uncertainty-aware decision making
* LLM agents and uncertainty

---

## 6. Relevant Reddit Communities

* **r/MachineLearning** — machine learning and probabilistic decision systems
* **r/datascience** — applied data science and fraud-detection discussions
* **r/fintech** — financial technology and transaction-risk discussions
* **r/cybersecurity** — security and fraud-related discussions
* **r/learnmachinelearning** — machine-learning implementation and evaluation discussions

These communities can be used to find practical discussions and different approaches to fraud detection and decision systems.

---

## 7. Relevant X Accounts

* **Feedzai** — financial crime and transaction-risk technology
* **Sift** — fraud prevention and digital trust
* **Featurespace** — behavioral analytics and payment fraud prevention
* **Stripe** — payment infrastructure and fraud prevention

These accounts are relevant for following industry developments in transaction risk and fraud detection.

---

## 8. Five Useful Papers, Articles, Repositories, or Datasets

### 1. Cost Sensitive Credit Card Fraud Detection using Bayes Minimum Risk

Bahnsen et al., 2013.

Relevant to the project because it applies **Bayesian decision theory and cost-sensitive decision making** to credit-card fraud detection.

### 2. Fraud Detection Handbook

A reproducible open-source handbook covering machine learning for credit-card fraud detection, including sequential data, performance evaluation, model selection, and imbalanced learning.

### 3. IEEE-CIS Fraud Detection Dataset

A transaction-fraud dataset containing transaction and identity information with an `isFraud` target. It can be used for future evaluation beyond the current manually constructed test cases.

### 4. Uncertainty Quantification in LLM Agents: Foundations, Emerging Challenges, and Opportunities

Oh et al., ACL 2026.

Relevant to the agent component because it studies uncertainty estimation in interactive LLM agents and the way uncertainty changes during agent interaction.

### 5. Fraud Detection Handbook — Simulated Transaction Data

The Fraud Detection Handbook project provides simulated transaction datasets alongside its fraud-detection research and implementation resources.

---

## 9. Questions That I Want to Answer

1. How should historical transaction data be converted into a customer profile?

2. How should current transaction evidence affect the Bayesian belief?

3. How should multiple pieces of evidence be combined?

4. How should conflicting evidence affect the belief?

5. How should the costs of different decisions be represented?

6. When should the agent Hold instead of Approve or Stop?

7. How should customer verification affect the next belief update?

8. What should happen when the customer does not provide additional evidence?

9. What role should the LLM have in the agent?

10. How should the complete decision process be evaluated?

---

## 10. AI Prompts

### Evidence Extraction

```text
Given the customer's profile and the incoming transaction, identify the relevant evidence that differs from the customer's normal behavior.

Use only the information provided.
Do not invent information.
```

### Belief Update

```text
Given the prior belief and the extracted evidence, update the probability of the transaction being legitimate or fraudulent.

Use only the provided evidence.
```

### Decision

```text
Given the updated probability and the cost of each possible action, determine the expected cost of Approve, Hold, and Stop.

Select the action with the lowest expected cost.
```

### Customer Verification

```text
The transaction has been placed on Hold because more evidence is required.

Ask the customer to verify the transaction and use the response as additional evidence.
```

---

## 11. Important AI Errors

* Hallucinating transaction information that was not provided.
* Misinterpreting transaction evidence.
* Failing to compare the transaction with the customer's normal profile.
* Incorrectly updating the belief after new evidence.
* Treating LLM confidence as the actual probability.
* Making a decision without considering expected cost.
* Ignoring new evidence obtained through customer verification.
* Producing inconsistent decisions from similar evidence.

---

## 12. Current Evaluation

The prototype has been evaluated using **15 transaction test cases**.

```text
Correct decisions: 11 / 15
Accuracy: 73.3%
```

This is the current baseline for evaluating the decision process and identifying where the agent makes incorrect decisions.

---

## 13. Research Direction

The final architecture treats transaction processing as a **sequential decision problem under uncertainty**.

The core loop is:

```text
Transaction
    ↓
Evidence Extraction
    ↓
Belief Update
    ↓
Expected Cost
    ↓
Decision
    ↓
More Evidence if Required
    ↓
Belief Update
```

The central research question is:

> Can a transaction agent make more consistent decisions by maintaining an explicit belief about the hidden state, updating that belief with new evidence, and selecting actions according to expected cost?
