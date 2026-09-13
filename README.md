# Transaction Agent

A decision-making agent under uncertainty for financial transactions.

The agent evaluates incoming financial transactions against historical customer behavior, updates its probabilistic belief about whether the transaction is **Legitimate** or **Fraudulent**, and selects an action (**APPROVE**, **HOLD**, or **STOP**) using **expected-cost decision theory**.

**HOLD** is treated as a first-class information-gathering action that pauses the transaction to request customer verification before arriving at a final decision.

This project is an investigation into decision-making under uncertainty, not a simple binary fraud classifier.

---

## 1. Canonical Architecture

```text
Historical Data (200 records, 10 customers)
      ↓
Customer Profile Summary (typical amount, merchants, locations, hours)
      ↓
Incoming Transaction (amount, merchant, timestamp, location)
      ↓
Evidence Extraction (consistent signals vs. anomaly signals)
      ↓
Bayesian Belief Update (prior × likelihoods → posterior)
      ↓
Expected-Cost Decision Engine (lowest expected cost among Approve / Hold / Stop)
      ↓
 ┌─────────┬─────────┬─────────┐
 │ Approve │  Hold   │  Stop   │
 └─────────┴─────────┴─────────┘
               ↓
          Customer Verification Request (SMS / Push)
               ↓
         Verification Evidence (Customer Confirms / Customer Denies)
               ↓
         Updated Belief
               ↓
         Final Decision (Approve / Stop)
```

---

## 2. Completed Implementation (Week 1)

All core components are implemented and individually tested in `src/`:

| Module | Purpose | Key Functions / Classes |
| :--- | :--- | :--- |
| [`src/transaction_agent.py`](src/transaction_agent.py) | Core domain models & dataclasses | `HiddenState`, `Action`, `EvidenceDirection`, `VerificationResponse`, `Transaction`, `HistoricalTransaction`, `CustomerProfile`, `ProfileSummary`, `Evidence`, `Belief`, `CostModel`, `Decision`, `Verification`, `PendingVerification` |
| [`src/data_loader.py`](src/data_loader.py) | CSV ingestion & customer grouping | `load_historical_transactions()`, `parse_historical_transaction()`, `group_by_customer()`, `build_customer_profiles()`, `build_all_profile_summaries()` |
| [`src/profile.py`](src/profile.py) | Behavioral profile construction | `calculate_typical_amount()`, `calculate_common_merchants()`, `calculate_typical_locations()`, `calculate_typical_transaction_hours()`, `build_profile_summary()` |
| [`src/evidence.py`](src/evidence.py) | Signal extraction against profile | `check_amount_evidence()`, `check_merchant_evidence()`, `check_location_evidence()`, `check_time_evidence()`, `extract_evidence()`, `extract_verification_evidence()` |
| [`src/belief.py`](src/belief.py) | Bayesian belief engine | `update_belief()`, `LIKELIHOODS` mapping |
| [`src/decision.py`](src/decision.py) | Expected-cost decision engine | `calculate_expected_cost()`, `make_decision()`, `DEFAULT_COST_MODEL` |
| [`src/verification.py`](src/verification.py) | Verification lifecycle & finalization | `request_verification()`, `record_verification()`, `finalize_decision()` |
| [`src/evaluate_v2.py`](src/evaluate_v2.py) | Benchmark evaluation runner | `evaluate_dataset()`, `print_evaluation_report()` |

---

## 3. Prototype Foundations & Modeling Assumptions

> [!NOTE]
> All probabilities, likelihoods, and cost values in this prototype are **synthetic research assumptions** designed to explore agent decision dynamics. They are **not** calibrated banking statistics.

### Initial Belief (Prior)
$$P(\text{Legitimate}) = 0.90, \quad P(\text{Fraudulent}) = 0.10$$

### Prototype Likelihood Table
Under the current simplifying **conditional independence** assumption, likelihoods for observed signals are defined as:

| Evidence Signal | Direction | $P(E \mid \text{Fraud})$ | $P(E \mid \text{Legit})$ | Likelihood Ratio | Note |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `large_amount` | Fraud | 0.30 | 0.20 | 1.50 | Amount > 1.5× typical median |
| `amount_consistent` | Legit | 0.70 | 0.80 | 0.875 | Complement of large amount |
| `new_merchant` | Fraud | 0.30 | 0.15 | 2.00 | Merchant not in profile |
| `merchant_consistent` | Legit | 0.70 | 0.85 | 0.824 | Complement of new merchant |
| `unusual_location` | Fraud | 0.30 | 0.10 | 3.00 | Location not in profile |
| `location_consistent` | Legit | 0.70 | 0.90 | 0.778 | Complement of unusual location |
| `unusual_time` | Fraud | 0.40 | 0.10 | 4.00 | Hour not in typical hours |
| `time_consistent` | Legit | 0.60 | 0.90 | 0.667 | Complement of unusual time |
| `customer_confirms` | Legit | 0.05 | 0.95 | 0.053 | Strong evidence for legitimate |
| `customer_denies` | Fraud | 0.95 | 0.05 | 19.00 | Strong evidence for fraud |

*Missing information remains missing*: Unobserved signals produce neutral `*_unknown` evidence and do not alter belief.

### Synthetic Cost Model
The decision engine chooses the action minimizing:
$$\text{Expected Cost}(\text{Action}) = P(\text{Legit}) \times \text{Cost}(\text{Action} \mid \text{Legit}) + P(\text{Fraud}) \times \text{Cost}(\text{Action} \mid \text{Fraud})$$

`DEFAULT_COST_MODEL` defines:

| Actual State | APPROVE | HOLD | STOP |
| :--- | :---: | :---: | :---: |
| **Legitimate** | 0.0 | **2.0** | 8.0 |
| **Fraudulent** | 10.0 | **2.0** | 0.0 |

This establishes three natural decision regions:
- $P(\text{Fraud}) < 20\% \implies$ **APPROVE** (routine transactions)
- $20\% \le P(\text{Fraud}) \le 75\% \implies$ **HOLD** (uncertain / mixed signals)
- $P(\text{Fraud}) > 75\% \implies$ **STOP** (severe anomalies)

---

## 4. Test Suite Status

The project has **23 automated tests**, all passing:

```bash
python -m pytest
```

```text
collected 23 items

test/test_belief.py ......                                               [ 26%]
test/test_decision.py ....                                               [ 43%]
test/test_evidence.py ...                                                [ 56%]
test/test_integration.py .....                                           [ 78%]
test/test_profile.py .                                                   [ 82%]
test/test_verification.py ....                                           [100%]

============================= 23 passed in 0.13s ==============================
```

---

## 5. V2 Benchmark Evaluation (35 Cases)

The agent was evaluated against the frozen scenario dataset [`experiments/transaction_agent_test_cases_v2.csv`](experiments/transaction_agent_test_cases_v2.csv).

### Ground-Truth Blindness
During evaluation, the runner ([`src/evaluate_v2.py`](src/evaluate_v2.py)) extracted signals strictly from scenario feature fields (`Amount (INR)`, `Merchant`, `Time`, `Location`, `Historical Behavior`, `Evidence Notes`). It had **no access** to `Hidden State` or `Expected Agent Action`. Ground truth was compared only after the decision was made.

### Evaluation Results
* **Overall Agreement**: **22 / 35 matched (62.9%)**
* **Expected Action Distribution**: 12 Approve, 15 Hold, 8 Stop
* **Agent Selected Distribution**: 21 Approve, 9 Hold, 5 Stop
* **Ground Truth States**: 22 Legitimate, 13 Fraudulent

### Failure Categorization (13 Mismatches)

1. **Category A: Prototype Assumption / Conditional Independence Dilution (7 cases: TC04, TC05, TC07, TC10, TC11, TC13, TC22)**
   - *Cause*: Under conditional independence, multiplying 3 routine consistent signals ($0.824 \times 0.778 \times 0.667 \approx 0.428$) dilutes a single moderate anomaly (e.g. `large_amount` ratio 1.5). The posterior fraud probability drops from 10% to 6.6%, falling below the 20% HOLD cutoff and triggering APPROVE.
   - *Example*: TC07 reached $P(\text{Fraud}) = 19.94\%$, narrowly missing the 20.0% boundary by 0.06%.

2. **Category B: Decision Boundary / Evaluation-Set Behavior (2 cases: TC08, TC14)**
   - *Cause*: Benchmark expected STOP; agent selected HOLD.
   - *Rationale*: With 3 anomalies and 1 consistent signal, $P(\text{Fraud})$ reached 40%–51%. Under expected-cost reasoning, HOLD ($EC=2.0$) is mathematically cheaper and safer than irreversible STOP ($EC=3.93$). In real banking, holding a 50/50 transaction for customer verification is rational.

3. **Category C: Open Modeling Questions / Currently Missing Signals (4 cases: TC20, TC25, TC26, TC35)**
   - `TC20` (Velocity): 3 transactions in 6 minutes. Rapid succession is not yet modeled.
   - `TC25`, `TC26` (Merchant Category): An unfamiliar merchant in a familiar category. Merchant checking is currently binary.
   - `TC35` (Sparse Profile): Profile has <5 past transactions. Profile uncertainty / maturity is not yet modeled.

---

## 6. Historical 15-Case Baseline

An earlier 15-case synthetic baseline yielded:
* **11 / 15 correct (73.3%)**

This historical baseline is preserved for reference and is distinct from the 35-case V2 evaluation.

---

## 7. Project Scope & Week 2 Starting Point

### Intentionally Deferred (NOT part of Week 1)
- Machine Learning (ML) classifiers
- Large Language Model (LLM) decision calls
- Temporal transaction velocity modeling
- Merchant category hierarchies
- Customer profile maturity scoring
- Web UI / frontend dashboards
- Production deployment or APIs

### Week 2 Starting Point
Week 2 begins with a tested, integrated decision agent and an empirical evaluation benchmark. The immediate research priorities are:
1. Investigating non-linear evidence combination to prevent dilution of single extreme anomalies.
2. Exploring transaction velocity and profile maturity as formal evidence signals.
3. Analyzing cost matrix calibration for boundary cases.
