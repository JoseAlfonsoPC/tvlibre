$ErrorActionPreference = 'Stop'
$FireLibreRoot = Split-Path -Parent $PSScriptRoot
python (Join-Path $FireLibreRoot 'firelibre.py') @args
exit $LASTEXITCODE
