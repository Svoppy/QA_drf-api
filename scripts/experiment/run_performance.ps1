param(
    [ValidateSet("normal", "load", "peak", "endurance")]
    [string]$Scenario = "normal",
    [string]$BaseUrl = "http://host.docker.internal:8002",
    [string]$OutputDir = "artifacts/performance",
    [string]$K6Image = "grafana/k6:0.49.0"
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$summaryPath = Join-Path $OutputDir "$Scenario-summary.json"
$summaryPathDocker = $summaryPath.Replace("\", "/")
$scriptPath = "/work/tests/performance/assignment3_scenarios.js"

docker run --rm `
    --network host `
    -e BASE_URL=$BaseUrl `
    -e SCENARIO=$Scenario `
    -v "${repoRoot}:/work" `
    -w /work `
    $K6Image run `
    --summary-export "/work/$summaryPathDocker" `
    $scriptPath
