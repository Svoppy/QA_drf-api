# Assignment 3 Local Validation Summary

Validation date: 2026-04-24

## Static and Configuration Checks

| Check | Result |
|---|---|
| Python compile for experiment scripts | Passed |
| Docker Compose config with experiment and chaos overrides | Passed |
| GitHub Actions YAML parse | Passed |
| k6 script inspect | Passed |
| Management command registration | Passed |

## Unit and Integration Checks

| Suite | Result |
|---|---|
| Unit tests | 26 passed |
| Integration smoke (`test_api_endpoints.py`, `test_response_times.py`) | 19 passed |

## Docker and Seed Checks

| Check | Result |
|---|---|
| Experiment stack started with Toxiproxy | Passed |
| SUT health endpoint | HTTP 200 |
| `seed_experiment_data` command | Seeded 30 products, 10 categories, 5 collections, 5 carts |

## Performance Smoke

Short k6 smoke was run with:

- scenario: `normal`
- VUs: 1
- duration: 5 seconds

Result:

| Metric | Value |
|---|---:|
| Checks | 100% |
| HTTP failures | 0% |
| p95 response time | 306.58 ms |
| Requests | 25 |

## Mutation Smoke

Mutation runner was validated in a Linux container because native Windows execution is not suitable for mutmut.

Validated target:

- `store_app/fields.py`

Result:

- mutmut 2.5.x starts with the configured subprocess runner.
- Baseline tests run through `python -m pytest tests/unit/`.
- `mutmut results` artifacts are generated.
- The full weekly workflow runs all configured mutation targets and writes `mutation-summary.json`.

## Chaos Validation

The chaos runner was executed locally with 20 probes per scenario.

Settings:

- API downtime fault duration: 1 second
- DB unavailable fault duration: 1 second
- DB latency: 500 ms plus 50 ms jitter

| Scenario | Probes | Recovered | Availability During Fault | Mean Recovery | Statuses |
|---|---:|---:|---:|---:|---|
| API downtime | 20 | 20/20 | 0.0% | 4.41s | `ReadTimeout: 20` |
| DB unavailable | 20 | 20/20 | 0.0% | 0.26s | `500: 20` |
| DB latency | 20 | 20/20 | 0.0% | 0.28s | `ReadTimeout: 20` |

Post-chaos health check returned HTTP 200.

