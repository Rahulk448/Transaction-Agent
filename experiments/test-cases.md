# Transaction Agent — Evaluation Test Cases & Benchmark Report

This document records the evaluation benchmark for the Transaction Agent.

---

## 1. Evaluation Datasets

The project maintains two distinct evaluation records:

1. **Historical 15-Case Baseline**:
   - Initial early synthetic evaluation prior to full end-to-end integration.
   - Result: **11 / 15 correct (73.3%)**.
   - Preserved as a historical baseline; not to be confused with or replaced by the V2 evaluation.

2. **V2 Frozen Benchmark Dataset (`experiments/transaction_agent_test_cases_v2.csv`)**:
   - 35 scenario-level evaluation cases.
   - 22 Legitimate ground-truth, 13 Fraudulent ground-truth.
   - Expected action distribution: 12 APPROVE, 15 HOLD, 8 STOP.
   - **This CSV file is strictly frozen and read-only.**

---

## 2. Evaluation Methodology & Ground-Truth Blindness

Evaluation was executed using the automated runner [`src/evaluate_v2.py`](../src/evaluate_v2.py).

### Ground-Truth Separation
During the evaluation:
- The agent was **completely blind** to `Hidden State` and `Expected Agent Action`.
- Evidence extraction consumed only the scenario feature fields:
  - `Amount (INR)`
  - `Merchant`
  - `Time`
  - `Location`
  - `Historical Behavior`
  - `Evidence Notes`
- The decision engine computed the lowest expected cost using `DEFAULT_COST_MODEL` (`approve_legitimate=0.0`, `approve_fraudulent=10.0`, `hold_legitimate=2.0`, `hold_fraudulent=2.0`, `stop_legitimate=8.0`, `stop_fraudulent=0.0`).
- Ground-truth actions and hidden states were compared only after the decision was finalized.

---

## 3. 35-Case V2 Evaluation Results

```text
Total Cases: 35
Matched Expected Action: 22 / 35
Overall Agreement: 62.9%
```

### Action Breakdown:
- **Agent Selected Actions**: 21 APPROVE, 9 HOLD, 5 STOP
- **Expected Benchmark Actions**: 12 APPROVE, 15 HOLD, 8 STOP

### Full 35-Case Result Table

| TC | Extracted Evidence | Final $P(\text{Fraud})$ | Cost (App) | Cost (Hld) | Cost (Stp) | Agent Action | Expected Action | Hidden State | Result |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TC01** | All 4 consistent | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC02** | All 4 anomalous | 0.800 | 8.00 | 2.00 | 1.60 | **STOP** | STOP | Fraudulent | **MATCH** |
| **TC03** | Modest amount, consistent history | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC04** | Large amount + 3 consistent | 0.066 | 0.66 | 2.00 | 7.47 | **APPROVE** | HOLD | Legitimate | MISMATCH |
| **TC05** | Large amount + 3 consistent | 0.066 | 0.66 | 2.00 | 7.47 | **APPROVE** | HOLD | Fraudulent | MISMATCH |
| **TC06** | 3:30am time explained by history | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC07** | Unusual time (3:30am) + 3 consistent | 0.199 | 1.99 | 2.00 | 6.40 | **APPROVE** | HOLD | Legitimate | MISMATCH |
| **TC08** | New merchant, unusual time, high amount | 0.509 | 5.09 | 2.00 | 3.93 | **HOLD** | STOP | Fraudulent | MISMATCH |
| **TC09** | Low amount ₹600 + unfamiliar merchant | 0.092 | 0.92 | 2.00 | 7.27 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC10** | Unfamiliar merchant + large amount | 0.147 | 1.47 | 2.00 | 6.82 | **APPROVE** | HOLD | Legitimate | MISMATCH |
| **TC11** | Unfamiliar merchant + large amount | 0.147 | 1.47 | 2.00 | 6.82 | **APPROVE** | HOLD | Fraudulent | MISMATCH |
| **TC12** | Different city explained by history | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC13** | Unusual location + 3 consistent | 0.138 | 1.38 | 2.00 | 6.90 | **APPROVE** | HOLD | Legitimate | MISMATCH |
| **TC14** | High amount, new merchant, foreign city | 0.400 | 4.00 | 2.00 | 4.80 | **HOLD** | STOP | Fraudulent | MISMATCH |
| **TC15** | Periodic ₹60,000 recurring amount | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC16** | 4 anomalies, ₹60,000 unfamiliar | 0.800 | 8.00 | 2.00 | 1.60 | **STOP** | STOP | Fraudulent | **MATCH** |
| **TC17** | 2 anomalies: unusual time & location | 0.490 | 4.90 | 2.00 | 4.08 | **HOLD** | HOLD | Legitimate | **MATCH** |
| **TC18** | 2 anomalies: unusual time & location | 0.490 | 4.90 | 2.00 | 4.08 | **HOLD** | HOLD | Fraudulent | **MATCH** |
| **TC19** | Daily small routine purchase | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC20** | Rapid succession (3 txs in 6 mins) | 0.092 | 0.92 | 2.00 | 7.27 | **APPROVE** | STOP | Fraudulent | MISMATCH |
| **TC21** | 5am time partially supported | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC22** | Moderate amount anomaly (₹9000) | 0.066 | 0.66 | 2.00 | 7.47 | **APPROVE** | HOLD | Legitimate | MISMATCH |
| **TC23** | Extreme ₹110,000 + 3 anomalies | 0.800 | 8.00 | 2.00 | 1.60 | **STOP** | STOP | Fraudulent | **MATCH** |
| **TC24** | Routine recurring monthly amount | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC25** | Unfamiliar merchant (same category) | 0.092 | 0.92 | 2.00 | 7.27 | **APPROVE** | HOLD | Legitimate | MISMATCH |
| **TC26** | Unfamiliar merchant (same category) | 0.092 | 0.92 | 2.00 | 7.27 | **APPROVE** | HOLD | Fraudulent | MISMATCH |
| **TC27** | Low amount ₹450 keeps exposure low | 0.092 | 0.92 | 2.00 | 7.27 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC28** | New merchant + different city | 0.280 | 2.80 | 2.00 | 5.76 | **HOLD** | HOLD | Legitimate | **MATCH** |
| **TC29** | ₹38,000 + 3 anomalies | 0.800 | 8.00 | 2.00 | 1.60 | **STOP** | STOP | Fraudulent | **MATCH** |
| **TC30** | Minor time deviation within spread | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC31** | New merchant + different city | 0.280 | 2.80 | 2.00 | 5.76 | **HOLD** | HOLD | Legitimate | **MATCH** |
| **TC32** | New merchant + different city | 0.280 | 2.80 | 2.00 | 5.76 | **HOLD** | HOLD | Fraudulent | **MATCH** |
| **TC33** | ₹150,000 extreme + all 4 anomalies | 0.800 | 8.00 | 2.00 | 1.60 | **STOP** | STOP | Fraudulent | **MATCH** |
| **TC34** | Merchant is sub-brand of usual | 0.040 | 0.40 | 2.00 | 7.68 | **APPROVE** | APPROVE | Legitimate | **MATCH** |
| **TC35** | Sparse profile (<5 prior transactions) | 0.092 | 0.92 | 2.00 | 7.27 | **APPROVE** | HOLD | Legitimate | MISMATCH |

---

## 4. Failure Categorization (13 Mismatches)

### Category A: Prototype Assumption / Conditional Independence Dilution (7 cases)
* **Cases**: `TC04`, `TC05`, `TC07`, `TC10`, `TC11`, `TC13`, `TC22`
* **Mechanism**: In `TC04` and `TC05`, an amount of ₹15,000 is 4× the historical maximum. Human benchmark intuition flags this as an anomaly requiring verification (HOLD). However, the prototype treats `large_amount` with likelihood ratio $\frac{0.30}{0.20} = 1.5$. Multiplying this with three consistent signals ($0.824 \times 0.778 \times 0.667 \approx 0.428$) yields a total factor of $0.642 < 1.0$, which dilutes the fraud probability from $10\%$ down to $6.6\%$, falling short of the $20\%$ HOLD threshold.
* **Decision Boundary Case**: In `TC07`, $P(\text{Fraud}) = 19.94\%$, missing the $20.0\%$ boundary by only $0.06$ percentage points.

### Category B: Decision Boundary / Evaluation-Set Behavior (2 cases)
* **Cases**: `TC08`, `TC14`
* **Mechanism**: The benchmark expected STOP, but the agent chose HOLD. With 3 anomalies and 1 consistent signal, posterior fraud probability reached $40.0\%–50.9\%$. In expected-cost decision theory, STOP requires $P(\text{Fraud}) > 75\%$. At $40\%–51\%$, the expected cost of HOLD ($2.0$) is strictly lower than STOP ($3.93–4.80$). Pausing a 50/50 transaction for verification is a cautious, reversible banking policy.

### Category C: Open Modeling Questions / Currently Missing Signals (4 cases)
* **Cases**: `TC20`, `TC25`, `TC26`, `TC35`
* **Mechanism**:
  - `TC20` (Velocity): 3 transactions within 6 minutes. Rapid succession is not yet captured by the 4 single-transaction checkers.
  - `TC25`, `TC26` (Merchant Category): An unfamiliar merchant within a familiar category. Merchant familiarity is currently modeled as binary.
  - `TC35` (Sparse Profile): Customer profile has fewer than 5 past transactions. Profile uncertainty / maturity is not yet modeled.

---

## 5. Key Modeling Lessons
1. **Identical Evidence Yields Identical Decisions**: In twin pairs (TC04/TC05, TC10/TC11, TC17/TC18, TC25/TC26, TC31/TC32), one case is Legitimate and one is Fraudulent in reality. The agent produced the identical action for both because it operates without ground-truth leakage.
2. **Conditional Independence Limits**: Independent multiplication can dilute single extreme anomalies when routine signals are present. Addressing this is an open modeling goal for Week 2.
3. **HOLD as First-Class Action**: The agent successfully deployed HOLD for ambiguous multi-anomaly cases (TC17, TC18, TC28, TC31, TC32), validating the expected-cost decision model.
