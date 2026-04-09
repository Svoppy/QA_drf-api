# Midterm Demo Guide

## Purpose

This file explains exactly what to run and what to show for the midterm project.

## What To Show

- The final report:
  - `docs/REPORT_Midterm_Kazikhanov.docx`
- The new midterm tests:
  - `tests/unit/test_midterm_order_failures.py`
  - `tests/unit/test_midterm_validation.py`
  - `tests/integration/test_midterm_resilience.py`
  - `tests/e2e/test_midterm_dashboard_access.py`
- The fixed application code:
  - `sut/habaneras-de-lino-drf-api/admin_app/views.py`
- The CI/CD proof:
  - PR: `https://github.com/Svoppy/QA_drf-api/pull/2`
  - Actions tab for the repository

## Important Note

- The actual demo URL is `http://localhost:8002`
- The old root `README.md` still contains outdated Assignment 1 information and an old port reference
- The most reliable proof for the full automated run is the GitHub Actions pipeline in PR `#2`
- Local unit tests are safest with a Python version compatible with the project stack, ideally Python `3.9`

## Local Demo Setup

### 1. Start the SUT

Run from:

```powershell
cd "C:\Users\nurym\Documents\AQA mid term\QA_drf-api\sut\habaneras-de-lino-drf-api"
```

Make sure the env file exists:

```powershell
Copy-Item ".\habaneras_de_lino_drf_api\settings\simple_env_conf.env" ".\habaneras_de_lino_drf_api\settings\.env" -Force
```

Start the application:

```powershell
docker compose up --build
```

Open in browser:

```text
http://localhost:8002
```

## Test Dependencies

Run from:

```powershell
cd "C:\Users\nurym\Documents\AQA mid term\QA_drf-api"
```

Install test dependencies:

```powershell
pip install -r requirements-test.txt
pip install -r .\sut\habaneras-de-lino-drf-api\requirements.txt
python -m playwright install chromium
```

## What To Run During Demo

### Option A. Show Only Midterm Tests

Unit:

```powershell
python -m pytest tests\unit\test_midterm_order_failures.py tests\unit\test_midterm_validation.py -v
```

Integration:

```powershell
python -m pytest tests\integration\test_midterm_resilience.py -v
```

E2E:

```powershell
python -m pytest tests\e2e\test_midterm_dashboard_access.py -v
```

### Option B. Show Full Suite

Unit:

```powershell
python -m pytest tests\unit\ -v
```

Integration:

```powershell
python -m pytest tests\integration\ -v
```

E2E:

```powershell
python -m pytest tests\e2e\ -v
```

## Recommended Demo Flow

- Open `docs/REPORT_Midterm_Kazikhanov.docx`
- Show the new midterm test files
- Show the fix in `admin_app/views.py`
- Start Docker and open `http://localhost:8002`
- If Python `3.9` is available, run the new unit tests
- Run the new integration tests
- Run the new E2E tests
- Open PR `#2`
- Open the successful GitHub Actions run linked from the PR as the full end-to-end proof

## What Each Midterm Test Demonstrates

| Test File | What It Demonstrates |
|---|---|
| `test_midterm_order_failures.py` | Stripe token and charge failure handling without partial persistence |
| `test_midterm_validation.py` | Validation of zip code and negative currency configuration |
| `test_midterm_resilience.py` | Controlled handling of malformed order input and stability under parallel cart requests |
| `test_midterm_dashboard_access.py` | Restricted dashboard pages redirect anonymous users to login |

## Evidence Files

- `docs/8_midterm_plan.md`
- `docs/9_midterm_analysis_tables.md`
- `docs/pipeline_run_current.png`
- `docs/pipeline_job_unit_current.png`
- `docs/graph_coverage.png`
- `docs/graph_defects.png`
- `docs/graph_runtime.png`

## Stop The SUT

Run from:

```powershell
cd "C:\Users\nurym\Documents\AQA mid term\QA_drf-api\sut\habaneras-de-lino-drf-api"
docker compose down
```
