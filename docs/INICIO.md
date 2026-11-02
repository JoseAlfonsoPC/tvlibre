# Empezar con FireLibre

[Volver al índice](../README.md) · [Compatibilidad](COMPATIBILIDAD.md) · [Manual ADB](MANUAL.md)

## 1. Preparar el ordenador

- macOS/Linux: Python 3.10+ como `python3`. Windows: Python 3.10+ como `python`.
- Instala [Platform Tools de Android](https://developer.android.com/tools/releases/platform-tools)
  y añade su carpeta a PATH. Comprueba `adb version`.
- `git clone https://github.com/JoseAlfonsoPC/firelibre.git` y entra en `firelibre`.
- No necesitas `pip`, root, un cable USB ni modificar el sistema de archivos del TV.

Ejecuta los ejemplos desde la raíz del repositorio. El wrapper `scripts/firelibre.sh` o
`scripts/firelibre.ps1` también acepta los mismos argumentos; los archivos de estado se guardan
relativos al directorio desde el que lo ejecutes.

## 2. Preparar el Fire TV

En los modelos compatibles: **Configuración → Mi Fire TV → Acerca de**. Pulsa siete veces
sobre el nombre del dispositivo si no aparecen las opciones de desarrollador. Regresa y activa
**Depuración ADB**. El recorrido puede variar entre firmwares.

Anota la IP desde **Acerca de → Red**. Ordenador y Stick deben tener comunicación en la misma
red; las redes de invitados suelen aislar dispositivos.

```bash
adb connect 192.0.2.10:5555
adb devices
```

Acepta en el televisor «Permitir depuración USB». La conexión debe figurar como `device`.
`unauthorized` necesita una aceptación física; `offline` significa que la sesión no está lista.

## 3. Diagnosticar sin cambiar nada

```bash
python3 firelibre.py --serial 192.0.2.10:5555 doctor --out state/doctor.json
python3 firelibre.py --serial 192.0.2.10:5555 inventory --out state/inventory.json
```

Estos archivos son privados. El diagnóstico puede funcionar en equipos que **no** tienen
autorizada la limpieza. No confundas tener ADB con ser un modelo validado.

## 4. Revisar el plan

```bash
python3 firelibre.py --serial 192.0.2.10:5555 plan --profile conservador --out state/plan.json
```

El perfil `equilibrado` amplía los candidatos a componentes de compras, avisos, diagnósticos y
tutoriales. Lee [Paquetes](PAQUETES.md) antes de elegirlo. Puedes conservar candidatos concretos:

```bash
python3 firelibre.py --serial 192.0.2.10:5555 plan --profile equilibrado --keep com.amazon.shoptv.client com.amazon.wifilocker --out state/plan.json
```

El plan registra lo que ya estaba apagado y lo deja así. No supone que todos los modelos tengan
todos los paquetes. Un plan generado con `--experimental` conserva ese indicador al aplicarse.
Los equipos no Android o las versiones fuera de cobertura siguen bloqueados.

## 5. Aplicar y comprobar

```bash
python3 firelibre.py --serial 192.0.2.10:5555 apply --plan state/plan.json --yes
```

Guarda la ruta de `backup.json` que aparece antes del primer cambio. Sustituye `RUTA` por ella:

```bash
python3 firelibre.py --serial 192.0.2.10:5555 verify --backup RUTA
```

Si una orden se rechaza, la ejecución se detiene y conserva lo ya registrado. No intenta
desbloquear paquetes protegidos. Usa [Restauración](RESTAURACION.md) si quieres deshacer.

## 6. Revisar los menús de privacidad

Comprueba con el mando **Preferencias → Configuración de privacidad**: uso del dispositivo,
uso de apps y anuncios basados en intereses. Desactiva los tres si esa es tu preferencia.
En **Contenido destacado**, revisa reproducción automática de vídeo y audio.
Los valores ADB pueden no reflejar por sí solos el estado sincronizado con tu cuenta.

## 7. Añadir un inicio sencillo

Continúa en [Launchers](LAUNCHERS.md). Instalación, activación de Home y reinicio son pasos
separados. No deshabilites el launcher de Amazon para forzar la sustitución.

Al terminar, prueba reproducción real, sonido, Wi-Fi, mando, Alexa y duplicación si las usas.
Si vas a seguir configurando, deja ADB activa por decisión propia; si terminas, puedes apagarla
desde Opciones para desarrolladores. No expongas el puerto ADB fuera de tu red.
