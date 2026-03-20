# AITU Course Registration — QA Assignment 1

Django web app for AITU students to browse and enroll in courses. Used as the system under test for QA AS1.

## Quick Start

```bash
docker compose up --build
```

App: http://localhost:8000 | Admin: http://localhost:8000/admin/

| User | Password |
|------|----------|
| `admin` | `admin1234` |
| `student1` | `Student1234!` |

## Run Tests

```bash
pip install -r app/requirements.txt

# Unit + Integration
pytest tests/unit/ tests/integration/ --cov=app --cov-report=term-missing

# E2E (app must be running)
playwright install chromium
pytest tests/e2e/ --base-url=http://localhost:8000
```

## Deliverables

| # | Document | Path |
|---|----------|------|
| 1 | Risk Assessment | `docs/1_risk_assessment.md` |
| 2 | Test Strategy | `docs/2_test_strategy.md` |
| 3 | Environment Setup Report | `docs/3_environment_setup.md` |
| 4 | Baseline Metrics | `docs/4_baseline_metrics.md` |
# qa_as1
