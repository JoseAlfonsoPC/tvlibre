# dumbtv Home integrado en FireLibre

Código de [dumbtv](https://github.com/humblemuzzu/dumbtv), bajo MIT. Conserva su autoría,
paquete `tv.dumbtv.home` y mecanismo de inicio. La adaptación añade recursos españoles,
extrae textos Java a recursos y usa versión local `1.6-es` (código 8).

Consulta [UPSTREAM.json](UPSTREAM.json) para la revisión de origen y [LICENSE](LICENSE)
para la licencia completa. No se incluye ninguna clave de firma ni APK precompilado en Git.

Desde la raíz de FireLibre: `bash scripts/build-launcher.sh`. Requisitos y migración en
[la guía de launchers](../../docs/LAUNCHERS.md). La compilación no instala nada en un TV.

`guard_label` permanece como `dumbtv home button` para que el diagnóstico del servicio
original e integrado pueda reconocerlo; su descripción y los menús sí están traducidos.
No añadas permiso de internet ni dependencias como parte de una traducción.
