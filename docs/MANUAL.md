# Manual: ADB y cambios paso a paso

[Índice](../README.md) · [Inicio con scripts](INICIO.md) · [Restauración](RESTAURACION.md)

**Los cambios de paquetes y ajustes de este manual son para Fire TV.** Para Android TV y
Google TV sigue la [guía correspondiente](ANDROID-TV-Y-GOOGLE-TV.md). No apliques paquetes
Amazon a otro sistema ni sustituyas sus nombres por candidatos que solo parezcan equivalentes.

Esta guía explica las operaciones. El motor Python guarda y comprueba el estado con mayor
detalle que una secuencia pegada en terminal. Si eliges trabajar a mano, guarda cada valor
anterior y su orden; un comando `enable` general no recupera todos los estados originales.

## Conectar y elegir el equipo

```bash
adb connect 192.0.2.10:5555
adb -s 192.0.2.10:5555 shell getprop ro.product.model
adb -s 192.0.2.10:5555 shell getprop ro.product.manufacturer
adb -s 192.0.2.10:5555 shell getprop ro.build.version.sdk
adb -s 192.0.2.10:5555 shell am get-current-user
```

Acepta la autorización en pantalla. Usa siempre `-s`; podrías tener también un teléfono
conectado. Si el usuario activo no es 0, el flujo de cambios de TVLibre se detiene.

## Guardar el estado inicial

Crea una carpeta privada `state/manual` antes de estas órdenes. En PowerShell puedes usar
`New-Item -ItemType Directory -Force state/manual`.

```bash
mkdir -p state/manual
adb -s 192.0.2.10:5555 shell pm list packages --user 0 > state/manual/packages.txt
adb -s 192.0.2.10:5555 shell pm list packages -d --user 0 > state/manual/disabled.txt
adb -s 192.0.2.10:5555 shell settings list secure > state/manual/secure.txt
adb -s 192.0.2.10:5555 shell settings list global > state/manual/global.txt
adb -s 192.0.2.10:5555 shell dumpsys package com.amazon.tv.acr > state/manual/acr-before.txt
```

Los volcados de ajustes pueden contener identificadores. No los subas a GitHub.
En Fire OS 7 `settings list` y `settings delete` rechazan `--user`; por eso se ejecutan
sin esa opción, una vez comprobado que el usuario activo es 0.

## Deshabilitar un candidato revisado

Primero confirma que el paquete aparece instalado y que no pertenece a
[`profiles/protegidos.json`](../profiles/protegidos.json). Ejemplo para ACR:

```bash
adb -s 192.0.2.10:5555 shell pm disable-user --user 0 com.amazon.tv.acr
adb -s 192.0.2.10:5555 shell dumpsys package com.amazon.tv.acr
```

En la línea `User 0`, `enabled=3` significa deshabilitado por el usuario. Un rechazo
`Cannot disable a protected package` es un límite del sistema: no se intenta sortearlo.
No uses `pm uninstall`, `pm clear`, root ni escrituras en `/system` como sustitutos.

Para deshacer, si antes era `enabled=0`, usa `pm default-state --user 0 PAQUETE`;
si era `enabled=1`, usa `pm enable --user 0 PAQUETE`. Si ya estaba deshabilitado, no lo actives.

## Privacidad y reproducción automática

Los perfiles enumeran los ajustes ADB que se intentan aplicar, por ejemplo:

```bash
adb -s 192.0.2.10:5555 shell settings --user 0 put secure amz_limit_ad_tracking 1
adb -s 192.0.2.10:5555 shell settings --user 0 put secure settingsApp:appUsageData:value 0
adb -s 192.0.2.10:5555 shell settings --user 0 put global com.amazon.tv.settings.featured_item_video_enabled 0
```

La existencia de una clave no demuestra que el firmware la utilice. En el mando revisa
**Preferencias → Configuración de privacidad**: datos del dispositivo, datos de apps y anuncios
por intereses. Revisa también **Contenido destacado → reproducción de vídeo/audio**.
Son cinco comprobaciones visuales separadas de la lectura ADB.

## Animaciones

El perfil equilibrado propone `0.5` para ventanas y transiciones, y conserva el valor del
animador. En algunos Fire OS 8 cambiar el animador a 0.5 provocó problemas en el menú de ajustes
según [dumbtv](https://github.com/humblemuzzu/dumbtv/blob/main/data/fireos/settings.txt).
No cambies los tres valores a ciegas. Para restaurarlos usa el valor exacto guardado;
si una clave no existía, se elimina con `settings delete`, en lugar de inventar un valor inicial.

## Launcher, Home y arranque

Instalar un APK solo añade la app. Elegirla como predeterminada puede no capturar Home en
Fire TV. La [integración dumbtv](LAUNCHERS.md) utiliza su servicio Guard cuando el firmware
permite vincularlo; mantiene el inicio de Amazon disponible.

Después de instalar, prueba la navegación con el mando y abre una app. Pulsa Home físicamente.
Prueba también un reinicio y observa la primera pantalla sin abrir manualmente el launcher.
Una prueba ADB y una prueba física se documentan por separado.

## Aplicaciones que quieres retirar

El motor no retira apps. Si solo quieres que una app desaparezca del inicio, usa
**Opciones → Apps en Inicio** en dumbtv. Ocultar el icono no libera almacenamiento.
Para retirar una app instalada por ti, usa **Configuración → Aplicaciones → Administrar
aplicaciones instaladas → Desinstalar**. La disponibilidad depende de la app y del firmware.
No se proporciona una lista universal para borrar paquetes de Amazon: algunas apps comparten
licencias, voz o servicios del sistema.

## Validación final

Comprueba arranque, Home, mando, volumen, red y Ajustes. Reproduce contenido real en las apps
que utilizas y prueba Alexa/duplicación si las mantienes. No atribuyas una mejora de velocidad
o consumo a la limpieza sin una medición antes/después. TVLibre no publica cifras de ese tipo.
