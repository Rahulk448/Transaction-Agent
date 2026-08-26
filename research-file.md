# Transaction Decision Agent — Research

## 1. Problem Statement

A financial transaction arrives with incomplete and uncertain information. The true legitimacy of the transaction is a hidden state that cannot be observed directly at decision time.

The agent must use the available transaction information and evidence to estimate how likely the transaction is to be legitimate or fraudulent and then choose an appropriate action.

The possible actions are:

* **Approve** — allow the transaction.
* **Question / Hold** — request or wait for additional evidence before deciding.
* **Stop** — reject or block the transaction when the estimated risk is sufficiently high.

The main challenge is not simply classifying a transaction as fraud or legitimate. The agent must make a **decision under uncertainty**, where different mistakes have different consequences.

---

## 2. Project Objective

The objective is to explore how an agent can make transaction decisions under uncertainty using:

* Probability
* Evidence
* Belief updates
* Decision thresholds
* Decision costs
* Risk
* Hidden states
* Sequential reasoning
* Human or external feedback

The project investigates whether an agent can update its belief about a transaction as new evidence becomes available instead of making a single fixed classification.

The system is designed as a hybrid decision agent:

1. The **LLM** handles semantic interpretation of transaction information and evidence.
2. The **probabilistic decision layer** represents belief about the hidden state.
3. The **decision layer** compares the resulting belief against predefined decision criteria.
4. The agent selects **approve, question/hold, or stop**.
5. The result can be evaluated against the known label for testing.

The current prototype has been evaluated using **15 test cases**, with the outputs manually evaluated and labeled.

Current result:

* Correct decisions: **11/15**
* Accuracy: **73.3%**

This evaluation is a baseline for further improvement rather than a claim of production-level fraud detection performance.

---

## 3. Technical Terms

### Hidden State

The actual legitimacy of a transaction that is not directly observable.

Example:

* Legitimate
* Fraudulent

The agent observes evidence about the transaction but does not directly observe the true state at decision time.

### Observation / Evidence

Information available to the agent that provides evidence about the hidden state.

Examples:

* Transaction amount
* Transaction location
* Previous transaction behavior
* Account history
* Device information
* Time of transaction
* Unusual transaction patterns
* Additional information supplied after questioning

### Belief

The agent's current probability estimate about the hidden state.

Example:

```text
P(Fraud | current evidence) = 0.72
P(Legitimate | current evidence) = 0.28
```

The belief can change when new evidence arrives.

### Belief Update

The process of changing the current probability after receiving new evidence.

Conceptually:

```text
Prior belief
     ↓
New evidence
     ↓
Updated belief
     ↓
Decision
```

Bayesian reasoning provides a formal framework for updating beliefs when new evidence is observed.

### Prior Probability

The initial belief about the likelihood of fraud before considering the current evidence.

### Posterior Probability

The updated belief after incorporating available evidence.

### Decision Threshold

A boundary used to determine which action should be taken based on the estimated risk.

Example:

```text
Low risk       → Approve
Medium risk    → Question / Hold
High risk      → Stop
```

The exact thresholds are part of the current prototype's decision design.

### False Positive

A legitimate transaction incorrectly treated as fraudulent.

Example:

```text
Legitimate transaction → Stop
```

This can create customer friction and lost legitimate business.

### False Negative

A fraudulent transaction incorrectly treated as legitimate.

Example:

```text
Fraudulent transaction → Approve
```

This can result in financial loss.

### Cost-Sensitive Decision Making

Different errors have different costs.

For example:

```text
Cost(false positive) ≠ Cost(false negative)
```

Therefore, the best decision is not necessarily the one with the highest raw classification accuracy.

### Uncertainty

The degree to which the available evidence is insufficient to confidently determine the true state.

High uncertainty can justify the **question/hold** action rather than immediately approving or stopping a transaction.

### Human-in-the-Loop

A system where a human can provide additional evidence, feedback, or a final decision when the automated system is uncertain.

This is particularly relevant to the question/hold state.

### Class Imbalance

Fraudulent transactions are normally much rarer than legitimate transactions.

This means raw accuracy can be misleading when evaluating real fraud detection systems.

### Calibration

How accurately predicted probabilities correspond to actual observed frequencies.

A system predicting 0.8 fraud probability should ideally be correct about 80% of the time among comparable cases.

### Decision Policy

The mapping from the agent's current belief and available information to an action.

```text
Belief + Evidence + Costs
          ↓
     Decision Policy
          ↓
Approve / Hold / Stop
```

### LLM

The language model is used as part of the agent rather than being treated as the entire decision mechanism.

Its role is primarily to interpret unstructured information, reason over evidence, and communicate the decision.

The mathematical decision mechanism remains separate from the language model.

---

## 4. Search Queries

The following search queries are relevant to researching and improving the transaction agent:

```text
financial transaction fraud detection machine learning
cost sensitive credit card fraud detection Bayesian decision theory
fraud detection decision thresholds false positives false negatives
Bayesian decision making under uncertainty
Bayesian belief update sequential evidence
probabilistic decision making agents
uncertainty quantification LLM agents
LLM agents decision making under uncertainty
human in the loop fraud detection
human feedback fraud detection machine learning
transaction fraud detection class imbalance
fraud detection model calibration
fraud detection concept drift
real time transaction fraud detection
financial fraud detection datasets
```

---

## 5. Verified / Relevant Reddit Communities

These communities are relevant for researching fraud detection, machine learning, AI agents, and financial technology.

### 1. r/MachineLearning

Useful for:

* Machine learning research
* Probabilistic models
* AI decision systems
* Model evaluation
* Uncertainty estimation

There are existing discussions specifically around fraud detection and imbalanced fraud datasets.

### 2. r/datascience

Useful for:

* Applied fraud detection
* Feature engineering
* Model evaluation
* Class imbalance
* Real-world data science problems

Fraud detection and credit-risk modelling have been directly discussed in the community.

### 3. r/fintech

Useful for:

* Financial technology
* Payment systems
* Transaction monitoring
* Real-time fraud detection
* Industry implementation problems

Recent discussions include practical problems around building real-time fraud detection systems and balancing fraud prevention against false positives.

### 4. r/cybersecurity

Useful for:

* Fraud patterns
* Security signals
* Transaction monitoring
* Abuse detection
* Risk indicators

### 5. r/learnmachinelearning

Useful for:

* Understanding ML fundamentals
* Probability and classification
* Model evaluation
* Practical implementation questions
* Learning resources

---

## 6. Relevant X Accounts

Relevant accounts and organizations to follow for financial fraud, transaction risk, machine learning, and AI research:

* **@Feedzai** — financial crime and transaction-risk research
* **@siftscience / @GetSift** — digital trust, fraud detection and machine learning
* **@sardine** — fraud prevention and financial infrastructure
* **@chainalysis** — financial crime, blockchain analytics and investigations
* **@StripeDev** — payment infrastructure and developer discussions
* **@mariotelfig** — machine learning research and Feedzai research
* **@jtascensao** — machine learning research and Feedzai-related work

These accounts can be used to monitor industry approaches, research directions, and practical transaction-risk problems.

---

## 7. Five Useful Papers, Articles, Repositories, or Datasets

### 1. Cost Sensitive Credit Card Fraud Detection using Bayes Minimum Risk

**Authors:** Alejandro Correa Bahnsen et al.
**Conference:** ICMLA 2013

This is particularly relevant to the transaction agent because it connects fraud detection with **Bayesian decision theory and different costs for different decisions**.

The important idea for this project is that the optimal decision should consider the cost of mistakes rather than only classification accuracy.

DOI:

```text
10.1109/ICMLA.2013.68
```

---

### 2. Financial Fraud Detection Based on Machine Learning: A Systematic Literature Review

**Journal:** Applied Sciences
**2022**

This review covers machine-learning approaches to financial fraud detection and discusses commonly used algorithms, datasets, evaluation metrics, and limitations.

Useful for understanding the broader fraud-detection landscape and positioning this project relative to conventional ML approaches.

---

### 3. Fraud Detection Handbook

**Repository / Project:** Fraud Detection Handbook

This is a reproducible open-source resource covering practical fraud-detection methodology, including:

* Transaction data
* Class imbalance
* Feature engineering
* Machine learning
* Evaluation
* Interpretability

It is especially useful for comparing the prototype agent with conventional fraud-detection pipelines.

Repository:

```text
fraud-detection-handbook.github.io
```

---

### 4. Amazon Fraud Dataset Benchmark

**Repository:** amazon-science/fraud-dataset-benchmark

A benchmark containing multiple fraud-related datasets, including:

* IEEE-CIS Fraud Detection
* Credit Card Fraud Detection
* Fraud Ecommerce
* Simulated Credit Card Transactions

The benchmark is useful for future evaluation beyond the current 15 manually constructed test cases.

Repository:

```text
github.com/amazon-science/fraud-dataset-benchmark
```

---

### 5. Uncertainty Quantification in LLM Agents: Foundations, Emerging Challenges, and Opportunities

**ACL 2026**

This work is relevant to the agent side of the project because it examines uncertainty specifically in interactive LLM agents.

It highlights challenges around:

* Estimating uncertainty
* Heterogeneous information
* Changing uncertainty during interaction
* Evaluating uncertainty in agent systems

This connects directly to the project's idea of an agent receiving evidence, updating its belief, and making decisions under uncertainty.

---

## 8. Questions That I Want to Answer

1. How should an agent represent the hidden legitimacy state of a transaction?

2. How should the initial probability of fraud be determined?

3. How should new transaction evidence change the agent's belief?

4. Should every piece of evidence have the same influence on the belief?

5. How should conflicting evidence be handled?

6. When should the agent ask a question instead of approving or stopping?

7. How should decision thresholds be selected?

8. How should the costs of false positives and false negatives affect the decision?

9. Is accuracy an appropriate primary metric for this type of system?

10. Should precision, recall, F1, confusion matrices, expected cost, and calibration also be evaluated?

11. How can the system determine whether it is sufficiently uncertain to defer the decision?

12. What role should the LLM have in the decision pipeline?

13. How can the mathematical decision layer prevent the LLM from making arbitrary decisions?

14. How should human feedback be incorporated into future belief updates?

15. How can the agent be evaluated on a larger and more realistic transaction dataset?

16. How does the agent compare against a simple rule-based baseline?

17. How does the agent compare against a conventional ML classifier?

18. Can the agent improve its decisions after receiving additional evidence?

19. How should the system handle changing fraud patterns over time?

20. How can the decision process remain explainable and auditable?

---

## 9. AI Prompts

### Transaction Evaluation Prompt

```text
You are evaluating a financial transaction under uncertainty.

Determine the likelihood that the transaction is legitimate or fraudulent using only the information provided.

Identify:
1. Evidence supporting legitimacy.
2. Evidence supporting fraud.
3. Missing or uncertain information.
4. Your current belief about the transaction.
5. Whether additional information is required.

Do not assume information that is not provided.
```

### Evidence Update Prompt

```text
The transaction has received new evidence.

Compare the new evidence with the previous belief.

Explain whether the evidence:
- increases the probability of fraud,
- decreases the probability of fraud, or
- does not meaningfully change the belief.

Then provide the updated assessment and explain why.
```

### Decision Prompt

```text
Using the current transaction evidence and estimated fraud probability, select exactly one action:

APPROVE
QUESTION / HOLD
STOP

Give a short explanation based on the available evidence and uncertainty.

Do not invent missing information.
```

---

## 10. Important AI Errors

### 1. Hallucinating Transaction Information

The LLM may invent details that were never provided.

Example:

```text
Transaction location: India
```

when no location was actually supplied.

This can incorrectly influence the decision.

---

### 2. Overconfidence

The LLM may produce a very confident answer even when the evidence is weak.

This is particularly dangerous for a system that is explicitly designed to operate under uncertainty.

---

### 3. Ignoring Missing Evidence

The model may behave as though missing information is negative or positive evidence.

Missing information should normally remain uncertain rather than automatically being treated as suspicious.

---

### 4. Threshold Inconsistency

The LLM may give similar transaction probabilities but choose different actions in different cases.

The decision layer therefore needs consistent decision rules.

---

### 5. Confusing Probability With Decision

A high probability of fraud does not automatically define the correct action unless the costs and thresholds are considered.

For example:

```text
P(Fraud) = 0.70
```

does not by itself prove that the transaction must be stopped.

---

### 6. Anchoring on One Suspicious Signal

The model may focus heavily on one unusual feature while ignoring the rest of the evidence.

The agent should consider the complete evidence set.

---

### 7. Failure to Update Beliefs

The agent may produce a new answer without properly incorporating newly supplied evidence.

A major research objective is to verify whether the belief actually changes when evidence changes.

---

### 8. Treating LLM Reasoning as Ground Truth

An LLM explanation is not automatically a mathematically valid probability update.

The project therefore separates:

```text
LLM interpretation
        ↓
Evidence
        ↓
Probabilistic belief
        ↓
Decision policy
        ↓
Action
```

---

## 11. Current Prototype Evaluation

The prototype has already been tested using **15 transaction test cases**.

Each test case was evaluated and labeled according to whether the agent's resulting decision was correct.

Current baseline:

| Metric              | Result |
| ------------------- | -----: |
| Test cases          |     15 |
| Correct decisions   |     11 |
| Incorrect decisions |      4 |
| Accuracy            |  73.3% |

The 15 cases should be treated as an initial evaluation set rather than a statistically representative fraud dataset.

The next stage should focus on understanding **why the four incorrect decisions occurred**, rather than simply increasing the number of test cases.

Important evaluation questions include:

* Was the evidence interpreted incorrectly?
* Was the belief update incorrect?
* Was the decision threshold inappropriate?
* Did the LLM hallucinate information?
* Was the transaction genuinely ambiguous?
* Was the ground-truth label itself clear?
* Did the agent choose the wrong action despite having a reasonable belief?

---

## 12. Research Direction

The main research direction is to move from a simple transaction classifier toward a **decision-making agent under uncertainty**.

The intended architecture is:

```text
Transaction
     ↓
Evidence Extraction
     ↓
Current Belief
     ↓
New Evidence
     ↓
Belief Update
     ↓
Risk / Expected Cost
     ↓
Decision Policy
     ↓
┌──────────┬────────────────┬─────────┐
│ APPROVE  │ QUESTION/HOLD  │  STOP   │
└──────────┴────────────────┴─────────┘
```

The central research question is:

> Can an agent make better and more explainable transaction decisions by explicitly representing uncertainty, updating beliefs as evidence changes, and choosing actions according to decision costs rather than relying only on a binary classification?

---

## 13. Initial Findings

The current prototype demonstrates that an LLM can be incorporated into a transaction decision process, but the **73.3% baseline accuracy** also shows that the current approach is not yet reliable enough to treat the agent as a final decision-maker.

The most important areas for improvement are:

* Consistent probability estimation
* Evidence weighting
* Belief updates
* Decision thresholds
* Cost-sensitive decisions
* Handling uncertainty
* Reducing hallucination
* Better evaluation methodology
* Comparison with conventional ML and rule-based baselines
* Larger and more realistic datasets

The project should therefore focus less on making the LLM "more confident" and more on making the **decision process more consistent, measurable, and auditable**.
