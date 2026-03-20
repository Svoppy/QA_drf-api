# QA Test Strategy Document
## Habaneras de Lino DRF API — QA Assignment 1

---

## 1. Project Scope & Objectives

**System under test:** Habaneras de Lino DRF API — a Django REST Framework e-commerce backend.
**Repository:** https://github.com/Ceci-Aguilera/habaneras-de-lino-drf-api

**In scope:**
- All REST API endpoints exposed by `store_app` (products, collections, categories, cart, orders)
- Model-level business logic (validation, tax calculation, cart total)
- Custom admin panel (`admin_app`) — login, dashboard navigation
- Docker infrastructure — startup, connectivity

**Out of scope:**
- Frontend (Next.js) — separate repository
- Stripe live payment processing (test mode only)
- Cloudinary CDN reliability
- Performance / load testing (planned for later assignments)

**Objectives:**
1. Verify that all critical API endpoints return correct status codes and response structures.
2. Validate input validation rules on all POST endpoints.
3. Confirm business logic correctness (pricing, cart totals, order creation).
4. Establish a repeatable, automated test baseline for future assignments.

---

## 2. Test Approach

### 2.1 Testing Levels

| Level | Scope | Tools | When to Run |
|-------|-------|-------|-------------|
| **Unit** | Models, validators, business logic methods | pytest-django, Django TestCase | Every commit (fast, no network) |
| **Integration** | API endpoints, request/response contracts | pytest + requests | Every commit (app must be running) |
| **E2E** | Admin panel browser flows | Playwright | On PR merge or nightly |

### 2.2 Test Priority (Risk-Based)

Tests are written and executed in order of risk score from the Risk Assessment:

1. **Order & Checkout** — POST /orders/ valid and invalid payloads
2. **Data Validation** — All serializer boundary and negative tests
3. **Tax Calculation** — GlobalModel edge cases (0, 1, many active records)
4. **Cart Management** — Full lifecycle: create cart → add items → retrieve → checkout
5. **Product Catalog** — Pagination, detail, 404 on missing items
6. **Admin Panel** — Login, invalid credentials, dashboard visibility

### 2.3 Manual vs Automated

| Test Type | Approach | Reason |
|-----------|----------|--------|
| API contract testing | Automated (pytest) | Repeatable, fast, CI-friendly |
| Model/unit testing | Automated (pytest-django) | No infrastructure required |
| Admin panel smoke | Automated (Playwright) | Browser automation available |
| Stripe webhook testing | Manual + mock | Cannot automate real Stripe events without ngrok |
| Visual UI review | Manual | Admin panel styling edge cases |
| Exploratory testing | Manual | Discover unexpected behaviors |

---

## 3. Tool Selection & Configuration

| Tool | Version | Purpose |
|------|---------|---------|
| **pytest** | 7.4.3 | Test runner |
| **pytest-django** | 4.7.0 | Django integration, in-memory DB for unit tests |
| **pytest-cov** | 4.1.0 | Code coverage reporting |
| **requests** | 2.31.0 | HTTP client for integration tests |
| **Playwright** | latest | E2E browser automation |
| **pytest-playwright** | 0.4.3 | Playwright pytest fixtures |
| **Faker** | 20.1.0 | Generate realistic test data |
| **Docker Compose** | v2 | Run SUT locally |
| **GitHub Actions** | — | CI/CD pipeline |

**pytest.ini configuration:**
```ini
[pytest]
DJANGO_SETTINGS_MODULE = habaneras_de_lino_drf_api.settings.settings
pythonpath = sut
testpaths = tests
```

---

## 4. Test Environment

| Environment | Purpose | How to Start |
|-------------|---------|-------------|
| Local Docker | Integration + E2E testing | `docker compose up --build` in `sut/` |
| GitHub Actions CI | Automated unit + integration | Push to `main` triggers workflow |
| In-memory SQLite | Unit tests only | Automatic via pytest-django |

---

## 5. Risk-Based Test Coverage Plan

| Risk Area | Test Type | Test Count (planned) | Coverage Target |
|-----------|-----------|---------------------|----------------|
| Order creation | Integration | 8 | 90% of order flow branches |
| Data validation | Unit + Integration | 15 | 100% of required fields |
| Tax calculation | Unit | 5 | 100% of pricing methods |
| Cart lifecycle | Integration | 6 | 80% of cart operations |
| Product API | Integration | 6 | 80% of endpoint variants |
| Admin login | E2E | 3 | 100% of auth flows |
| **Total planned** | | **43** | — |

---

## 6. Planned Metrics

| Metric | How Measured | Target |
|--------|-------------|--------|
| **Test coverage (line)** | pytest-cov | ≥ 60% on `store_app/` |
| **Test pass rate** | CI pipeline | 100% on main branch |
| **Defects found per module** | Manual tracking | Tracked per risk area |
| **API response time** | requests elapsed | < 500ms per endpoint (noted, not enforced) |
| **CI pipeline duration** | GitHub Actions | < 5 minutes for unit + integration |

---

## 7. Entry & Exit Criteria

**Entry criteria (to start testing):**
- SUT starts successfully via `docker compose up`
- All migrations applied without error
- Test dependencies installed

**Exit criteria (Assignment 1 complete):**
- All planned unit and integration tests written and passing
- CI pipeline runs green on push
- All 4 deliverable documents completed
- Baseline metrics recorded in `docs/4_baseline_metrics.md`
