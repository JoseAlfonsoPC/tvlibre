# Solución de problemas

[Índice](../README.md) · [Recuperación](RESTAURACION.md)

| Síntoma | Comprobar / actuar |
|---|---|
| `unauthorized` | Acepta el diálogo ADB en el TV y repite una vez. No se acepta desde el ordenador. |
| `offline` tras reiniciar | Espera al arranque y renueva solo ese transporte: `adb -s IP:5555 reconnect`. No mates el servidor ADB de otros dispositivos. |
| IP no accesible | TV encendido, IP actual, red de invitados/aislamiento y depuración activada. |
| `--user not supported for delete and list` | Fire OS antiguo. El motor utiliza `settings list/delete` sin ese argumento y exige usuario 0 para modificar. |
| Modelo pendiente de validar | Usa diagnóstico y la matriz. `--experimental` es una elección explícita, no una corrección automática. |
| Plan rechazado por cambios | Genera un plan nuevo: el firmware, estado o dispositivo ya no coincide con el guardado. |
| `Cannot disable a protected package` | Conserva el registro. No pruebes root, borrar datos o desinstalar como alternativa. |
| Estado aplicado no coincide | La ejecución se detiene. Conserva el diario y verifica/restaura esa sesión. |
| Firma APK incompatible | No se desinstala automáticamente. Usa la guía de migración y respalda configuración accesible. |
| Home vuelve a Amazon | `launcher verify`; verifica vinculación real y que no compitan dos controladores de Home. |
| Guard habilitado pero no vinculado | El firmware puede rechazarlo. Restaura la activación; no lo des por funcional porque la clave esté escrita. |
| Demora al volver al inicio | Comprueba `alarm_manager_constants`; la activación registra `min_futurity=0`. Un cambio posterior necesita una sesión nueva. |
| Restauración con conflictos | Se conservan los valores que cambiaron después. Revisa el diario y deshaz sesiones posteriores primero. |
| El APK compila con otro hash | Otra firma o metadatos de compilación pueden cambiarlo. El catálogo verifica la release fijada; no ignores su hash para instalar un archivo distinto. |
| Menú del launcher en inglés | Comprueba el idioma del dispositivo y la versión 1.6-es. Las apps externas no se traducen desde el launcher. |

## Informar de un fallo

Incluye versión TVLibre, modelo, SDK, firmware, comando sin IP y mensaje de error resumido.
Indica si lo reprodujiste antes y después de restaurar. No adjuntes `state/`, volcados completos
de ajustes, claves, IP, cuentas ni capturas que los muestren. Utiliza las plantillas de incidencias.
