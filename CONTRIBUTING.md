# Contribuir a FireLibre

Gracias por aportar evidencia, código o documentación. Las contribuciones se publican bajo
la licencia del proyecto, respetando las licencias de código integrado.

## Preparar un cambio

1. Abre una incidencia para un dispositivo, error o propuesta concreta.
2. Trabaja en una rama y conserva un alcance revisable.
3. Actualiza las guías y el changelog cuando cambie el comportamiento.
4. No incluyas estado real, datos personales, APK, credenciales ni claves de firma en Git.

Para un paquete nuevo aporta modelo, SDK, firmware, función conocida, comando aceptado,
estado previo, restauración y pruebas de funciones. Si no se conoce su función, dilo;
no uses el nombre como única evidencia. Nuevos modelos permanecen experimentales hasta
que se documenten los resultados relevantes.

## Comprobaciones locales

```bash
python3 -m unittest discover -s tests
python3 scripts/check_repo.py
python3 -m compileall -q firelibre firelibre.py scripts tests
for script in scripts/*.sh integrations/dumbtv/build.sh; do bash -n "$script"; done
```

Las pruebas no deben contactar a un TV. Si cambias las rutas de aplicación o
recuperación, añade casos de interrupción y conflicto. No basta con probar el camino correcto.

Para cambios Java/recursos ejecuta `bash scripts/build-launcher.sh` con SDK/JDK, verifica el
manifiesto y los recursos y explica las pruebas físicas que hiciste realmente. No publiques
una clave. No actualices un hash del catálogo a un archivo diferente sin explicar su origen.

## Licencias e integraciones

Conserva `integrations/dumbtv/LICENSE` y registra cambios en `UPSTREAM.json`. Un launcher nuevo
empieza como referencia documentada; no se automatiza la desactivación de otro controlador sin
un plan, copia, detección de conflictos y recuperación.

## Describir una propuesta

Explica el problema, el comportamiento final y cómo se comprobó. Para hardware indica modelo,
SDK, firmware y pruebas, sin IP ni identificadores. Usa la plantilla de pull request.
