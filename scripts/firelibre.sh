#!/usr/bin/env bash
set -euo pipefail
FIRELIBRE_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
exec python3 "$FIRELIBRE_ROOT/firelibre.py" "$@"
