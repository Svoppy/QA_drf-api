# QA Assignment 1 — Habaneras de Lino DRF API

## System Under Test

**Habaneras de Lino** — Django REST Framework e-commerce API for a linen clothing store.
Source: https://github.com/Ceci-Aguilera/habaneras-de-lino-drf-api

Tech stack: Django 4.0.6, DRF 3.13.1, PostgreSQL, Nginx, Stripe, Cloudinary, Docker.

## Repository Structure

```
qa_as1/
├── sut/                        # System under test (cloned repo)
├── tests/
│   ├── conftest.py
│   ├── unit/                   # Model & business logic tests (pytest-django)
│   ├── integration/            # API endpoint tests (requests)
│   └── e2e/                    # Browser tests (Playwright)
├── docs/
│   ├── 1_risk_assessment.md
│   ├── 2_test_strategy.md
│   ├── 3_environment_setup.md
│   └── 4_baseline_metrics.md
├── .github/workflows/ci.yml    # CI/CD pipeline
├── pytest.ini
└── requirements-test.txt
```

## Quick Start

### 1. Start the SUT
```bash
cd sut
cp habaneras_de_lino_drf_api/settings/simple_env_conf.env habaneras_de_lino_drf_api/settings/.env
docker compose up --build
# App runs at http://localhost:8001
```

### 2. Install test dependencies
```bash
pip install -r requirements-test.txt
playwright install chromium
```

### 3. Run tests
```bash
# Unit tests only (no running app needed)
pytest tests/unit/ --cov=sut/store_app --cov-report=term-missing

# Integration tests (app must be running)
pytest tests/integration/ -v

# E2E tests (app must be running)
pytest tests/e2e/ -v
```

## Deliverables

| # | Document | Path |
|---|----------|------|
| 1 | Risk Assessment | `docs/1_risk_assessment.md` |
| 2 | Test Strategy | `docs/2_test_strategy.md` |
| 3 | Environment Setup Report | `docs/3_environment_setup.md` |
| 4 | Baseline Metrics | `docs/4_baseline_metrics.md` |
