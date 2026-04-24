import argparse
import csv
import json
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[2]
SUT_DIR = ROOT / "sut" / "habaneras-de-lino-drf-api"
PROXY_NAME = "assignment3_postgres"


@dataclass
class ProbeResult:
    scenario: str
    probe: int
    fault_seconds: float
    request_status: str
    request_ms: float
    recovery_seconds: float
    recovered: bool
    note: str = ""


def compose(args, check=True):
    command = [
        "docker",
        "compose",
        "-f",
        "docker-compose.yml",
        "-f",
        "docker-compose.override.yml",
        "-f",
        "docker-compose.experiment.yml",
        "-f",
        "docker-compose.chaos.yml",
        *args,
    ]
    return subprocess.run(command, cwd=SUT_DIR, check=check, text=True)


def request_health(base_url, timeout=5):
    started = time.perf_counter()
    try:
        response = requests.get(f"{base_url}/store/clothing-collections/", timeout=timeout)
        elapsed_ms = (time.perf_counter() - started) * 1000
        return str(response.status_code), elapsed_ms
    except requests.RequestException as exc:
        elapsed_ms = (time.perf_counter() - started) * 1000
        return exc.__class__.__name__, elapsed_ms


def wait_until_healthy(base_url, timeout_seconds):
    started = time.perf_counter()
    while time.perf_counter() - started < timeout_seconds:
        status, _ = request_health(base_url, timeout=3)
        if status == "200":
            return True, time.perf_counter() - started
        time.sleep(2)
    return False, time.perf_counter() - started


def toxiproxy_url(path, host):
    return f"{host.rstrip('/')}{path}"


def reset_toxiproxy(host):
    requests.post(toxiproxy_url("/reset", host), timeout=5)


def set_proxy_enabled(host, enabled):
    response = requests.post(
        toxiproxy_url(f"/proxies/{PROXY_NAME}", host),
        json={"enabled": enabled},
        timeout=5,
    )
    response.raise_for_status()


def clear_latency(host):
    requests.delete(
        toxiproxy_url(f"/proxies/{PROXY_NAME}/toxics/a3_latency", host),
        timeout=5,
    )


def add_latency(host, latency_ms, jitter_ms):
    clear_latency(host)
    response = requests.post(
        toxiproxy_url(f"/proxies/{PROXY_NAME}/toxics", host),
        json={
            "name": "a3_latency",
            "type": "latency",
            # Upstream latency delays request forwarding and gives a realistic degradation profile.
            "stream": "upstream",
            "toxicity": 1.0,
            "attributes": {"latency": latency_ms, "jitter": jitter_ms},
        },
        timeout=5,
    )
    response.raise_for_status()


def api_downtime_probe(base_url, probe, fault_seconds, recovery_timeout):
    compose(["stop", "api"])
    time.sleep(fault_seconds)
    status, request_ms = request_health(base_url, timeout=5)
    compose(["start", "api"])
    recovered, recovery_seconds = wait_until_healthy(base_url, recovery_timeout)
    return ProbeResult(
        scenario="api_downtime",
        probe=probe,
        fault_seconds=fault_seconds,
        request_status=status,
        request_ms=request_ms,
        recovery_seconds=recovery_seconds,
        recovered=recovered,
    )


def db_unavailable_probe(base_url, proxy_host, probe, fault_seconds, recovery_timeout):
    set_proxy_enabled(proxy_host, False)
    time.sleep(fault_seconds)
    status, request_ms = request_health(base_url, timeout=5)
    set_proxy_enabled(proxy_host, True)
    recovered, recovery_seconds = wait_until_healthy(base_url, recovery_timeout)
    return ProbeResult(
        scenario="db_unavailable",
        probe=probe,
        fault_seconds=fault_seconds,
        request_status=status,
        request_ms=request_ms,
        recovery_seconds=recovery_seconds,
        recovered=recovered,
    )


def db_latency_probe(base_url, proxy_host, probe, latency_ms, jitter_ms, recovery_timeout):
    add_latency(proxy_host, latency_ms, jitter_ms)
    status, request_ms = request_health(base_url, timeout=30)
    clear_latency(proxy_host)
    recovered, recovery_seconds = wait_until_healthy(base_url, recovery_timeout)
    return ProbeResult(
        scenario="db_latency",
        probe=probe,
        fault_seconds=latency_ms / 1000,
        request_status=status,
        request_ms=request_ms,
        recovery_seconds=recovery_seconds,
        recovered=recovered,
        note=f"latency_ms={latency_ms};jitter_ms={jitter_ms}",
    )


def write_results(output_dir, results):
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [asdict(result) for result in results]

    with (output_dir / "chaos-results.csv").open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {}
    for scenario in sorted({result.scenario for result in results}):
        selected = [result for result in results if result.scenario == scenario]
        recovered = sum(1 for result in selected if result.recovered)
        statuses = {}
        for result in selected:
            statuses[result.request_status] = statuses.get(result.request_status, 0) + 1
        summary[scenario] = {
            "probes": len(selected),
            "recovered": recovered,
            "availability_during_fault_percent": round(
                100 * sum(1 for result in selected if result.request_status == "200") / len(selected),
                2,
            ),
            "mean_recovery_seconds": round(
                sum(result.recovery_seconds for result in selected) / len(selected),
                2,
            ),
            "mean_request_ms": round(
                sum(result.request_ms for result in selected) / len(selected),
                2,
            ),
            "statuses": statuses,
        }

    (output_dir / "chaos-summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    lines = ["# Assignment 3 Chaos Testing Summary", ""]
    for scenario, data in summary.items():
        lines.append(f"## {scenario}")
        lines.append(f"- Probes: {data['probes']}")
        lines.append(f"- Recovered: {data['recovered']}/{data['probes']}")
        lines.append(f"- Availability during fault: {data['availability_during_fault_percent']}%")
        lines.append(f"- Mean recovery: {data['mean_recovery_seconds']}s")
        lines.append(f"- Mean request time: {data['mean_request_ms']}ms")
        lines.append(f"- Statuses: {data['statuses']}")
        lines.append("")
    (output_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run Assignment 3 Docker chaos probes.")
    parser.add_argument("--base-url", default="http://localhost:8002")
    parser.add_argument("--toxiproxy-url", default="http://localhost:8474")
    parser.add_argument("--scenario", choices=["all", "api_downtime", "db_unavailable", "db_latency"], default="all")
    parser.add_argument("--probes", type=int, default=20)
    parser.add_argument("--fault-seconds", type=float, default=2.0)
    parser.add_argument("--latency-ms", type=int, default=100)
    parser.add_argument("--jitter-ms", type=int, default=20)
    parser.add_argument("--recovery-timeout", type=int, default=90)
    parser.add_argument("--output-dir", default="artifacts/chaos")
    parser.add_argument("--manage-stack", action="store_true")
    args = parser.parse_args()

    if args.probes < 20:
        raise SystemExit("Assignment 3 chaos testing requires at least 20 probes per selected scenario.")

    output_dir = (ROOT / args.output_dir).resolve()
    results = []

    if args.manage_stack:
        compose(["up", "-d", "--build"])
        healthy, seconds = wait_until_healthy(args.base_url, args.recovery_timeout)
        if not healthy:
            raise SystemExit(f"SUT did not become healthy after {seconds:.1f}s.")

    try:
        reset_toxiproxy(args.toxiproxy_url)
        scenarios = (
            ["api_downtime", "db_unavailable", "db_latency"]
            if args.scenario == "all"
            else [args.scenario]
        )

        for scenario in scenarios:
            for probe in range(1, args.probes + 1):
                if scenario == "api_downtime":
                    result = api_downtime_probe(
                        args.base_url,
                        probe,
                        args.fault_seconds,
                        args.recovery_timeout,
                    )
                elif scenario == "db_unavailable":
                    result = db_unavailable_probe(
                        args.base_url,
                        args.toxiproxy_url,
                        probe,
                        args.fault_seconds,
                        args.recovery_timeout,
                    )
                else:
                    result = db_latency_probe(
                        args.base_url,
                        args.toxiproxy_url,
                        probe,
                        args.latency_ms,
                        args.jitter_ms,
                        args.recovery_timeout,
                    )
                results.append(result)
                print(asdict(result), flush=True)
                wait_until_healthy(args.base_url, args.recovery_timeout)
    finally:
        if results:
            write_results(output_dir, results)
        reset_toxiproxy(args.toxiproxy_url)
        if args.manage_stack:
            compose(["down"])


if __name__ == "__main__":
    main()
