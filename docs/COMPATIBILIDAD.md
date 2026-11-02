# Dispositivos compatibles y cobertura real

[Índice](../README.md) · [Launchers](LAUNCHERS.md)

## Cómo decide el programa

El diagnóstico lee fabricante, modelo, Android SDK y firmware. Las modificaciones requieren
Amazon, usuario principal 0, una identidad estable y una versión admitida. No se usa el nombre
comercial como única prueba: generaciones, regiones y revisiones pueden llevar sistemas distintos.

| Sistema detectado | Diagnóstico | Limpieza | Home integrado |
|---|---|---|---|
| Amazon SDK 28, modelo AFTSSS | Sí | Permitida | Guard, con comprobación de vinculación |
| Amazon SDK 25 | Sí | Solo `--experimental` | Instalación del APK; Keeper no automatizado aquí |
| Amazon SDK 28, otros modelos | Sí | Solo `--experimental` | Solo prueba explícita; depende del firmware |
| Amazon SDK 29/30 | Sí | Solo `--experimental` | Guard experimental; puede ser rechazado |
| Amazon SDK 22, Fire OS 5 | Si ADB responde | Bloqueada | APK integrado requiere SDK 25 mínimo |
| SDK 31 o superior | Si ADB responde | Bloqueada en 0.1 | Sin ruta validada en TVLibre |
| Android TV / Google TV | Si ADB responde | Bloqueada | Referencias externas, sin automatización propia |
| Chromecast con Google TV / Google TV Streamer | Si ADB responde | Sin perfil propio | Guía específica e integraciones externas |
| Chromecast clásico, Ultra o Audio | Sin ruta compatible aquí | No | No se instala un launcher Android con este proyecto |
| Vega OS u otros sistemas sin Android | No con este motor | No | No |

Según la [documentación oficial de Amazon](https://developer.amazon.com/docs/fire-tv/fire-os-overview.html),
Fire OS 5 se basa en Android 5.1/SDK 22; Fire OS 6 en Android 7.1/25; Fire OS 7 en Android 9/28;
y Fire OS 8 incluye Android 10/29 y Android 11/30. Hay versiones posteriores y productos con
Vega OS. Revisa la tabla oficial para identificar cada modelo.

## La referencia comprobada

**Fire TV Stick de 3.ª generación, modelo AFTSSS / sheldonp**, Android 9, firmware de referencia
`PS7708.5501N`:

- En una configuración anterior a TVLibre se deshabilitaron los 33 candidatos del perfil
  ampliado, en dos etapas, y se comprobó que el TV volviera al inicio.
- dumbtv Home 1.6 y la traducción 1.6-es funcionaron; el launcher español arrancó tras reiniciar.
- Home físico se confirmó con dumbtv oficial; en la traducción se comprobó el retorno por ADB.
- Se comprobó apertura de Prime Video, Netflix y YouTube. No se verificaron reproducción,
  sesión de voz Alexa ni duplicación real. Conservar paquetes no demuestra esas funciones.
- El **motor Python nuevo** de TVLibre se comprueba con simulación de cambios y recuperación,
  y diagnóstico/plan de solo lectura sobre el dispositivo real. No se ha aplicado ni restaurado
  una sesión de este motor en hardware en la versión inicial.

Por tanto, «referencia» no equivale a certificar todas las funciones ni todas las actualizaciones
del AFTSSS. Una actualización puede cambiar permisos, paquetes o accesibilidad.

## Equipos que requieren especial atención

- **Fire TV Stick 2.ª gen AFTT con Fire OS 5:** en la experiencia de origen no pudo utilizar
  esta integración moderna ni asegurar Home. No se reduce el SDK mínimo para forzarlo.
- **Stick 4K, 4K Max, Lite, Cube y televisores Fire TV:** consulta su modelo y SDK, sin asumir
  equivalencia con el Stick de referencia. Solo se ofrecen pruebas experimentales dentro del
  rango indicado y no se promete Home automático.
- **Fire TV Stick 4K Select (2025), Fire TV Stick HD (2026) y Fire TV Stick 4K 3.ª gen (2026):**
  la tabla oficial los identifica con Vega OS; no son el AFTSSS y no admiten este proyecto Android.
- **Samsung Tizen, LG webOS, Roku y VIDAA:** necesitan procedimientos propios de su sistema.

## Añadir un dispositivo comprobado

Abre una incidencia con modelo, SDK y firmware, sin IP, número de serie, Wi-Fi ni cuentas.
Indica perfil, operaciones aceptadas/rechazadas, reinicio, Home físico y funciones reproducidas.
Usa la [plantilla de dispositivo](../.github/ISSUE_TEMPLATE/dispositivo.yml).
Un nuevo modelo no se marca probado porque únicamente instale un APK.
