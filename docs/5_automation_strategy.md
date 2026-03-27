# Automation Strategy & CI/CD Integration
## Habaneras de Lino DRF API — QA Assignment 2

---

## 1. Automation Scope

Assignment 2 expands on the risk-based test strategy from Assignment 1 by automating the critical and high-risk modules first, then extending coverage toward the planned targets.

| Priority | Module | Risk Score | Automation Status |
|----------|--------|------------|-------------------|
| 1 | M1 — Order & Checkout | 20 🔴 | Expanded (5 new integration tests) |
| 2 | M8 — Tax & Currency | 12 🔴 | New (6 unit tests) |
| 3 | M6 — Data Validation | 16 🔴 | Expanded (field boundary tests) |
| 4 | M3 — Cart Management | 12 🟠 | Expanded (4 lifecycle tests) |
| 5 | M4 — Product Catalog | 6 🟡 | Extended (response time tests) |
| 6 | M7 — Admin Panel | 6 🟡 | Existing 5 E2E tests retained |

---

## 2. Tool Selection Rationale

| Tool | Version | Role | Why Selected |
|------|---------|------|-------------|
| **pytest** | 7.4.3 | Test runner | Industry standard; rich plugin ecosystem |
| **pytest-django** | 4.7.0 | Unit test DB isolation | Provides `@pytest.mark.django_db` + in-memory SQLite |
| **pytest-cov** | 4.1.0 | Coverage measurement | Integrates natively with pytest; supports `--cov-fail-under` |
| **requests** | 2.31.0 | Integration HTTP client | Minimal, readable; no framework lock-in |
| **Playwright + pytest-playwright** | latest / 0.4.3 | Browser E2E | Headless Chromium; auto-wait APIs reduce flakiness |
| **GitHub Actions** | — | CI/CD runner | Free for public repos; native artifact/report support |

---

## 3. Test Suite Growth (AS1 → AS2)

| Category | AS1 Baseline | AS2 Added | AS2 Total |
|----------|-------------|-----------|-----------|
| Unit (no Docker) | 10 | 9 | **19** |
| Integration (app running) | 13 | 19 | **32** |
| E2E (Playwright) | 5 | 0 | **5** |
| **Total** | **28** | **28** | **56** |

New test files added in AS2:
- `tests/unit/test_globalmodel.py` — 6 tests (M8 tax/currency edge cases)
- `tests/unit/test_product_model.py` — 6 tests (Cart total, ClothingProduct fields)
- `tests/integration/test_cart_lifecycle.py` — 4 tests (M3 cart token behavior)
- `tests/integration/test_orders_extended.py` — 5 tests (M1 field validation, idempotency)
- `tests/integration/test_response_times.py` — 6 tests (performance gate, all GET endpoints)

---

## 4. CI/CD Pipeline Design

Pipeline file: `.github/workflows/ci.yml`

### Pipeline Stages

```
Push to main / PR → [Job 1: Unit Tests] → [Job 2: Integration Tests] → [Job 3: E2E Tests]
                          ↓                        ↓                          ↓
                    Coverage XML           JUnit XML report           JUnit XML report
                    (artifact)             (artifact)                 (artifact)
```

### Job 1 — Unit Tests + Coverage Gate
- **Trigger:** every push and PR
- **Environment:** Ubuntu runner, Python 3.12, SQLite in-memory (no Docker)
- **Runs:** `tests/unit/`
- **Quality gate:** `--cov-fail-under=60` → pipeline fails if coverage drops below 60%
- **Env vars:** `DJANGO_SETTINGS_MODULE=habaneras_de_lino_drf_api.settings.test`

### Job 2 — Integration Tests (depends on Job 1 passing)
- **Environment:** Ubuntu runner, Docker Compose spins up full SUT (nginx + Django + PostgreSQL)
- **Health check:** polls `GET /store/clothing-collections/` every 5s, max 30 attempts (150s)
- **Runs:** `tests/integration/`
- **Artifacts:** JUnit XML (`integration-results.xml`) uploaded on pass or fail

### Job 3 — E2E Tests (depends on Job 2 passing)
- **Environment:** Ubuntu runner, Docker Compose SUT, Playwright Chromium with `--with-deps`
- **Runs:** `tests/e2e/`
- **Artifacts:** JUnit XML (`e2e-results.xml`)

### Failure Handling
- Any job failure stops downstream jobs (via `needs:`)
- On failure: Docker logs (last 60 lines) are printed to the Actions run for diagnosis
- All test result artifacts are uploaded even on failure (`if: always()`)

---

## 5. Local Test Execution

```bash
# Start SUT
cd sut/habaneras-de-lino-drf-api && docker compose up -d

# Unit tests only (no SUT needed)
.venv/bin/pytest tests/unit/ -v --cov=store_app --cov-report=term-missing

# Integration tests (SUT must be running)
.venv/bin/pytest tests/integration/ -v

# E2E tests (SUT + Playwright)
.venv/bin/pytest tests/e2e/ -v

# All tests
.venv/bin/pytest tests/ -v
```

---

## 6. Version Control

All test scripts are tracked in the same repository as the QA strategy documents:

```
AS1/
├── tests/
│   ├── unit/
│   │   ├── test_models.py          # AS1
│   │   ├── test_globalmodel.py     # AS2 — M8 tax calculation
│   │   └── test_product_model.py   # AS2 — Cart total, product fields
│   ├── integration/
│   │   ├── test_api_endpoints.py   # AS1
│   │   ├── test_cart_lifecycle.py  # AS2 — M3 cart token tests
│   │   ├── test_orders_extended.py # AS2 — M1 order validation
│   │   └── test_response_times.py  # AS2 — performance gate
│   └── e2e/
│       └── test_admin_panel.py     # AS1
├── .github/workflows/ci.yml        # AS2 — CI/CD pipeline
└── docs/
    ├── 5_automation_strategy.md    # AS2 — this document
    ├── 6_quality_gate_report.md    # AS2 — quality gates
    └── 7_metrics_report.md         # AS2 — metrics
```
