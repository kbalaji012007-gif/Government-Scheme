# RuralConnect Karnataka - Backend Launcher
Set-Location -Path $PSScriptRoot

if (Test-Path ".\.venv\Scripts\python.exe") {
    Write-Host "Starting FastAPI backend using virtual environment..." -ForegroundColor Green
    & ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
} else {
    Write-Host "Starting FastAPI backend using system Python..." -ForegroundColor Green
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
}
