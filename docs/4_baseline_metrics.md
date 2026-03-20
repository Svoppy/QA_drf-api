# Baseline Metrics for Research Paper
## AITU Course Registration System — AS1 Deliverable 4

**Date:** March 2024
**Author:** [Your Name]
**Purpose:** These metrics form the baseline for performance, coverage, and defect reduction analysis in the final research paper.

---

## 1. System Description (for Paper Introduction)

The AITU Course Registration Portal is a Django 4.2 web application simulating the academic course enrollment system of Astana IT University (Kazakhstan). It represents a realistic, medium-complexity web system with authentication, data management, business rule enforcement (seat limits, waitlisting), and role-based access control.

The system was selected because it exhibits the structural characteristics of real-world Kazakhstani higher education platforms: multi-role access, concurrent enrollment operations, and data integrity constraints — making it an appropriate subject for risk-based QA research.

---

## 2. Codebase Metrics (Baseline — AS1)

| Metric | Value |
|--------|-------|
| Total Python source files | 12 |
| Total lines of code (app) | ~550 |
| Number of Django models | 3 (Department, Course, Enrollment) |
| Number of views | 8 |
| Number of URL patterns | 9 |
| Number of HTML templates | 8 |

---

## 3. Risk Assessment Metrics

| Metric | Value |
|--------|-------|
| Total modules analyzed | 5 |
| CRITICAL risk modules | 2 (Authentication, Enrollment) |
| HIGH risk modules | 0 |
| MEDIUM risk modules | 3 (Search, Dashboard, Admin) |
| LOW risk modules | 0 |
| Total identified risks | 18 |
| Risks with mitigations planned | 12 |
| Risks deferred to later assignments | 6 |

**Risk distribution:**
```
CRITICAL  ████████████████████  2 modules (40%)
MEDIUM    ██████████████████████████████  3 modules (60%)
LOW       (none)
```

---

## 4. Test Suite Metrics (AS1 Baseline)

| Metric | Value |
|--------|-------|
| Total test files | 3 |
| Total test cases written | 42 |
| Unit tests | 19 |
| Integration tests | 18 |
| E2E tests (Playwright) | 11 |
| Tests covering CRITICAL modules | 26 (62% of total) |
| Tests covering MEDIUM modules | 16 (38% of total) |

**Test distribution by type:**
```
Unit         ███████████  19 (45%)
Integration  ██████████   18 (43%)
E2E          █████        11 (12% — requires running server)
```

---

## 5. Coverage Plan (Estimated Baseline)

> Note: Actual coverage must be measured after first CI run. Replace these with real numbers from `pytest --cov` output.

| Module | Estimated Coverage | Priority |
|--------|-------------------|----------|
| `courses/models.py` | ~90% | CRITICAL |
| `users/forms.py` | ~95% | CRITICAL |
| `courses/views.py` | ~80% | CRITICAL |
| `users/views.py` | ~75% | CRITICAL |
| `courses/admin.py` | ~30% | MEDIUM |
| `core/settings.py` | ~20% | LOW |
| **Overall estimated** | **~70%** | — |

**Coverage target progression:**

| Assignment | Target Coverage |
|-----------|----------------|
| AS1 (baseline) | ≥ 70% |
| AS2 (automation expanded) | ≥ 80% |
| AS3 (final) | ≥ 85% |

---

## 6. Testing Effort Estimate

| Activity | Estimated Hours |
|----------|----------------|
| Risk assessment & documentation | 4h |
| Django app development (testable system) | 6h |
| Unit test writing | 3h |
| Integration test writing | 3h |
| E2E test writing (Playwright) | 2h |
| CI/CD pipeline setup | 2h |
| Documentation | 3h |
| **Total** | **~23h** |

---

## 7. Defect Baseline

At AS1 (initial setup), no defects have been formally discovered yet. The following are **known limitations** documented for the research paper:

| ID | Description | Module | Severity | Status |
|----|-------------|--------|----------|--------|
| L-01 | No rate limiting on login endpoint | Auth | Medium | Known gap |
| L-02 | Waitlisted students not auto-promoted when seat opens | Enrollment | Low | Deferred |
| L-03 | SQLite race condition on concurrent enrollment | Enrollment | High | Deferred to AS2 |
| L-04 | No HTTPS enforcement in development | Auth | Medium | Infrastructure |
| L-05 | Admin panel accessible at default `/admin/` path | Admin | Low | Known |

---

## 8. Research Paper Connection

### Introduction Chapter
- Use Section 1 (System Description) and Section 2 (Codebase Metrics) as the system overview
- Explain why AITU Course Registration represents a realistic Kazakhstan-context web application

### Methodology Chapter
- Use the Risk Matrix methodology from Deliverable 1
- Reference the Testing Pyramid (Section 3.1 of Deliverable 2)
- Document tool selection rationale (Section 4 of Deliverable 2)

### Baseline Data (for Comparison in Later Chapters)
- **Coverage baseline:** ~70% (to be confirmed after first CI run)
- **Test count baseline:** 42 tests (19 unit + 18 integration + 11 E2E)
- **High-risk module count:** 2 (Authentication, Enrollment)
- **Known defects at baseline:** 0 confirmed, 5 known limitations

### What Changes in AS2/AS3
- AS2 will expand automation (more E2E tests, API tests, performance tests)
- AS3 will analyze: defect detection rate, coverage improvement, and CI pipeline effectiveness
- These AS1 numbers become the **before** state in a before/after analysis

---

## 9. How to Update These Metrics (After First CI Run)

1. Run: `pytest tests/unit/ tests/integration/ --cov=app --cov-report=term-missing`
2. Record the actual line coverage percentage
3. Update Section 5 with real numbers
4. Screenshot the terminal output and save to `docs/screenshots/`
5. Push to GitHub and attach the CI run link

**Screenshot checklist for paper:**
- [ ] `pytest` output showing all tests passing
- [ ] Coverage report terminal output
- [ ] GitHub Actions CI pipeline — green
- [ ] Running app at http://localhost:8000
- [ ] Django admin panel
- [ ] Course list page
- [ ] Enrollment workflow
