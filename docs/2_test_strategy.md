# QA Test Strategy Document
## AITU Course Registration System — AS1 Deliverable 2

**Date:** March 2024
**Author:** [Your Name]
**System:** AITU Course Registration Portal (Django Web Application)

---

## 1. Project Scope and Objectives

### 1.1 Scope
This test strategy covers the AITU Course Registration Portal — a Django web application enabling students to register accounts, discover courses, and manage enrollments.

**In scope:**
- User registration and authentication
- Course listing, search, and filtering
- Enrollment, drop, and waitlist workflows
- Student dashboard and profile views
- Admin panel access control

**Out of scope:**
- External integrations (payment systems, LDAP/SSO)
- Mobile responsiveness testing
- Accessibility (WCAG) compliance
- Load/performance testing at scale (deferred to AS2)

### 1.2 Objectives
1. Validate that all critical user flows work correctly end-to-end.
2. Ensure business rules (capacity limits, duplicate prevention) are enforced.
3. Confirm access control prevents unauthorized actions.
4. Establish a baseline coverage metric for future assignments.

---

## 2. Risk-Based Test Prioritization

Based on the Risk Assessment (Deliverable 1), testing effort is allocated as follows:

| Module | Risk Level | Test Effort |
|--------|------------|-------------|
| Authentication | CRITICAL | 35% |
| Enrollment Management | CRITICAL | 35% |
| Course Search & Filter | MEDIUM | 15% |
| Student Dashboard | MEDIUM | 10% |
| Admin Panel | MEDIUM | 5% |

---

## 3. Test Approach

### 3.1 Testing Pyramid

```
         /\
        /E2E\          ← 10% of tests (Playwright, full browser)
       /------\
      / Integr \       ← 40% of tests (Django test client, HTTP layer)
     /----------\
    /    Unit    \     ← 50% of tests (models, forms, business logic)
   /--------------\
```

### 3.2 Test Types

**Unit Tests** (`tests/unit/`)
- Scope: Model methods, form validation, utility functions
- Tool: `pytest-django`
- No HTTP, no browser, fastest execution
- Examples: `enrolled_count`, `is_full`, `available_seats`, form field validators

**Integration Tests** (`tests/integration/`)
- Scope: View responses, authentication flows, database state after actions
- Tool: Django `test.Client` via `pytest-django`
- Tests complete request-response cycles
- Examples: POST /enroll/, GET /courses/ with filters, login with wrong password

**End-to-End Tests** (`tests/e2e/`)
- Scope: Complete user journeys through real browser
- Tool: Playwright (`pytest-playwright`)
- Requires a running application instance
- Examples: register → browse courses → enroll → view my courses

### 3.3 Manual vs Automated

| Test Type | Approach | Rationale |
|-----------|----------|-----------|
| Unit tests | Automated | Fast, deterministic, high ROI |
| Integration tests | Automated | Covers request/response cycles reliably |
| E2E tests | Automated (Playwright) | Critical paths need regression protection |
| Exploratory testing | Manual | Finding unexpected edge cases |
| Usability review | Manual | UX cannot be fully automated |

---

## 4. Tool Selection and Configuration

| Tool | Version | Purpose |
|------|---------|---------|
| `pytest` | 8.1.x | Test runner |
| `pytest-django` | 4.8.x | Django integration for pytest |
| `pytest-cov` | 5.0.x | Code coverage reporting |
| `playwright` | 1.43.x | Browser automation (E2E) |
| `pytest-playwright` | 0.4.x | Playwright + pytest integration |
| `factory-boy` | 3.3.x | Test data factories |
| `Faker` | 24.x | Realistic fake data generation |
| `coverage.py` | 7.4.x | Standalone coverage analysis |
| `flake8` | — | Linting (enforced in CI) |
| GitHub Actions | — | CI/CD pipeline |
| Docker | — | Reproducible environment |

### 4.1 pytest Configuration (`pytest.ini`)
```ini
[pytest]
DJANGO_SETTINGS_MODULE = core.settings
pythonpath = app
testpaths = tests
addopts = -v --tb=short --strict-markers
```

### 4.2 Coverage Target
- **Current baseline:** To be measured in first run
- **Minimum threshold:** 70% line coverage (enforced in CI with `--cov-fail-under=70`)
- **Target by AS3:** 80% line coverage

---

## 5. Test Environment

| Environment | Purpose | URL |
|-------------|---------|-----|
| Local (Docker) | Development testing | http://localhost:8000 |
| CI (GitHub Actions) | Automated testing on every push | — |

**Setup:**
```bash
# Run app
docker compose up web

# Run unit + integration tests (no running app needed)
pytest tests/unit/ tests/integration/

# Run E2E tests (app must be running)
pytest tests/e2e/ --base-url=http://localhost:8000

# Full test suite with coverage
pytest tests/unit/ tests/integration/ --cov=app --cov-report=term-missing
```

---

## 6. Test Data Strategy

- **Fixtures:** Defined in `tests/conftest.py` using `pytest` fixtures with `@pytest.mark.django_db`
- **Seed data:** `python manage.py seed` populates 12 courses, 5 departments, 2 users for manual/E2E testing
- **Isolation:** Each test gets a clean database state via Django's test transaction rollback
- **Factory Boy:** To be introduced in AS2 for complex data scenarios

---

## 7. Planned Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Line coverage | % of app code executed by tests | ≥ 70% (AS1), ≥ 80% (AS3) |
| Test count | Total number of automated tests | ≥ 30 by end of AS1 |
| Pass rate | % of tests passing in CI | 100% on main branch |
| High-risk coverage | % of CRITICAL modules with tests | 100% |
| Defect detection rate | Bugs found before user report | Tracked from AS2 |

---

## 8. Entry and Exit Criteria

### Entry Criteria (start testing)
- Application runs successfully via `docker compose up`
- All migrations applied and seed data loaded
- Test dependencies installed

### Exit Criteria (testing complete for AS1)
- All unit and integration tests pass
- Coverage ≥ 70%
- CI pipeline green on main branch
- All CRITICAL-risk modules have automated test coverage

---

## 9. Risks to Testing

| Risk | Mitigation |
|------|------------|
| SQLite concurrency not tested | Document; plan PostgreSQL tests in AS2 |
| E2E tests are flaky | Add `expect().to_be_visible()` with timeouts; retry on CI |
| No authentication rate-limiting | Document as known gap; test manually |
| Seed data state leaks between E2E tests | Flush DB and re-seed before E2E run |
