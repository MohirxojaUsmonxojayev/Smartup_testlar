Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

if (-not $env:TELEGRAM_BOT_TOKEN) {
    throw "TELEGRAM_BOT_TOKEN environment variable is required."
}

if (-not $env:TELEGRAM_CHAT_ID -and -not $env:TELEGRAM_ALLOWED_CHAT_IDS) {
    throw "TELEGRAM_CHAT_ID or TELEGRAM_ALLOWED_CHAT_IDS environment variable is required."
}

if (-not $env:GITHUB_TOKEN -and -not $env:GITHUB_PAT) {
    throw "GITHUB_TOKEN or GITHUB_PAT environment variable is required."
}

if (-not $env:GITHUB_REPOSITORY) {
    $env:GITHUB_REPOSITORY = "turgunovjasur/Playwright"
}

if (-not $env:GITHUB_WORKFLOW_FILE) {
    $env:GITHUB_WORKFLOW_FILE = "daily-smoke.yml"
}

if (-not $env:GITHUB_REF) {
    $env:GITHUB_REF = "main"
}

if (-not $env:DEFAULT_SERVER_URL) {
    $env:DEFAULT_SERVER_URL = "https://smartup.online/"
}

if (-not $env:ALLOWED_SERVER_URLS) {
    $env:ALLOWED_SERVER_URLS = "https://smartup.online"
}

$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    & $VenvPython "scripts\telegram_ci_bot.py"
}
else {
    & python "scripts\telegram_ci_bot.py"
}
