#!/usr/bin/env bash
# Compila desde el código MIT integrado. No instala nada en un televisor.
set -euo pipefail
umask 077
FIRELIBRE_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
"$FIRELIBRE_ROOT/integrations/dumbtv/build.sh"
mkdir -p "$FIRELIBRE_ROOT/dist"
cp "$FIRELIBRE_ROOT/integrations/dumbtv/build/dumbtv-home.apk" "$FIRELIBRE_ROOT/dist/dumbtv-home-1.6-es.apk"
printf 'APK compilado en dist/dumbtv-home-1.6-es.apk. Conserva tu clave de firma privada.\n'
