# QA Environment Setup Report
## Habaneras de Lino DRF API — QA Assignment 1

---

## 1. Repository Structure

```
qa_as1/
├── sut/                                    # System Under Test (cloned from GitHub)
│   ├── store_app/                          # Main e-commerce API app
│   ├── admin_app/                          # Custom admin panel
│   ├── habaneras_de_lino_drf_api/          # Django project settings
│   │   └── settings/
│   │       ├── settings.py
│   │       └── simple_env_conf.env         # Template for .env
│   ├── nginx/                              # Nginx reverse proxy config
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── tests/
│   ├── conftest.py                         # Shared pytest fixtures
│   ├── unit/
│   │   └── test_models.py                  # Model & validator unit tests
│   ├── integration/
│   │   └── test_api_endpoints.py           # REST API integration tests
│   └── e2e/
│       └── test_admin_panel.py             # Playwright browser tests
├── docs/
│   ├── 1_risk_assessment.md
│   ├── 2_test_strategy.md
│   ├── 3_environment_setup.md
│   └── 4_baseline_metrics.md
├── .github/
│   └── workflows/
│       └── ci.yml                          # GitHub Actions CI pipeline
├── pytest.ini
├── requirements-test.txt
└── README.md
```

---

## 2. Tools Installed & Configured

### 2.1 System Under Test

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.8.10 | Runtime for Django app |
| Django | 4.0.6 | Web framework |
| Django REST Framework | 3.13.1 | API layer |
| PostgreSQL | 14 | Primary database |
| Docker | 24+ | Container runtime |
| Docker Compose | v2 | Multi-container orchestration |
| Nginx | latest | Reverse proxy (port 8001 → Django) |
| Stripe SDK | 5.0.0 | Payment processing |
| Cloudinary | 1.30.0 | Image CDN |

### 2.2 QA / Test Tools

| Tool | Version | Purpose |
|------|---------|---------|
| pytest | 7.4.3 | Test runner |
| pytest-django | 4.7.0 | Django ORM access in tests |
| pytest-cov | 4.1.0 | Coverage reporting |
| requests | 2.31.0 | HTTP client for integration tests |
| Playwright | latest | Browser automation |
| pytest-playwright | 0.4.3 | Playwright fixtures for pytest |
| Faker | 20.1.0 | Realistic test data generation |

---

## 3. SUT Setup Steps

### Step 1 — Clone the repository
```bash
git clone https://github.com/Ceci-Aguilera/habaneras-de-lino-drf-api.git sut
cd sut
```

### Step 2 — Configure environment variables
```bash
cp habaneras_de_lino_drf_api/settings/simple_env_conf.env \
   habaneras_de_lino_drf_api/settings/.env
```
Edit `.env` and fill in:
- `SECRET_KEY` — Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` — PostgreSQL credentials
- `STRIPE_SECRET_KEY` — Stripe test key (`sk_test_...`)
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` — Cloudinary credentials
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` — SMTP credentials

### Step 3 — Start the application
```bash
docker compose up --build
```
Application available at: **http://localhost:8001**
Admin panel: **http://localhost:8001/admin/**

### Step 4 — Create admin user (first run)
```bash
docker compose exec web python manage.py createsuperuser
```

---

## 4. Test Environment Setup Steps

### Step 1 — Install test dependencies
```bash
# From qa_as1/ root
pip install -r requirements-test.txt
```

### Step 2 — Install Playwright browsers
```bash
playwright install chromium
```

### Step 3 — Run unit tests (no app required)
```bash
pytest tests/unit/ --cov=sut/store_app --cov-report=term-missing
```

### Step 4 — Run integration tests (app must be running)
```bash
pytest tests/integration/ -v
```

### Step 5 — Run E2E tests (app must be running)
```bash
pytest tests/e2e/ -v
```

---

## 5. CI/CD Pipeline Configuration

**Platform:** GitHub Actions
**File:** `.github/workflows/ci.yml`

### Pipeline Stages

```
Push to main/PR
      │
      ▼
┌─────────────┐
│ Unit Tests  │  ← PostgreSQL service container
│             │    pytest tests/unit/ + coverage
└──────┬──────┘
       │ (on success)
       ▼
┌──────────────────────┐
│ Integration Tests    │  ← docker compose up (SUT)
│                      │    pytest tests/integration/
└──────────────────────┘
```

**Triggers:**
- Push to `main` or `master`
- Pull Request to `main` or `master`

**Artifacts:**
- `coverage.xml` — uploaded after unit test run

---

## 6. Version Control Setup

- **Repository host:** GitHub
- **Branch strategy:** `main` for stable, feature branches for new test development
- **SUT is pinned** as a git submodule reference (cloned into `sut/`) — not modified
- `.gitignore` excludes: `sut/habaneras_de_lino_drf_api/settings/.env`, `__pycache__/`, `.pytest_cache/`, `coverage.xml`

---

## 7. Known Configuration Issues

| Issue | Workaround |
|-------|-----------|
| `simple_env_conf.env` contains placeholder values | Must be replaced with real credentials before running |
| Stripe live keys not available | Use Stripe test mode keys (`sk_test_*`) |
| Cloudinary required for image fields | Use dummy credentials; image upload tests skipped |
| `GlobalModel` must have exactly one active record | Management command or fixture needed for integration tests |
