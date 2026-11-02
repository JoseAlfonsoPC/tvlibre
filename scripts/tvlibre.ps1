$ErrorActionPreference = 'Stop'
$TVLibreRoot = Split-Path -Parent $PSScriptRoot
python (Join-Path $TVLibreRoot 'tvlibre.py') @args
exit $LASTEXITCODE
