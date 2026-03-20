# Risk Assessment Document
## Habaneras de Lino DRF API — QA Assignment 1

---

## 1. System Overview

**Habaneras de Lino** is an open-source Django REST Framework backend for an e-commerce clothing store. It exposes a public REST API consumed by a Next.js frontend and includes a custom Django admin panel for store management.

- **Repository:** https://github.com/Ceci-Aguilera/habaneras-de-lino-drf-api
- **Framework:** Django 4.0.6 + DRF 3.13.1
- **Database:** PostgreSQL
- **External services:** Stripe (payments), Cloudinary (image storage)
- **Deployment:** Docker + Nginx

---

## 2. Identified Modules / Components

| # | Module | Description |
|---|--------|-------------|
| M1 | **Order & Checkout Flow** | POST /orders/ — creates an order linked to a cart, address, and Stripe payment |
| M2 | **Stripe Payment Integration** | Processes payment charges via Stripe API; handles refund statuses |
| M3 | **Cart Management** | Create/update/delete product variations in a session cart identified by token |
| M4 | **Product Catalog API** | List and detail endpoints for clothing products with pagination |
| M5 | **Collections & Categories API** | Browsing and filtering by collection name/year and category |
| M6 | **Data Validation & Serializers** | Input validation for all POST/PATCH endpoints |
| M7 | **Admin Panel (admin_app)** | Custom Bootstrap dashboard for managing products, orders, payments |
| M8 | **GlobalModel / Tax Calculation** | Single active record drives currency exchange and US sales tax computation |
| M9 | **Image Upload (Cloudinary)** | Product and collection images uploaded to Cloudinary CDN |
| M10 | **Docker / Nginx Infrastructure** | Container orchestration, reverse proxy, static files serving |

---

## 3. Risk Assessment Matrix

Risk Score = Probability (1–5) × Impact (1–5)

| Module | Probability of Failure | Impact if Fails | Risk Score | Priority |
|--------|----------------------|-----------------|------------|----------|
| M2 — Stripe Payment | 3 | 5 | **15** | 🔴 Critical |
| M1 — Order & Checkout | 4 | 5 | **20** | 🔴 Critical |
| M8 — Tax Calculation | 3 | 4 | **12** | 🔴 High |
| M6 — Data Validation | 4 | 4 | **16** | 🔴 High |
| M3 — Cart Management | 3 | 4 | **12** | 🟠 High |
| M7 — Admin Panel | 2 | 3 | **6** | 🟡 Medium |
| M4 — Product Catalog | 2 | 3 | **6** | 🟡 Medium |
| M9 — Image Upload | 2 | 2 | **4** | 🟢 Low |
| M5 — Collections API | 1 | 2 | **2** | 🟢 Low |
| M10 — Infrastructure | 2 | 5 | **10** | 🟠 Medium |

---

## 4. Detailed Risk Analysis

### M1 — Order & Checkout Flow (Score: 20) 🔴 Critical
**Why critical:** This is the core business transaction. A failure here means lost revenue and broken user experience. The endpoint combines cart validation, address persistence, email notification, and Stripe charge in a single operation — high cyclomatic complexity.

**Failure scenarios:**
- Cart token mismatch or inactive cart accepted
- Missing required fields accepted without error
- Email notification silently fails
- Order created but payment not recorded

**Testing approach:** Integration tests with mock Stripe; unit tests for order state machine.

---

### M6 — Data Validation (Score: 16) 🔴 High
**Why critical:** DRF serializers are the only layer preventing malformed data from reaching the database. Missing or weak validation allows corrupt records, crashes, and security issues.

**Failure scenarios:**
- Negative quantity in ProductVariation accepted
- Invalid color code (#GGGGGG) stored without error
- Zip code longer than 5 digits accepted
- Email field not validated as email format

**Testing approach:** Boundary value tests on all serializers; invalid payloads to all POST endpoints.

---

### M2 — Stripe Payment Integration (Score: 15) 🔴 Critical
**Why critical:** Real money is involved. A bug in charge creation or refund handling causes financial loss or legal exposure.

**Failure scenarios:**
- Double charge on retry
- Refund status not updated after Stripe webhook
- Invalid Stripe key not handled gracefully

**Testing approach:** Unit tests with Stripe mocks; verify error response codes on payment failures.

---

### M8 — Tax & Currency Calculation (Score: 12) 🔴 High
**Why critical:** `GlobalModel` is a singleton — if no active record exists, `pricing_with_tax()` raises an unhandled exception crashing product detail and order creation.

**Failure scenarios:**
- No active GlobalModel → 500 on any pricing call
- Multiple active GlobalModels → ambiguous tax rate
- Wrong MX conversion factor → incorrect pricing displayed

**Testing approach:** Unit tests covering zero, one, and multiple active GlobalModel records.

---

### M3 — Cart Management (Score: 12) 🟠 High
**Why critical:** Cart is the state that carries the purchase through checkout. Stale or incorrect cart state corrupts orders.

**Failure scenarios:**
- Inactive cart accepted for checkout
- Cart token collision between users
- Orphaned ProductVariations after cart deletion

**Testing approach:** Integration tests for cart lifecycle: create → add items → retrieve → checkout.

---

### M10 — Docker/Nginx Infrastructure (Score: 10) 🟠 Medium
**Why medium:** Infrastructure failure prevents all testing and production access, but the configuration is relatively simple and stable.

**Testing approach:** Smoke test — verify app responds after `docker compose up`.

---

## 5. Prioritized Testing Order

1. 🔴 M1 — Order & Checkout Flow
2. 🔴 M6 — Data Validation & Serializers
3. 🔴 M2 — Stripe Payment Integration
4. 🔴 M8 — Tax & Currency Calculation
5. 🟠 M3 — Cart Management
6. 🟠 M10 — Infrastructure smoke test
7. 🟡 M4 — Product Catalog API
8. 🟡 M7 — Admin Panel
9. 🟢 M9 — Image Upload
10. 🟢 M5 — Collections & Categories

---

## 6. Assumptions & Reasoning

- **Stripe integration is untestable in full** without Stripe test keys — tests will use mocks or test-mode keys.
- **Cloudinary** is treated as low risk because image upload failure does not break core purchase flow.
- **Admin panel** is medium risk because it is used internally only; a bug here affects operations, not end-customer revenue.
- **GlobalModel singleton** pattern is considered a design risk — tests must cover the missing-record edge case explicitly.
- No authentication is required for most store API endpoints (public browsing); cart is identified only by token — session fixation is a potential security risk noted but deferred to security testing.
