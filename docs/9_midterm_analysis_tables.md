# Midterm Analysis Tables

## 1. Re-evaluated High-Risk Components

| Module | Original Risk Score | Observed Issues (A2/A3) | Updated Risk Score | Justification |
|---|---:|---|---:|---|
| M1 - Order and Checkout | 20 | D-004 duplicate-order risk still open; malformed JSON handled with controlled error; missing-field and invalid-email paths stable; module coverage 72.00% | 18 | Impact remains critical, but detectability improved and current automation did not reproduce an unhandled checkout crash |
| M2 - Stripe Payment Integration | 15 | New unit tests cover token failure and charge failure rollback; no live payment success-path evidence; module coverage 66.67% | 15 | Impact remains critical and coverage is still below 70%, so risk stays unchanged |
| M6 - Data Validation | 16 | D-005 zip code validation weakness; serializer and negative currency validation now covered; module coverage 81.08% | 14 | Validation remains important, but detectability is higher after added tests |
| M8 - Tax Calculation | 12 | D-002 no active GlobalModel crash; D-003 multiple active GlobalModel crash; module coverage 94.74% | 16 | Empirical evidence showed two real S1 crash modes in a high-impact pricing path |
| M3 - Cart Management | 12 | D-001 unknown token returns 200; concurrency test passed; module coverage 54.17% | 13 | No crash under repeated requests, but detectability is still low and cart ambiguity remains unresolved |

## 2. Failed Test Cases

| Test Name / ID | Module Affected | Failure Type | Frequency (failed runs) | Evidence Source | Status |
|---|---|---|---:|---|---|
| `test_valid_login_redirects_away_from_login` | M7 | Environment/setup failure | 1 | Assignment 2 report, D-006 | Fixed in CI by admin user creation |
| `test_dashboard_shows_store_app_models` | M7 | Environment/setup failure | 1 | Assignment 2 report, D-006 | Fixed in CI by admin user creation |
| `TC-MT-E2E-M8-01` | M8, admin_app | Authorization defect | 1 | Midterm local run before rebuild | Fixed |
| `TC-MT-E2E-M1-01` | M1, admin_app | Authorization defect | 1 | Midterm local run before rebuild | Fixed |

## 3. Flaky Tests

| Test ID | Runs Observed | Passes | Failures | Flaky | Suspected Cause |
|---|---:|---:|---:|---|---|
| TC-MT-IT-M1-01 | 5 | 5 | 0 | No | None observed |
| TC-MT-IT-M3-01 | 5 | 5 | 0 | No | None observed |
| TC-MT-E2E-M8-01 | 5 | 5 | 0 | No | None observed after fix |
| TC-MT-E2E-M1-01 | 5 | 5 | 0 | No | None observed after fix |

## 4. Coverage Gaps by High-Risk Module

| Module | Measured Coverage % | Threshold | Status | Untested Functions / Endpoints / Components |
|---|---:|---:|---|---|
| M1 - Order and Checkout | 72.00 | 70 | Pass | Paid order success path with real cart; full idempotency behavior with valid cart; production cost / profit branch |
| M2 - Stripe Payment Integration | 66.67 | 70 | Below threshold | Live Stripe success path; payment persistence branch; refund/webhook behavior |
| M6 - Data Validation | 81.08 | 70 | Pass | Some serializer/view combinations still only indirectly covered |
| M8 - Tax Calculation | 94.74 | 70 | Pass | No major gap found in current measurable unit path |
| M3 - Cart Management | 54.17 | 70 | Below threshold | Product variation update/delete path; cart serializer nested branches; alternate cart retrieval branches |

## 5. Unexpected System Behavior

| ID | Module | Observation | Predicted in A1 | Status |
|---|---|---|---|---|
| D-001 | M3 | Unknown cart token returns 200 instead of clear missing-cart response | Partially | Open |
| D-006 | M7 | Fresh environment lacked admin user, causing E2E auth flow failure | No | Fixed |
| MT-DEF-01 | M1, M8, admin_app | Anonymous user could access dashboard pages without login | No | Fixed |
| PERF-01 | Whole suite | No performance anomaly observed in repeated midterm runs | No | Observed stable |

## 6. Risk Dimension Mapping

| Module | Likelihood | Impact | Detectability | Evidence Basis |
|---|---|---|---|---|
| M1 - Order and Checkout | Medium | Very High | Medium | Open duplicate-order risk, stable negative-path tests, 72.00% module coverage |
| M2 - Stripe Payment Integration | Medium | Very High | Medium-Low | Failure paths covered, but live payment success and refund behavior still unverified |
| M6 - Data Validation | Medium | High | High | Added serializer and field validation tests, 81.08% module coverage |
| M8 - Tax Calculation | High | Very High | High | Two confirmed S1 crash modes and 94.74% measurable coverage |
| M3 - Cart Management | Medium | High | Low | 54.17% module coverage and unresolved unknown-token behavior |

## 7. Metrics

### 7.1 Before vs After Improvements

| Metric | Before Midterm | After Current Midterm Iteration | Change |
|---|---:|---:|---:|
| Unit tests | 22 | 26 | +4 |
| Integration tests | 28 | 30 | +2 |
| E2E tests | 5 | 7 | +2 |
| Total automated tests | 55 | 63 | +8 |
| Total coverage (`store_app`) | 41.00% | 74.41% | +33.41 pp |
| Unit runtime | 2.18s | 1.77s | -0.41s |
| Integration runtime | 1.11s | 1.15s | +0.04s |
| E2E runtime | 5.82s | 9.17s | +3.35s |
| Total local runtime | 9.11s | 12.09s | +2.98s |

### 7.2 Defect Detection

| Module | Risk Level | Defects Found | Current Count |
|---|---|---|---:|
| M1 | Critical | D-004, MT-DEF-01 | 2 |
| M2 | Critical | No live defect reproduced | 0 |
| M6 | Critical | D-005 | 1 |
| M8 | High | D-002, D-003, MT-DEF-01 (dashboard config access) | 3 |
| M3 | High | D-001 | 1 |
| M7 | Medium | D-006 | 1 |

### 7.3 Stability

| Metric | Value |
|---|---:|
| Repeated integration runs observed | 5 |
| Repeated E2E runs observed | 5 |
| Flaky tests observed | 0 |
| Flaky rate in repeated midterm sample | 0.00% |

## 8. Planned vs Actual

| Aspect | Planned (A1) | Actual (A2/A3) | Gap |
|---|---|---|---|
| Coverage target | 60% overall in A1 planning | 41% in A2, 74.41% after current midterm iteration | A2 missed the planned target; midterm iteration exceeded it |
| Stripe automation | Planned with mocks or test keys | Only mock-style failure-path coverage added so far | Success path and refund flow still missing |
| Cart lifecycle depth | Planned full create -> add -> retrieve -> checkout | Retrieval and resilience covered, real checkout-linked cart path still shallow | Partial fulfillment |
| Admin access coverage | Planned admin smoke only | Midterm found and fixed anonymous dashboard access defect | Scope expanded beyond original plan |
| Pipeline evidence | Planned CI on every commit | Workflow exists and runs by design, but updated midterm pipeline screenshot/log package still pending | Evidence package incomplete |
| Defect expectation | Highest-risk modules expected to yield most defects | Highest-risk modules did yield most defects | Planning assumption confirmed |

## 9. Quality Gate Evaluation

| Gate | Threshold | Current Result | Evaluation |
|---|---:|---:|---|
| Test pass rate | 100% | 63/63 passed locally | Appropriate |
| Total coverage | 70% | 74.41% | Appropriate |
| High-risk module coverage | 70% | M2 = 66.67%, M3 = 54.17% | Too strict for current state, but useful because it exposes real gaps |
| Critical failures allowed | 0 | 0 open blocking failures after fixes | Appropriate |
