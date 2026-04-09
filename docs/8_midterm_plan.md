# Midterm Plan
## QA Implementation and Empirical Analysis

This document captures what has already been established for the midterm and
what will be implemented next on top of the Assignment 2 baseline.

---

## 1. Baseline Confirmed

The current Assignment 2 state was re-run and confirmed before starting the
midterm work.

### Current baseline

- Unit tests: 22 passed
- Integration tests: 28 passed
- E2E tests: 5 passed
- Total: 55/55 passed
- Unit coverage gate: 40.41% total coverage, gate passed

### Current evidence already available

- Risk assessment from Assignment 1
- Test strategy from Assignment 1
- Quality gate report from Assignment 2
- Metrics report from Assignment 2
- Working GitHub Actions pipeline
- JUnit-style result artifacts for integration and E2E

---

## 2. Midterm Requirement Mapping

The plan is aligned to the midterm assignment tasks.

### Task 1: Refine Risk-Based Testing Strategy

We will re-evaluate the top high-risk modules using empirical evidence from
automation runs:

- M1 - Order and Checkout
- M2 - Stripe Payment Integration
- M6 - Data Validation
- M8 - Tax and Currency Calculation
- M3 - Cart Management

For each module we will update:

- observed issues
- updated risk score
- likelihood
- impact
- detectability
- evidence from tests, coverage, and pipeline behavior

### Task 2: Expand Automation and Coverage

We will add 8 new midterm-focused test cases across all required levels:

- unit
- integration
- end-to-end

The new tests will target mandatory categories:

- failure scenarios
- edge cases
- concurrency or race conditions
- invalid user behavior

### Task 2.3 and 2.4: CI/CD and Quality Gates

The existing GitHub Actions pipeline will be used as the base.
We will extend the evidence and re-evaluate thresholds for midterm reporting.

### Task 3: Metrics Collection

We will collect real numerical data for:

- coverage
- defects found
- execution time
- pipeline runtime
- flaky rate

### Task 4: Comparative Analysis

We will compare:

- Assignment 1 planning
- Assignment 2 actual outcomes
- Midterm improvements and gaps

### Task 5: Midterm Report

This work will feed a final midterm report with:

- system description
- methodology
- automation implementation
- results
- discussion

---

## 3. What We Have Already Added for Midterm

These are the midterm preparation steps already completed.

### Analysis completed

- Read and decomposed the midterm DOCX requirements
- Mapped requirements to the current repository state
- Re-ran the current Assignment 2 test baseline
- Identified the main gaps between current state and midterm rubric
- Identified the high-risk modules that should drive midterm scope

### Key findings

- The Assignment 2 baseline is stable: 55/55 tests passed
- Existing automation already covers M1, M3, M6, M7, M8, M10
- M2 Stripe is still under-covered and remains a critical midterm target
- Detectability is still weak in serializers and views
- Midterm should focus on stronger evidence, deeper negative testing, and
  better mapping from risk to actual failures

### Implemented in this iteration

The following new midterm tests were added and executed successfully.

| Test ID | File | Level | Module | Category | Result |
|---|---|---|---|---|---|
| TC-MT-UT-M2-01 | `tests/unit/test_midterm_order_failures.py` | Unit | M2, M1 | Failure | Passed |
| TC-MT-UT-M2-02 | `tests/unit/test_midterm_order_failures.py` | Unit | M2, M1 | Failure | Passed |
| TC-MT-UT-M6-01 | `tests/unit/test_midterm_validation.py` | Unit | M6 | Edge | Passed |
| TC-MT-UT-M6-02 | `tests/unit/test_midterm_validation.py` | Unit | M6 | Invalid input | Passed |
| TC-MT-IT-M1-01 | `tests/integration/test_midterm_resilience.py` | Integration | M1 | Failure | Passed |
| TC-MT-IT-M3-01 | `tests/integration/test_midterm_resilience.py` | Integration | M3 | Concurrency | Passed |
| TC-MT-E2E-M8-01 | `tests/e2e/test_midterm_dashboard_access.py` | E2E | M8, admin_app | Invalid behavior | Passed |
| TC-MT-E2E-M1-01 | `tests/e2e/test_midterm_dashboard_access.py` | E2E | M1, admin_app | Invalid behavior | Passed |

Execution summary for this iteration:

- New unit tests executed: 4 passed
- New integration tests executed: 2 passed
- New E2E tests executed: 2 passed
- New midterm tests completed so far: 8

### Midterm defect found and fixed in this iteration

| ID | Area | Observation | Action |
|---|---|---|---|
| MT-DEF-01 | `admin_app` dashboard access | Anonymous users could open `/dashboard/global-configs/` and `/dashboard/orders/` without authentication | Added `DashboardAccessMixin(LoginRequiredMixin)` to dashboard views and verified redirect behavior with E2E tests |

---

## 4. Planned New Midterm Test Cases

The target is 8 new tests. These are the planned candidates.

| Test ID | Level | Module | Category | Planned Goal |
|---|---|---|---|---|
| TC-MT-UT-M2-01 | Unit | M2, M1 | Failure | Stripe token creation failure returns controlled error and leaves no broken order |
| TC-MT-UT-M2-02 | Unit | M2, M1 | Failure | Stripe charge failure rolls back order cleanly |
| TC-MT-UT-M6-01 | Unit | M6 | Edge | Address serializer rejects zip code longer than 5 |
| TC-MT-UT-M6-02 | Unit | M6 | Invalid input | Negative monetary values are rejected by custom field validation |
| TC-MT-IT-M1-01 | Integration | M1 | Invalid behavior | Checkout without shipping address returns controlled client error |
| TC-MT-IT-M1-02 | Integration | M1, M6 | Edge | Oversized or special-character payload does not trigger server error |
| TC-MT-IT-M3-01 | Integration | M3 | Concurrency | Parallel cart interactions remain consistent and do not crash |
| TC-MT-E2E-M8-01 | E2E | M8, admin_app | Invalid behavior | Anonymous access to dashboard global-config pages redirects to login |
| TC-MT-E2E-M1-01 | E2E | M1, admin_app | Invalid behavior | Anonymous access to dashboard order pages redirects to login |

Note:

- 8 tests from this list are now implemented.
- The required three testing levels are now represented in the midterm
  expansion: unit, integration, and E2E.
- Remaining work is no longer test-count expansion; it is evidence, metrics,
  risk reassessment, comparative analysis, and report assembly.

---

## 5. Execution Order

### Phase 1: Evidence and baseline

- Save current pass counts and timing
- Run repeat executions to inspect stability and flaky behavior
- Prepare updated risk reassessment table

### Phase 2: High-risk logic tests

- Add new unit tests for Stripe failure paths
- Add serializer and validation tests for M6

### Phase 3: API behavior expansion

- Add new integration tests for order validation and cart concurrency
- Re-measure execution time and coverage impact

### Phase 4: E2E and access behavior

- Add dashboard authorization tests
- Verify admin flows still pass after changes

### Phase 5: Reporting and comparison

- Update metrics tables
- Build planned-vs-actual comparison
- Write the midterm report sections

---

## 6. Expected Midterm Deliverables

- Updated risk reassessment table for top modules
- New automated tests with IDs and evidence
- Updated CI/CD evidence
- Coverage and execution metrics
- Comparative analysis table
- Midterm report draft

---

## 7. Current Working Assumptions

- GitHub Actions remains the CI/CD platform
- Docker-based SUT remains the execution environment for integration and E2E
- The current repository branch is the source of truth for midterm work
- Stripe behavior will be validated with mocks rather than live payments
