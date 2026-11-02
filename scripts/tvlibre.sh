#!/usr/bin/env bash
set -euo pipefail
TVLIBRE_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
exec python3 "$TVLIBRE_ROOT/tvlibre.py" "$@"
