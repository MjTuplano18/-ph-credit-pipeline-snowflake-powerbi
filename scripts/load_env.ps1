# FILE: load_env.ps1
# PURPOSE: Load .env values into the current PowerShell session
# PHASE: 1
# DEPENDS ON: .env in the repo root
# OUTPUTS: Environment variables available to dbt and Python scripts

$envFile = Join-Path $PSScriptRoot "..\.env"

if (-not (Test-Path $envFile)) {
  Write-Error "Missing .env. Create it from .env.example and fill in Snowflake values."
  exit 1
}

$lines = Get-Content $envFile
foreach ($line in $lines) {
  if ($line -match '^\s*$' -or $line -match '^\s*#') {
    continue
  }

  if ($line -match '^\s*([^=]+)=(.*)$') {
    $name = $matches[1].Trim()
    $value = $matches[2].Trim()
    [Environment]::SetEnvironmentVariable($name, $value, "Process")
  }
}

Write-Host "Loaded .env into the current session."