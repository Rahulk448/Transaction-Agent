# Transaction Agent — Master Project History & Handoff Document

**Project**: Transaction Agent  
**Repository**: `Rahulk448/Transaction-Agent`  
**Current Milestone**: Week 1 Completion — End-to-End Integration & Benchmark Evaluation  
**Date of Record**: September 13, 2026  

---

## 1. Source-of-Truth Hierarchy & Rules of Engagement

To ensure continuity across future AI agent and developer sessions, all contributors must respect the following hierarchy:

$$\text{Actual Repository Code / Artifacts} \;>\; \text{Master Project History} \;>\; \text{Conversation Memory}$$

### Golden Rules
1. **Never Rebuild Completed Work**: If a component or test is marked as completed in this history and verified by code, do not restart, recreate, or redesign it.
2. **Preserve Frozen Assets**: The benchmark dataset [`experiments/transaction_agent_test_cases_v2.csv`](experiments/transaction_agent_test_cases_v2.csv) is strictly **frozen**. Never overwrite, modify, or regenerate it.
3. **Ground-Truth Blindness**: Ground truth (`Hidden State`, `Expected Agent Action`) must never be provided to the agent or feature extractors during decision-making. It is strictly an evaluation-time metric.
4. **No Uncalibrated Feature Creep**: Do not implement ML, LLM, or complex velocity/clustering models until research foundations and requirements are formally established.
5. **HOLD is First-Class**: HOLD is an explicit, low-friction information-gathering action, not a collapsed fallback or failure state.

---

## 2. Project Purpose & Canonical Architecture

Transaction Agent is a probabilistic decision-making system under uncertainty.

The hidden state is binary:
- **Legitimate**
- **Fraudulent**

The agent chooses from three actions:
- **APPROVE**: Accept transaction immediately (cost = 0 for legit; cost = 10 for fraud).
- **HOLD**: Pause transaction and request customer verification (cost = 2 for legit; cost = 2 for fraud).
- **STOP**: Terminate transaction immediately (cost = 8 for legit; cost = 0 for fraud).

### The Canonical Decision Pipeline
```text
Historical Behavioral Data (200 records, 10 customers)
      ↓
Customer Profile Summary (typical amount, common merchants, locations, hours)
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
          Customer Verification Request (PendingVerification)
               ↓
         Verification Evidence (customer_confirms / customer_denies)
               ↓
         Updated Belief
               ↓
         Final Decision (Approve / Stop)
```

---

## 3. Chronological Session Log (Week 1)

### Phase 1: Problem Definition & Domain Modeling (Aug 31 – Sep 2, 2026)
- **Objective**: Establish domain semantics and core data structures.
- **Completed**:
  - Researched cost-sensitive fraud detection (Bahnsen et al., Fraud Detection Handbook).
  - Defined dataclasses in [`src/transaction_agent.py`](src/transaction_agent.py): `Transaction`, `HistoricalTransaction`, `CustomerProfile`, `ProfileSummary`, `Evidence`, `Belief`, `CostModel`, `Decision`, `Verification`, `PendingVerification`.
  - Defined enums: `HiddenState`, `Action`, `EvidenceDirection`, `VerificationResponse`.

### Phase 2: Historical Data & Behavioral Profiles (Sep 3 – Sep 8, 2026)
- **Objective**: Ingest raw historical transactions and derive customer profiles.
- **Completed**:
  - Ingested [`data/synthetic_historical_transactions.csv`](data/synthetic_historical_transactions.csv) (200 transactions across 10 customers `C001`–`C010`).
  - Implemented [`src/data_loader.py`](src/data_loader.py) to parse CSV rows and group by customer.
  - Implemented [`src/profile.py`](src/profile.py) to calculate median typical amount, unique common merchants, locations, and transaction hours.
  - *Key Constraint Identified*: `build_all_profile_summaries()` returns a `list[ProfileSummary]`, not a dictionary.

### Phase 3: Core Component Implementation (Sep 8 – Sep 11, 2026)
- **Objective**: Build individual units for evidence, belief, decision, and verification.
- **Completed**:
  - [`src/evidence.py`](src/evidence.py): Amount, merchant, location, time checkers against profile summary.
  - [`src/belief.py`](src/belief.py): Bayesian updater using prior and likelihood tables.
  - [`src/decision.py`](src/decision.py): Expected-cost calculator using 6 explicit cost fields.
  - [`src/verification.py`](src/verification.py): Verification request, response recording, and finalization.
  - Unit tests: 12 tests passing across `test/test_*.py`.

### Phase 4: Integration Discovery & Likelihood Alignment (Sep 13, 2026)
- **Discovery**: In a smoke test using customer `C001`, an incoming transaction matching the profile produced `amount_consistent`, `merchant_consistent`, `location_consistent`, and `time_consistent`. However, the belief remained locked at 0.90 / 0.10.
- **Root Cause**: `src/belief.py` only contained entries for anomaly signals (`large_amount`, `new_merchant`, `unusual_time`) and customer responses. Consistency signals and `unusual_location` evaluated to `None` and were silently dropped.
- **Resolution**:
  - Extended `LIKELIHOODS` in [`src/belief.py`](src/belief.py) with exact mathematical complements ($P(\text{consistent}) = 1 - P(\text{anomaly})$):
    - `amount_consistent`: Fraud 0.70, Legit 0.80
    - `merchant_consistent`: Fraud 0.70, Legit 0.85
    - `time_consistent`: Fraud 0.60, Legit 0.90
  - Added prototype assumptions for location:
    - `unusual_location`: Fraud 0.30, Legit 0.10 (3× fraud signal)
    - `location_consistent`: Fraud 0.70, Legit 0.90
  - Verified belief updates with unit tests in [`test/test_belief.py`](test/test_belief.py).

### Phase 5: Cost Matrix Optimization for HOLD (Sep 13, 2026)
- **Discovery**: The original cost matrix (`hold_legitimate=6.0`, `hold_fraudulent=4.0`) resulted in HOLD having a higher expected cost than both APPROVE and STOP at every probability point in $[0, 1]$. HOLD was mathematically inadmissible.
- **Resolution**:
  - Established `DEFAULT_COST_MODEL` in [`src/decision.py`](src/decision.py):
    - `approve_legitimate=0.0`, `approve_fraudulent=10.0`
    - `hold_legitimate=2.0`, `hold_fraudulent=2.0` (reflecting low customer friction for verification)
    - `stop_legitimate=8.0`, `stop_fraudulent=0.0`
  - Yields three clean decision regions:
    - $P(\text{Fraud}) < 20\% \implies$ APPROVE
    - $20\% \le P(\text{Fraud}) \le 75\% \implies$ HOLD
    - $P(\text{Fraud}) > 75\% \implies$ STOP
  - Integrated across decision and verification modules with tests in [`test/test_decision.py`](test/test_decision.py) and [`test/test_integration.py`](test/test_integration.py). Total test suite reached **23 passed tests**.

### Phase 6: V2 Benchmark Evaluation on 35 Frozen Cases (Sep 13, 2026)
- **Objective**: Evaluate the complete integrated agent on the 35 scenario cases in [`experiments/transaction_agent_test_cases_v2.csv`](experiments/transaction_agent_test_cases_v2.csv).
- **Execution**: Built automated runner [`src/evaluate_v2.py`](src/evaluate_v2.py) strictly blind to `Hidden State` and `Expected Agent Action`.
- **Outcome**:
  - **22 / 35 Matched (62.9% accuracy)**.
  - Action Distribution: Agent selected 21 APPROVE, 9 HOLD, 5 STOP (vs. expected 12 APPROVE, 15 HOLD, 8 STOP).
  - Evaluated 22 Legitimate and 13 Fraudulent hidden states.
  - Categorized all 13 mismatches into Categories A, B, and C.
  - Documented findings in [`experiments/test-cases.md`](experiments/test-cases.md) and [`README.md`](README.md).

---

## 4. Architectural Inventory

```
Transaction-Agent/
├── data/
│   └── synthetic_historical_transactions.csv   # 200 records, 10 customers (behavioral history)
├── experiments/
│   ├── test-cases.md                           # Comprehensive evaluation report & 35-case table
│   └── transaction_agent_test_cases_v2.csv     # FROZEN 35-case evaluation dataset (read-only)
├── src/
│   ├── belief.py                               # Bayesian update logic & LIKELIHOODS mapping
│   ├── data_loader.py                          # Ingestion & profile grouping
│   ├── decision.py                             # Expected-cost calculation & DEFAULT_COST_MODEL
│   ├── evaluate_v2.py                          # Ground-truth-blind V2 evaluation runner
│   ├── evidence.py                             # Rule-based signal extraction
│   ├── profile.py                              # Customer profile summarization
│   ├── transaction_agent.py                    # Domain models, dataclasses, enums
│   └── verification.py                         # Customer verification handling & finalization
├── test/
│   ├── test_belief.py                          # Unit tests for belief updates (6 tests)
│   ├── test_decision.py                        # Unit tests for expected cost & decision zones (4 tests)
│   ├── test_evidence.py                        # Unit tests for evidence checkers (3 tests)
│   ├── test_integration.py                     # Full end-to-end pipeline & smoke tests (5 tests)
│   ├── test_profile.py                         # Unit tests for profile summary (1 test)
│   └── test_verification.py                    # Unit tests for verification workflow (4 tests)
├── discussion-record.md                        # Forum outreach and feedback records
├── pytest.ini                                  # Python path configuration
├── README.md                                   # Public project documentation
├── research-file.md                            # Academic & industry research notes
└── PROJECT-HISTORY.md                          # Master durable handoff document (this file)
```

---

## 5. Summary of 13 Mismatches in V2 Evaluation

| Category | Cases | Root Cause / Dynamics | Classification |
| :--- | :--- | :--- | :--- |
| **Category A** | `TC04`, `TC05`, `TC07`, `TC10`, `TC11`, `TC13`, `TC22` (7 cases) | Single anomaly (e.g. large amount ₹15,000) is diluted by three routine consistency signals under conditional independence. Posterior fraud probability lands at $6.6\%–19.9\%$, below the $20\%$ HOLD threshold. (TC07 reached $19.94\%$, missing by $0.06\%$). | Prototype Assumption / Conditional Independence |
| **Category B** | `TC08`, `TC14` (2 cases) | Benchmark expected STOP, agent chose HOLD. With 3 anomalies, $P(\text{Fraud})$ reached $40\%–51\%$. Under expected-cost reasoning, HOLD ($EC=2.0$) is strictly cheaper than an irreversible STOP ($EC=3.93–4.80$). Pausing is cautious and rational. | Evaluation-Set Behavior / Decision Boundary |
| **Category C** | `TC20`, `TC25`, `TC26`, `TC35` (4 cases) | `TC20` has rapid velocity (3 txs in 6 mins). `TC25`/`TC26` have merchant category familiarity. `TC35` has sparse profile history (<5 txs). None of these signals are yet supported by the prototype feature extractor. | Open Modeling Question / Missing Signals |

---

## 6. Intentionally Deferred Items (Out of Scope for Week 1)

The following items are **explicitly deferred** to future phases and must **not** be implemented in Week 1:
- Machine Learning (ML) classifiers or model training
- Large Language Model (LLM) integration or confidence-based overrides
- Transaction velocity / burst-rate modeling
- Merchant category taxonomies and hierarchies
- Customer profile maturity scoring
- User interfaces, web dashboards, or frontends
- Production APIs, deployment scripts, or live payment gateway integrations

---

## 7. Week 2 Starting Point

When resuming in Week 2, the team will start from:
1. **Repository State**: Clean, passing 23/23 tests on Python 3.14.
2. **Benchmark Baseline**: 22/35 (62.9%) on the frozen V2 dataset.
3. **Primary Research Objectives**:
   - **Non-Linear Evidence Combination**: Investigate how extreme individual anomalies (e.g. amount > 4× historical max) should bypass or resist dilution from routine consistent signals.
   - **Velocity & History Maturity Modeling**: Formalize transaction velocity (TC20) and profile uncertainty (TC35) as first-class domain evidence.
   - **Cost Matrix Boundary Calibration**: Study the transition threshold between HOLD and STOP for high-anomaly fraud patterns.
