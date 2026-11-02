# Android TV, Google TV y Chromecast

[Índice](../README.md) · [Compatibilidad](COMPATIBILIDAD.md) · [Launchers](LAUNCHERS.md)

En Android TV y Google TV puedes utilizar el diagnóstico ADB y las integraciones de esta
guía. Los perfiles de limpieza incluidos en TVLibre 0.1 son específicos de Fire TV.

## Identificar el dispositivo

| Equipo | Recorrido en TVLibre 0.1 |
|---|---|
| Televisor o TV Box con Android TV | Diagnóstico ADB y proyectos específicos según modelo |
| Televisor o reproductor con Google TV | Diagnóstico ADB y proyectos específicos según modelo |
| Chromecast **con Google TV**, HD o 4K | Recorrido Google TV; validar versión y permisos de ADB |
| Google TV Streamer | Recorrido Google TV; sin prueba física propia de este proyecto |
| Chromecast clásico, Ultra o Audio | Sin ruta de instalación de launchers Android en TVLibre |
| Fire TV con Android/Fire OS | [Inicio Fire TV](INICIO.md), dentro de su matriz |
| Fire TV con Vega OS | No compatible con el motor Android |

[Google TV se apoya en Android TV OS](https://developer.android.com/training/tv/get-started/google-tv).
Los [Chromecast con Google TV](https://support.google.com/chromecast/answer/12578818?hl=es)
son los modelos con interfaz y mando; el nombre «Chromecast» por sí solo no identifica esa
plataforma. Disponer de Google Cast en un televisor tampoco demuestra que acepte ADB.

## Diagnóstico con TVLibre

1. Identifica marca, modelo, versión Android y opciones de desarrollador.
2. Activa y autoriza la depuración disponible en ese equipo. La ruta y el puerto pueden
   variar; no supongas que todos permiten `IP:5555`.
3. Sigue la [documentación ADB de Android](https://developer.android.com/tools/adb#connect-to-a-device-over-wi-fi)
   para conectar. Si el equipo ofrece depuración inalámbrica con emparejamiento, utiliza
   los puertos y código que muestre su propia pantalla; no hay un puerto universal.
4. Una vez conectado, utiliza su identificador explícito, por ejemplo:

```bash
python3 tvlibre.py --serial 192.0.2.10:5555 doctor --out state/doctor.json
python3 tvlibre.py --serial 192.0.2.10:5555 inventory --out state/inventory.json
```

Estos comandos no cambian ajustes ni apps. El bloqueo del
comando `plan` en plataformas sin perfil no indica que la conexión haya fallado: expresa
el alcance del motor actual. `--experimental` no convierte una lista de Fire TV en una
lista válida de Android TV o Google TV.

## Limpieza y launchers

- **[CleanYourTV](https://github.com/Gathin23/cleanyourtv):** consulta su inventario de modelos,
  instrucciones y recuperación para Android TV/Google TV. Revisa una lista del equipo
  concreto; no reutilices los paquetes de TVLibre para Amazon.
- **[Projectivy](https://github.com/spocky/miproja1):** alternativa para categorías, canales y
  personalización. Sigue la instalación y configuración oficiales para tu firmware.
- **[FLauncher](https://gitlab.com/flauncher/flauncher):** launcher alternativo para Android TV.
  Verifica su instalación, selección de inicio y compatibilidad en el dispositivo concreto.
- **dumbtv:** el código integrado se centra en Fire TV. No se presenta su servicio Guard
  como sustituto universal de Home para cualquier televisor.

Sigue las instrucciones y la recuperación de cada herramienta para tu modelo.

## Comprobar un nuevo modelo

Guarda el estado anterior antes de cualquier cambio y conserva el inicio, Ajustes, mando,
Play Store/servicios requeridos, actualizaciones y receptor Cast si lo utilizas. Después
comprueba Home físico, reinicio, reproducción, voz y envío de contenido desde otro dispositivo.

Para aportar compatibilidad, indica modelo, Android SDK, firmware, herramienta usada,
cambios exactos y qué se restauró y probó. Usa la [plantilla de dispositivo](../.github/ISSUE_TEMPLATE/dispositivo.yml).
