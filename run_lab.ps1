$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Mesmo Python do run.ps1; depois o launcher "py"; por último o "python" do PATH.
$bundledPython = "C:\Users\POPULOS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path $bundledPython) {
    $python = @($bundledPython)
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $python = @("py", "-3")
} else {
    $python = @("python")
}

$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    # .venv incompleto (criação anterior falhou): recria do zero.
    if (Test-Path ".venv") { Remove-Item ".venv" -Recurse -Force }
    Write-Host "Criando .venv com: $($python -join ' ')"
    $exe, $extra = $python
    & $exe @extra -m venv .venv
    if (-not (Test-Path $venvPython)) {
        throw "Não foi possível criar o .venv. Instale o Python 3.11+ (python.org, marque 'Add to PATH') e rode de novo."
    }
}

& $venvPython -m pip install -r requirements.txt --disable-pip-version-check
if ($LASTEXITCODE -ne 0) { throw "pip install falhou" }
Start-Process "http://127.0.0.1:8765"
& $venvPython lab_server.py
