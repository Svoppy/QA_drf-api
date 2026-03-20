# Risk Assessment Document
## AITU Course Registration System — AS1 Deliverable 1

**Date:** March 2024
**Author:** [Your Name]
**System:** AITU Course Registration Portal (Django Web Application)

---

## 1. System Overview

The AITU Course Registration Portal is a Django-based web application that allows students of Astana IT University to browse, search, and enroll in academic courses. Core functionality includes user authentication, course discovery, enrollment management, and a student dashboard.

**Technology Stack:**
- Backend: Django 4.2 (Python)
- Database: SQLite (dev) / PostgreSQL (prod)
- Frontend: Django Templates (HTML/CSS)
- Infrastructure: Docker, Gunicorn

**Key Modules:**
1. Authentication (register, login, logout)
2. Course Listing & Search
3. Enrollment Management (enroll, drop, waitlist)
4. Student Dashboard (my courses, profile)
5. Admin Panel

---

## 2. Risk Assessment Methodology

Risk was assessed using a **Risk Matrix** based on two dimensions:

| Dimension | Scale | Criteria |
|-----------|-------|----------|
| **Probability** | 1–5 | How likely is a failure in this module? |
| **Impact** | 1–5 | How severe would a failure be for users/business? |

**Risk Score = Probability × Impact**

| Score Range | Risk Level | Priority |
|-------------|------------|----------|
| 20–25 | Critical | Test first, thoroughly |
| 12–19 | High | Requires comprehensive testing |
| 6–11 | Medium | Standard testing |
| 1–5 | Low | Basic coverage sufficient |

---

## 3. Module Risk Analysis

### Module 1: User Authentication
**Description:** Registration, login, logout, session management, password validation.

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Probability | 4 | Auth bugs are frequent; complex validation rules |
| Impact | 5 | Unauthorized access = security breach; broken login = full lockout |
| **Risk Score** | **20** | **CRITICAL** |

**Key risks:**
- Brute force attacks on login endpoint (no rate limiting in MVP)
- Duplicate email registration bypass
- Session fixation after login
- Password validation not enforced on client side
- Redirect after login (`?next=`) could be manipulated (open redirect)

**Assumptions:** CSRF protection is enabled (Django default). Password hashing uses PBKDF2 (Django default).

---

### Module 2: Enrollment Management
**Description:** Enrolling in courses, dropping, waitlisting, preventing duplicates, capacity enforcement.

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Probability | 4 | Complex state machine; concurrent access possible |
| Impact | 5 | Incorrect enrollment = wrong academic record, seat overbooking |
| **Risk Score** | **20** | **CRITICAL** |

**Key risks:**
- Race condition: two students enroll simultaneously in the last seat
- Double enrollment bypass (if unique constraint fails)
- Enrolling in inactive/full courses
- Dropping course you're not enrolled in (404 vs. 403 ambiguity)
- Waitlist-to-enrolled promotion logic (not yet implemented)

**Assumptions:** SQLite handles concurrency poorly; PostgreSQL recommended for production.

---

### Module 3: Course Search & Filter
**Description:** Text search by title/code/instructor, filter by department and semester.

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Probability | 3 | Search logic is relatively simple but user-facing |
| Impact | 3 | Broken search = poor UX but not data corruption |
| **Risk Score** | **9** | **MEDIUM** |

**Key risks:**
- SQL injection via search query (mitigated by Django ORM parameterization)
- Empty results when filters are combined (no course matches)
- Case sensitivity in search (Django `icontains` mitigates this)
- Performance: N+1 queries on course list without `select_related`

**Assumptions:** Django ORM prevents raw SQL injection.

---

### Module 4: Student Dashboard (My Courses / Profile)
**Description:** Displays enrolled courses, credits count, enrollment history.

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Probability | 2 | Read-only; low mutation risk |
| Impact | 3 | Wrong data displayed; credit miscalculation affects advising |
| **Risk Score** | **6** | **MEDIUM** |

**Key risks:**
- Total credits calculation includes dropped/waitlisted courses incorrectly
- Displaying another student's data (IDOR — Insecure Direct Object Reference)
- Stale enrollment status shown after status change

---

### Module 5: Admin Panel
**Description:** Django Admin for managing courses, departments, enrollments.

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Probability | 2 | Low user-facing; admin users are trusted |
| Impact | 4 | Admin can delete/modify all data |
| **Risk Score** | **8** | **MEDIUM** |

**Key risks:**
- Default admin credentials not changed in production
- Admin accessible without TLS/HTTPS in deployment
- Bulk enrollment edits bypassing business logic

---

## 4. Prioritized Risk Summary

| Rank | Module | Risk Score | Level | Priority Action |
|------|--------|-----------|-------|----------------|
| 1 | Authentication | 20 | CRITICAL | Full test coverage: unit + integration + E2E |
| 2 | Enrollment Management | 20 | CRITICAL | Concurrency tests, state machine validation |
| 3 | Admin Panel | 8 | MEDIUM | Access control tests |
| 4 | Course Search & Filter | 9 | MEDIUM | Functional + edge case tests |
| 5 | Student Dashboard | 6 | MEDIUM | Data integrity tests |

---

## 5. Assumptions & Constraints

1. The system uses Django's built-in CSRF protection — token-based attacks are mitigated.
2. Testing is performed in a SQLite environment; production risks of concurrency are higher with SQLite than PostgreSQL.
3. No external payment or academic SIS integration exists in this version.
4. Rate limiting and HTTPS termination are assumed to be handled at the infrastructure level (e.g., nginx/load balancer), not the application layer.
5. Admin users are treated as fully trusted; privilege escalation within admin is out of scope.

---

## 6. Risk Reduction Strategy

| Risk | Mitigation |
|------|------------|
| Double enrollment | Database `unique_together` constraint + application-level check |
| Auth bypass | Django auth middleware + `@login_required` decorator |
| SQL injection | Django ORM parameterization |
| Session fixation | Django rotates session key on login |
| IDOR | All queries filtered by `request.user` |
| Race conditions | Recommend moving to PostgreSQL + DB-level locking |
