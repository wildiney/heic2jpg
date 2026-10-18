# Build single-file heic2jpg.exe and install to C:\tools (must be on PATH).
param([string]$InstallDir = "C:\tools")
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

python -m pip install -q -e ".[dev]"
python -m PyInstaller --onefile --clean --noconfirm --name heic2jpg `
    --paths src --collect-all pillow_heif entry.py
if ($LASTEXITCODE) { throw "PyInstaller failed" }

New-Item -ItemType Directory -Force $InstallDir | Out-Null
Copy-Item dist\heic2jpg.exe $InstallDir -Force
Write-Host "Installed: $InstallDir\heic2jpg.exe"
