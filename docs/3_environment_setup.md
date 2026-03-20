# QA Environment Setup Report
## AITU Course Registration System — AS1 Deliverable 3

**Date:** March 2024
**Author:** [Your Name]

---

## 1. System Requirements

| Component | Version |
|-----------|---------|
| Docker | 24.x+ |
| Docker Compose | 2.x+ |
| Python | 3.11 |
| Git | 2.x+ |

No other dependencies are required on the host machine — Docker handles the rest.

---

## 2. Repository Structure

```
AS1/
├── app/                            # Django application
│   ├── core/                       # Django project configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── courses/                    # Courses app (models, views, URLs)
│   │   ├── management/commands/seed.py  # Database seeding
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── users/                      # Users app (auth, registration)
│   │   ├── forms.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── templates/                  # Django HTML templates
│   │   ├── base.html
│   │   ├── courses/
│   │   └── users/
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── tests/                          # All tests (outside app)
│   ├── conftest.py                 # Shared pytest fixtures
│   ├── unit/
│   │   ├── test_models.py          # Model unit tests
│   │   └── test_forms.py          # Form validation tests
│   ├── integration/
│   │   └── test_views.py          # View/workflow integration tests
│   └── e2e/
│       └── test_e2e_flows.py      # Playwright E2E tests
│
├── docs/                           # Deliverable documents
│   ├── 1_risk_assessment.md
│   ├── 2_test_strategy.md
│   ├── 3_environment_setup.md
│   └── 4_baseline_metrics.md
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD pipeline
│
├── docker-compose.yml
└── pytest.ini
```

---

## 3. Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd AS1
```

### Step 2: Build and Start the Application
```bash
docker compose up --build
```

This automatically:
1. Builds the Django image
2. Runs database migrations
3. Seeds sample data (12 courses, 2 users)
4. Starts Gunicorn on port 8000

**Access the app:** http://localhost:8000

**Default credentials:**
| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin1234` | Superuser (admin panel) |
| `student1` | `Student1234!` | Regular student |

**Admin panel:** http://localhost:8000/admin/

### Step 3: Install Test Dependencies Locally (for running tests)
```bash
pip install -r app/requirements.txt
playwright install chromium
```

---

## 4. Running Tests

### Unit & Integration Tests (no app needed)
```bash
# All unit and integration tests
pytest tests/unit/ tests/integration/ -v

# With coverage report
pytest tests/unit/ tests/integration/ --cov=app --cov-report=term-missing

# Specific test file
pytest tests/unit/test_models.py -v
```

### E2E Tests (app must be running)
```bash
# Start app first
docker compose up web -d

# Run E2E tests
pytest tests/e2e/ --base-url=http://localhost:8000 -v
```

### Full Suite via Docker
```bash
docker compose --profile test run test
```

---

## 5. CI/CD Pipeline

**Platform:** GitHub Actions
**File:** `.github/workflows/ci.yml`

### Pipeline Stages

```
Push/PR
  │
  ▼
[Lint]           ← flake8 code quality check
  │
  ▼
[Unit & Integration Tests]  ← pytest + coverage (≥70%)
  │
  ▼
[E2E Tests]      ← Playwright browser tests
  │
  ▼
[Docker Build]   ← Verifies image builds successfully
```

### Triggers
- Push to `main` or `develop` branches
- Pull requests targeting `main`

### Artifacts
- `coverage.xml` uploaded on every run for tracking

---

## 6. Test Configuration

**`pytest.ini`** — central pytest configuration:
- `DJANGO_SETTINGS_MODULE = core.settings`
- `pythonpath = app` (makes app importable)
- `testpaths = tests`
- Custom markers: `unit`, `integration`, `e2e`, `slow`

**`tests/conftest.py`** — shared fixtures:
- `client` — unauthenticated Django test client
- `auth_client` — authenticated test client (logged in as `student`)
- `course`, `full_course` — pre-created Course objects
- `student`, `another_student` — User objects
- `enrollment` — pre-existing Enrollment object

---

## 7. Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-key` | Django secret key |
| `DEBUG` | `True` | Debug mode |
| `ALLOWED_HOSTS` | `localhost 127.0.0.1` | Allowed hosts |
| `DJANGO_SETTINGS_MODULE` | `core.settings` | Settings module path |

---

## 8. Installed Tools Summary

| Tool | Installation | Verification |
|------|-------------|-------------|
| Docker | System | `docker --version` |
| Python 3.11 | Docker image / local | `python --version` |
| Django 4.2 | `requirements.txt` | `python -m django --version` |
| pytest 8.1 | `requirements.txt` | `pytest --version` |
| pytest-django | `requirements.txt` | (bundled) |
| pytest-cov | `requirements.txt` | (bundled) |
| Playwright | `requirements.txt` + `playwright install` | `playwright --version` |
| coverage.py | `requirements.txt` | `coverage --version` |
| GitHub Actions | Cloud (free tier) | Via GitHub repo |

---

## 9. Known Issues & Workarounds

| Issue | Workaround |
|-------|-----------|
| SQLite not thread-safe for concurrency tests | Run concurrency tests against PostgreSQL in AS2 |
| E2E tests require running server | Start app with `docker compose up web -d` before E2E run |
| Playwright browsers must be installed separately | Run `playwright install chromium` after pip install |
