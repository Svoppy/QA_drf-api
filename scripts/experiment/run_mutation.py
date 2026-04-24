import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MUTATION_PATHS = [
    "sut/habaneras-de-lino-drf-api/store_app/fields.py",
    "sut/habaneras-de-lino-drf-api/store_app/models.py",
    "sut/habaneras-de-lino-drf-api/store_app/serializers.py",
    "sut/habaneras-de-lino-drf-api/store_app/views.py",
    "sut/habaneras-de-lino-drf-api/admin_app/views.py",
]


def run(command, output_file=None, check=True):
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
    )
    if output_file:
        output_file.write_text(result.stdout, encoding="utf-8")
    else:
        print(result.stdout)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result


def count_result_ids(status, output_dir):
    result = run(
        [sys.executable, "-m", "mutmut", "result-ids", status],
        output_file=output_dir / f"mutmut-{status}-ids.txt",
        check=False,
    )
    return len([item for item in result.stdout.split() if item.strip()])


def main():
    parser = argparse.ArgumentParser(description="Run Assignment 3 mutation testing with mutmut.")
    parser.add_argument("--output-dir", default="artifacts/mutation")
    parser.add_argument("--skip-baseline", action="store_true")
    parser.add_argument("--target", default=None, help="Optional mutmut target pattern, e.g. store_app.models*")
    parser.add_argument(
        "--paths-to-mutate",
        default=",".join(DEFAULT_MUTATION_PATHS),
        help="Comma-separated file paths for mutmut, defaulting to Assignment 3 functional targets.",
    )
    args = parser.parse_args()

    output_dir = (ROOT / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habaneras_de_lino_drf_api.settings.test")
    pythonpath = str(ROOT / "sut" / "habaneras-de-lino-drf-api")
    os.environ["PYTHONPATH"] = pythonpath + os.pathsep + os.environ.get("PYTHONPATH", "")

    if not args.skip_baseline:
        run(
            [sys.executable, "-m", "pytest", "tests/unit/", "-q"],
            output_file=output_dir / "baseline-unit-tests.txt",
        )

    mutmut_command = [
        sys.executable,
        "-m",
        "mutmut",
        "run",
        "--CI",
        f"--paths-to-mutate={args.paths_to_mutate}",
    ]
    if args.target:
        mutmut_command.append(args.target)

    run(mutmut_command, output_file=output_dir / "mutmut-run.txt", check=False)
    run([sys.executable, "-m", "mutmut", "results"], output_file=output_dir / "mutmut-results.txt", check=False)

    counts = {
        status: count_result_ids(status, output_dir)
        for status in ("killed", "survived", "timeout", "suspicious", "skipped", "untested")
    }
    score_denominator = counts["killed"] + counts["survived"] + counts["timeout"] + counts["suspicious"]
    counts["mutation_score_percent"] = (
        round(((counts["killed"] + counts["timeout"]) / score_denominator) * 100, 2)
        if score_denominator
        else 0.0
    )
    (output_dir / "mutation-summary.json").write_text(
        json.dumps(counts, indent=2),
        encoding="utf-8",
    )

    summary = [
        "# Assignment 3 Mutation Testing Summary",
        "",
        "Targets:",
        *[f"- {path}" for path in args.paths_to_mutate.split(",") if path.strip()],
        "",
        "Generated files:",
        "- baseline-unit-tests.txt",
        "- mutmut-run.txt",
        "- mutmut-results.txt",
        "- mutation-summary.json",
        "",
        "Metrics:",
        f"- Killed: {counts['killed']}",
        f"- Survived: {counts['survived']}",
        f"- Timeout: {counts['timeout']}",
        f"- Suspicious: {counts['suspicious']}",
        f"- Skipped: {counts['skipped']}",
        f"- Untested: {counts['untested']}",
        f"- Mutation score: {counts['mutation_score_percent']}%",
        "",
        "Review survived mutants in mutmut-results.txt and strengthen tests for meaningful survivors.",
    ]
    (output_dir / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
