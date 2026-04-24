# Assignment 3 Experimental Engineering

This folder documents the implemented performance, mutation, and chaos testing layer for the active SUT:

`sut/habaneras-de-lino-drf-api`

The older `sut/` project copy is not used by the current pytest and CI configuration.

## Scope

Assignment 3 covers:

- Performance testing under normal, load, peak, and short endurance scenarios.
- Mutation testing for functional Python files.
- Chaos/fault injection testing for API downtime, DB unavailable, and DB latency.
- Weekly GitHub Actions execution with artifacts.

## Implemented Files

| Area | Files |
|---|---|
| Performance | `tests/performance/assignment3_scenarios.js`, `scripts/experiment/run_performance.ps1` |
| Mutation | `setup.cfg`, `requirements-experiment.txt`, `scripts/experiment/run_mutation.py` |
| Chaos | `sut/habaneras-de-lino-drf-api/docker-compose.chaos.yml`, `sut/habaneras-de-lino-drf-api/toxiproxy.json`, `scripts/experiment/run_chaos.py` |
| Docker/seed | `sut/habaneras-de-lino-drf-api/docker-compose.experiment.yml`, `store_app/management/commands/seed_experiment_data.py`, updated `entrypoint.sh` |
| Defense scripts | `scripts/experiment/run_defense_full.ps1`, `scripts/experiment/start_experiment_stack.ps1`, `scripts/experiment/seed_experiment_data.ps1`, `scripts/experiment/stop_experiment_stack.ps1` |
| Summary | `scripts/experiment/build_summary.py`, `artifacts/summary.md` |
| CI cron | `.github/workflows/experimental-weekly.yml` |

## One-Command Defense Run

From the repository root:

```powershell
.\scripts\experiment\run_defense_full.ps1
```

This command starts the Docker experiment stack, seeds data, runs unit and integration checks, executes all four performance scenarios, runs mutation testing in an isolated Linux container, injects the required chaos faults with 20 probes each, writes test artifacts, builds `artifacts/summary.md`, and stops the stack at the end.

For a shorter live demonstration of the same flow, use:

```powershell
.\scripts\experiment\run_defense_full.ps1 -Mode Demo
```

To rebuild the consolidated table from existing artifacts only:

```powershell
python scripts\experiment\build_summary.py --output artifacts\summary.md
```

## Performance Testing

Tool: k6.

Implemented scenarios:

| Scenario | Purpose | Default settings |
|---|---|---|
| normal | Expected regular traffic | 5 VU, 3 minutes |
| load | Sustained working load | 20 VU, 5 minutes |
| peak | Peak traffic with ramp-up | 5 to 50 VU, 3-minute hold |
| endurance | Short stability run | 15 VU, 10 minutes |

Covered endpoints:

- `GET /store/clothing-products/<page>/`
- `GET /store/clothing-products/items/<id>/`
- `GET /store/clothing-collections/`
- `GET /store/categories/`
- `GET /store/cart/<token>/`
- `POST /store/product-variations/`
- `POST /store/orders/` with controlled validation-failure payload only.

The order endpoint is intentionally exercised as a validation/failure path so performance tests do not depend on live Stripe.

Main metrics:

- average response time
- median response time
- p95 / p99 response time
- requests per second
- throughput
- HTTP error rate
- failed checks

Local example:

```powershell
cd "C:\Users\nurym\Documents\AQA mid term\QA_drf-api"
.\scripts\experiment\run_performance.ps1 -Scenario normal -BaseUrl http://host.docker.internal:8002
```

Direct k6 example:

```bash
k6 run -e BASE_URL=http://localhost:8002 -e SCENARIO=load tests/performance/assignment3_scenarios.js
```

## Mutation Testing

Tool: mutmut.

Mutation targets:

- `store_app/fields.py`
- `store_app/models.py`
- `store_app/serializers.py`
- `store_app/views.py`
- `admin_app/views.py`

Excluded:

- migrations
- settings
- static files
- templates
- Django admin registration

Mutation flow:

1. Run baseline unit tests.
2. Run mutmut against the configured functional files.
3. Export `mutmut-run.txt` and `mutmut-results.txt`.
4. Export `mutation-summary.json` with killed, survived, timeout, suspicious, skipped, and untested counts.
5. Review survived mutants.
6. Add tests for meaningful survivors.
7. Re-run mutation testing.

Local example:

```bash
cd "/mnt/c/Users/nurym/Documents/AQA mid term/QA_drf-api"
python -m pip install -r requirements-experiment.txt
python scripts/experiment/run_mutation.py --output-dir artifacts/mutation
```

Note: mutmut does not support native Windows execution. Run mutation testing in WSL/Linux or through the GitHub Actions weekly workflow.

## Chaos / Fault Injection Testing

Tooling:

- Docker Compose
- Toxiproxy between Django API and PostgreSQL
- `scripts/experiment/run_chaos.py`

Implemented scenarios:

| Scenario | Minimum probes | Fault |
|---|---:|---|
| API downtime | 20 | Stop/start `api` container |
| DB unavailable | 20 | Disable PostgreSQL proxy |
| DB latency | 20 | Add 1000 ms latency toxic |

Metrics:

- availability during fault
- request status distribution
- request duration
- recovery time
- recovered probes

Local flow:

```powershell
cd "C:\Users\nurym\Documents\AQA mid term\QA_drf-api\sut\habaneras-de-lino-drf-api"
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.experiment.yml -f docker-compose.chaos.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.experiment.yml -f docker-compose.chaos.yml exec -T api python manage.py seed_experiment_data --products 120 --carts 20
```

Then from repository root:

```powershell
python scripts\experiment\run_chaos.py --scenario all --probes 20 --output-dir artifacts\chaos
```

The runner rejects values below `--probes 20` to keep Assignment 3 evidence complete.

## GitHub Actions Weekly Cron

Workflow:

`.github/workflows/experimental-weekly.yml`

Triggers:

```yaml
workflow_dispatch:
schedule:
  - cron: "0 3 * * 1"
```

This runs every Monday at 03:00 UTC and can also be launched manually.

Pipeline stages:

1. Install dependencies.
2. Start Docker experiment stack.
3. Seed experiment data.
4. Run preflight unit and integration smoke tests.
5. Run performance scenarios: normal, load, peak, endurance.
6. Run mutation testing.
7. Run chaos probes: API downtime, DB unavailable, DB latency, 20 probes each.
8. Build the consolidated `artifacts/summary.md`.
9. Upload artifacts.

## Expected Artifacts

| Artifact path | Contents |
|---|---|
| `artifacts/performance/*.json` | k6 summaries |
| `artifacts/mutation/*.txt` | baseline and mutmut output |
| `artifacts/mutation/mutation-summary.json` | mutation counts and mutation score |
| `artifacts/mutation/summary.md` | mutation target summary |
| `artifacts/chaos/chaos-results.csv` | per-probe chaos results |
| `artifacts/chaos/chaos-summary.json` | aggregated chaos metrics |
| `artifacts/chaos/summary.md` | report-friendly chaos summary |
| `artifacts/summary.md` | consolidated table for unit, integration, performance, mutation, and chaos results |
| `artifacts/docker/compose.log` | Docker logs for debugging |
