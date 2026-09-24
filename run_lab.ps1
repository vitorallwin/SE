$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
& $venvPython -m pip install -r requirements.txt --disable-pip-version-check
Start-Process "http://127.0.0.1:8765"
& $venvPython lab_server.py
