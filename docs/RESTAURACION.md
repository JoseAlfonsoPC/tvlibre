# Restauración y recuperación

[Índice](../README.md) · [Problemas frecuentes](SOLUCION-DE-PROBLEMAS.md)

## Qué copia se usa

Cada ejecución que modifica estados genera una carpeta privada distinta en `state/`.
Apunta las rutas completas de las sesiones de limpieza y de activación del launcher.
`backup.json` contiene valores previos, valores aplicados y operaciones intentadas.
No se reconstruyen los valores anteriores a partir de una lista genérica.

```bash
python3 firelibre.py --serial 192.0.2.10:5555 restore --backup state/FECHA-cleanup-ID/backup.json --yes
python3 firelibre.py --serial 192.0.2.10:5555 verify --backup state/FECHA-cleanup-ID/backup.json
```

## Volver al inicio anterior, conservando la limpieza

Restaura **la copia de propósito `launcher`**, no la de limpieza:

```bash
python3 firelibre.py --serial 192.0.2.10:5555 restore --backup state/FECHA-launcher-ID/backup.json --yes
adb -s 192.0.2.10:5555 shell input keyevent KEYCODE_HOME
```

Se recupera la lista de accesibilidad, su estado de activación, los parámetros de alarma y
la exención de batería que modificó esa sesión. El APK sigue instalado.
Si antes ya había un controlador de Home, se recupera ese estado anterior: no se promete
Amazon como resultado de una copia cuyo estado inicial ya tenía otro launcher activo.

## Qué ocurre con varias sesiones

Deshaz las sesiones en **orden inverso**, empezando por la más reciente. No edites un
`backup.json` para convertirlo en una lista universal. Si el estado actual es distinto tanto
del anterior como del aplicado, el programa lo considera un conflicto y no lo pisa.
Intenta recuperar las demás operaciones y devuelve error si queda alguna pendiente.

Si el proceso se cortó justo después de escribir un ajuste, su marca `attempted` permite
comparar el dispositivo real y recuperarlo. La marca `applied` por sí sola no sería suficiente.
No hay una transacción Android global: puede quedar una sesión parcialmente aplicada y
necesitar este comando de restauración.

## Lo que no revierte `restore`

- Desinstalaciones que hayas hecho tú, cuentas o datos privados de otras apps.
- Interruptores cambiados con el mando, si no se registraron en una sesión ADB.
- Actualizaciones de firmware o cambios de DNS/firewall hechos fuera del motor.
- La instalación/actualización de un APK. Su registro `action=install-apk` conserva un APK
  previo cuando estaba disponible; no es un diario `purpose=launcher`.
- Una sesión en otro equipo o firmware. La identidad y la compilación deben coincidir.

Para un APK, reinstalar una versión anterior puede requerir procedimientos y datos que no
son reversibles sin pérdida. FireLibre no usa downgrade forzado, borrado de datos ni
desinstalación automática. Consulta [Migración de firma](LAUNCHERS.md#migrar-desde-la-versión-oficial).

## Si ya había cambios de otras guías

FireLibre guarda el estado que encuentre **al comenzar su propia sesión**. Un paquete ya
deshabilitado seguirá así al deshacer FireLibre. Para restaurar CleanYourTV, dumbtv u otra
guía anterior necesitas sus copias y herramientas originales.

## Tras una actualización de Fire OS

Ejecuta `doctor`, un inventario y un plan nuevos. No fuerces el uso de una copia de un firmware
distinto. La identidad sigue siendo importante, pero no basta para asegurar que los paquetes
y permisos sigan teniendo la misma función.

## Sin ADB o sin copia

Revisa IP y depuración en el TV. Si puedes abrir Ajustes, desactiva el servicio de accesibilidad
del launcher en sus menús y abre el inicio de Amazon. Conserva siempre la copia antes de tocar
otras opciones. Este proyecto no ejecuta un restablecimiento de fábrica como recuperación
automática ni promete reconstruir datos que ya no existen.
