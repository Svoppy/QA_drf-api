# Baseline Metrics
## Habaneras de Lino DRF API — QA Assignment 1

---

## 1. System Complexity Metrics

| Metric | Value |
|--------|-------|
| Total Django apps | 2 (`store_app`, `admin_app`) |
| Total models | 10 (GlobalModel, CustomColor, ClothingCollection, Category, ClothingProduct, ClothingProductImage, Cart, ProductVariation, Address, Payment, Order) |
| Total API endpoints | 13 |
| External service integrations | 2 (Stripe, Cloudinary) |
| Lines of code (store_app) | ~900 |
| Lines of code (admin_app) | ~300 |

---

## 2. Risk Module Count

| Risk Level | Module Count | Modules |
|------------|-------------|---------|
| 🔴 Critical (score ≥ 15) | 3 | Order & Checkout, Data Validation, Stripe Payment |
| 🟠 High (score 10–14) | 3 | Tax Calculation, Cart Management, Infrastructure |
| 🟡 Medium (score 5–9) | 2 | Admin Panel, Product Catalog |
| 🟢 Low (score < 5) | 2 | Image Upload, Collections API |
| **Total** | **10** | |

---

## 3. API Endpoint Inventory

| # | Method | Endpoint | Risk Priority |
|---|--------|----------|---------------|
| 1 | GET | `/clothing-products/<page>/` | Medium |
| 2 | GET | `/clothing-products/items/<id>/` | Medium |
| 3 | GET | `/clothing-collections/` | Low |
| 4 | GET | `/clothing-collections/filter/names/` | Low |
| 5 | GET | `/clothing-collections/<id>/` | Low |
| 6 | GET | `/categories/` | Low |
| 7 | GET | `/categories/<id>/` | Low |
| 8 | GET | `/categories/filter/names/` | Low |
| 9 | POST | `/product-variations/` | High |
| 10 | GET | `/cart/<token>/` | High |
| 11 | GET/PATCH/DELETE | `/product-variations/<id>/` | High |
| 12 | POST | `/orders/` | **Critical** |
| 13 | POST | `/stripe-webhook/` | **Critical** |

---

## 4. Initial Coverage Plan

| Module | Planned Test Count | Type | Coverage Target |
|--------|-------------------|------|----------------|
| Order & Checkout (M1) | 8 | Integration | 90% |
| Data Validation (M6) | 15 | Unit + Integration | 100% |
| Stripe / Payment (M2) | 4 | Unit (mock) | 80% |
| Tax Calculation (M8) | 5 | Unit | 100% |
| Cart Management (M3) | 6 | Integration | 80% |
| Product Catalog (M4) | 6 | Integration | 80% |
| Admin Panel (M7) | 3 | E2E | 70% |
| Infrastructure (M10) | 1 | Smoke | 100% |
| **Total planned** | **48** | | |

---

## 5. Tests Written (Assignment 1 Baseline)

| Test File | Tests Written | Type |
|-----------|--------------|------|
| `tests/unit/test_models.py` | 9 | Unit |
| `tests/integration/test_api_endpoints.py` | 14 | Integration |
| `tests/e2e/test_admin_panel.py` | 4 | E2E |
| **Total** | **27** | |

**Coverage baseline (unit tests only, no running app):**
- `store_app/models.py` — targeted by 9 unit tests
- Estimated line coverage at baseline: ~25% (unit tests only cover model layer)
- Target after all assignments: ≥ 60%

---

## 6. Estimated Testing Effort

| Activity | Estimated Effort |
|----------|----------------|
| Risk assessment & strategy | 4 hours |
| Environment setup (Docker + CI) | 3 hours |
| Unit test writing | 4 hours |
| Integration test writing | 5 hours |
| E2E test writing | 3 hours |
| Documentation | 4 hours |
| **Total Assignment 1** | **~23 hours** |

---

## 7. Defect Baseline (Pre-Testing)

No defects identified yet — formal defect tracking begins in Assignment 2 when tests are executed against a running instance. Known risk areas to watch:

| Risk Area | Known Design Concern |
|-----------|---------------------|
| GlobalModel singleton | `get(active=True)` will crash if 0 or 2+ active records exist |
| Cart token | No authentication; collision risk between users |
| Order endpoint | No idempotency key — retry could create duplicate orders |
| Stripe webhook | No signature verification visible in code |

---

## 8. Metrics Collection Plan

These metrics will be tracked across assignments to measure QA effectiveness:

| Metric | Tool | Collected In |
|--------|------|-------------|
| Line coverage % | pytest-cov | Every CI run |
| Test pass rate | GitHub Actions | Every push |
| Defects found per module | Manual log | Assignment 2+ |
| Defect fix rate | GitHub Issues | Assignment 3+ |
| API response time | requests.elapsed | Assignment 2 |
