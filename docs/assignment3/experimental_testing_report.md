# Assignment 3 Experimental Testing Report

## System Under Test

The system under test is the Habaneras de Lino Django REST Framework API located in `sut/habaneras-de-lino-drf-api`. The tested modules are selected from the current risk model:

| Module | Reason |
|---|---|
| M1 Order and Checkout | Critical business flow and Stripe-adjacent failure handling |
| M2 Stripe Payment Integration | External dependency risk, tested through controlled failure paths |
| M3 Cart Management | Stateful token-based cart behavior |
| M4 Product Catalog API | High-read traffic surface |
| M5 Collections and Categories API | Read-heavy nested serialization |
| M6 Data Validation | Prevents malformed data from reaching persistence |
| M7 Admin Panel | Operational interface |
| M8 Tax and Currency Calculation | Pricing correctness and singleton configuration risk |
| M10 Docker/Nginx Infrastructure | Required for integration, performance, and chaos tests |

## Performance Testing Methodology

Performance testing is implemented with k6 in `tests/performance/assignment3_scenarios.js`.

Only four scenarios are used:

| Scenario | Load profile | Purpose |
|---|---|---|
| normal | 5 VU for 3 minutes | Expected traffic |
| load | 20 VU for 5 minutes | Sustained working load |
| peak | Ramp to 50 VU, hold, recover | Peak traffic behavior |
| endurance | 15 VU for 10 minutes | Short stability check |

The workload uses a realistic mix:

- 70% catalog browsing
- 20% cart operations
- 10% controlled order validation failures

The checkout endpoint is not charged through live Stripe during performance testing.

## Mutation Testing Methodology

Mutation testing is implemented with mutmut and targets only functional files:

- `store_app/fields.py`
- `store_app/models.py`
- `store_app/serializers.py`
- `store_app/views.py`
- `admin_app/views.py`

The mutation score should be calculated from:

```text
killed mutants / (killed mutants + survived mutants) * 100
```

Survived mutants should be reviewed manually. Equivalent mutants should be documented separately and not treated as useful missing coverage.

The weekly workflow runs mutation testing on Ubuntu because mutmut does not support native Windows execution.

## Chaos Testing Methodology

Chaos testing is implemented with Docker Compose and Toxiproxy.

Three fault types are used:

| Fault | Probes | Expected observation |
|---|---:|---|
| API downtime | 20 | Nginx/API failure response followed by recovery |
| DB unavailable | 20 | Controlled DB failure and recovery |
| DB latency | 20 | Higher response time and possible error propagation |

Each probe follows this flow:

1. Confirm baseline health.
2. Inject the fault.
3. Send a representative request.
4. Remove the fault.
5. Measure recovery time.
6. Store per-probe metrics.

## Reproducibility

The weekly GitHub Actions workflow runs the full experiment suite every Monday:

`.github/workflows/experimental-weekly.yml`

It uploads performance, mutation, chaos, and Docker log artifacts for report evidence.

## Metrics To Report

| Category | Metrics |
|---|---|
| Performance | avg, median, p95, p99, RPS, error rate, throughput |
| Mutation | created, killed, survived, timeout, mutation score |
| Chaos | availability %, recovery time, error status distribution, latency during fault |

## Recommendations Section

Recommended follow-up analysis after the first full weekly run:

1. Compare p95 and p99 across normal/load/peak/endurance.
2. Identify whether nested serializers in catalog endpoints create bottlenecks.
3. Review survived mutants in validation and order-payment rollback paths.
4. Compare API downtime recovery time against DB fault recovery time.
5. Convert meaningful survived mutants into new unit or integration tests.
