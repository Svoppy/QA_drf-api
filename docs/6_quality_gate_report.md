# Quality Gate Report
## Habaneras de Lino DRF API — QA Assignment 2

---

## 1. Quality Gate Definitions

Quality gates are pass/fail thresholds that must be satisfied before code can merge to `main`. They are enforced automatically by the GitHub Actions pipeline.

### Gate 1 — Unit Test Pass Rate

| Criterion | Threshold | Enforcement |
|-----------|-----------|-------------|
| Unit test pass rate | **100%** | CI fails on any unit test failure |
| Failed tests allowed | **0** | Pipeline blocks merge |

**Rationale:** Unit tests run against in-memory SQLite and have no external dependencies. A failure here indicates a model logic regression that must be fixed before proceeding.

---

### Gate 2 — Code Coverage

| Criterion | Threshold | Enforcement |
|-----------|-----------|-------------|
| Line coverage on `store_app/` | **≥ 60%** | `--cov-fail-under=60` in CI |
| Measured by | pytest-cov | Coverage XML uploaded as artifact |

**Rationale:** 60% is the minimum viable coverage for a business-critical e-commerce backend. The threshold is intentionally lower than 80% to account for untestable code paths (Stripe webhooks, Cloudinary uploads) without ignoring them entirely. Coverage targets increase per assignment:

| Assignment | Coverage Target | Status |
|------------|----------------|--------|
| AS1 | Baseline only (~25% estimated) | Achieved |
| AS2 | ≥ 60% | Enforced in CI |
| AS3 | ≥ 70% | Planned |

---

### Gate 3 — Integration Test Pass Rate

| Criterion | Threshold | Enforcement |
|-----------|-----------|-------------|
| Integration test pass rate | **100%** | CI Job 2 fails on any test failure |
| Critical module failures allowed | **0** | M1, M3, M6, M8 failures block merge |
| API response time (all GET endpoints) | **< 500ms** | Asserted per test in `test_response_times.py` |

**Rationale:** Integration tests call the live API. A failure here means an endpoint has broken contract or regressed. The 500ms threshold is based on typical Django + PostgreSQL response times under no-load conditions.

---

### Gate 4 — E2E Test Pass Rate

| Criterion | Threshold | Enforcement |
|-----------|-----------|-------------|
| E2E test pass rate | **100%** | CI Job 3 fails on any failure |
| Admin login flow must pass | Required | Security regression check |

**Rationale:** E2E tests verify the admin panel — the operational interface. Failures here impact store managers directly.

---

### Gate 5 — No Critical Defects on Main

| Criterion | Threshold | Enforcement |
|-----------|-----------|-------------|
| Severity-1 (data loss / crash) defects | **0** | Manual review + test coverage for known risks |
| Severity-2 (wrong business logic) defects | **0** | Covered by unit + integration tests |
| Known defects deferred to AS3 | Documented | See Section 3 below |

---

## 2. Gate Results (AS2 Run — 2026-03-27)

### Unit Tests

| Metric | Result | Gate | Status |
|--------|--------|------|--------|
| Tests run | 19 | — | — |
| Tests passed | 19 | 19 / 19 | ✅ PASS |
| Tests failed | 0 | 0 allowed | ✅ PASS |
| Line coverage (store_app) | TBD (run locally) | ≥ 60% | Pending CI run |

### Integration Tests

| Metric | Result | Gate | Status |
|--------|--------|------|--------|
| Tests run | 32 | — | — |
| Tests passed | TBD | 32 / 32 required | Pending CI run |
| Response time gate | TBD | < 500ms | Pending CI run |

### E2E Tests

| Metric | Result | Gate | Status |
|--------|--------|------|--------|
| Tests run | 5 | — | — |
| Tests passed | TBD | 5 / 5 required | Pending CI run |

> Note: Integration and E2E results pending first GitHub Actions run after push. Local runs show all unit tests passing.

---

## 3. Known Defects & Risk Register

These defects were identified during testing and are documented here. They are not blocking the AS2 quality gate because they are either by-design API behaviour or scheduled for AS3.

| ID | Severity | Module | Description | Status |
|----|----------|--------|-------------|--------|
| D-001 | S2 | M3 — Cart | `GET /cart/<token>/` returns **200** for any unknown token (creates empty cart), not 404. Caller cannot distinguish a missing cart from an empty cart. | Open — documented in AS1 |
| D-002 | S1 | M8 — Tax | `GlobalModel.objects.get(active=True)` raises unhandled `DoesNotExist` if no active record exists, causing 500 on all pricing calls. | Covered by `test_no_active_model_raises_does_not_exist` |
| D-003 | S1 | M8 — Tax | `GlobalModel.objects.get(active=True)` raises `MultipleObjectsReturned` if two records are active simultaneously. No uniqueness constraint enforced. | Covered by `test_multiple_active_models_raises_multiple_objects_returned` |
| D-004 | S2 | M1 — Orders | No idempotency key on POST /orders/ — duplicate requests may create duplicate orders. Not confirmed (requires cart setup). | Test added; full validation deferred to AS3 |
| D-005 | S3 | M6 — Validation | `zip_code` field has `max_length=5` at model level but DRF serializer may not enforce this without explicit `MaxLengthValidator`. | Test added: `test_zip_code_too_long_rejected_or_truncated` |

---

## 4. Alerting & Failure Handling

| Failure Type | Response |
|-------------|----------|
| Unit test fails | CI blocks merge; developer must fix before PR can be approved |
| Coverage drops below 60% | CI blocks merge; developer must add tests or exclude untestable code via `# pragma: no cover` |
| Integration test fails | CI blocks merge; Docker logs dumped automatically to Actions run |
| E2E test fails | CI blocks merge; Playwright screenshot/trace available in artifact |
| Response time > 500ms | Test fails with elapsed time in error message |
| Docker SUT fails to start | CI fails with health-check timeout message; container logs printed |
