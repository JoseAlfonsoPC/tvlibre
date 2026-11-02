# Origen, autoría y decisiones del proyecto

[Índice](../README.md) · [Licencias](../THIRD_PARTY_NOTICES.md)

FireLibre es un repositorio propio de **JoseAlfonsoPC**, con motor, interfaz de terminal,
flujo de recuperación, perfiles y documentación organizados para usuarios de habla española.
Su desarrollo parte de una experiencia real configurando dos generaciones distintas de Fire TV.

## Las tres referencias

| Referencia | Qué aprovechamos | Cómo se adapta |
|---|---|---|
| [Guía ADB de JLCareglio](https://gist.github.com/JLCareglio/881ab7feaa8013f838bec02c706b47a3) | Preparación ADB y posibilidad de combinar un launcher con privacidad de red | Manual redactado de nuevo; firewall opcional y sin bloqueo de OTA por defecto |
| [CleanYourTV](https://github.com/Gathin23/cleanyourtv) | Inventario, diagnóstico por modelo y deshabilitación reversible | Motor nuevo con planes, diario de intención y restauración del valor exacto |
| [dumbtv](https://github.com/humblemuzzu/dumbtv) | Launcher mínimo, Home mediante Guard y listas específicas de Fire TV | Integración de su código MIT traducido y comprobaciones separadas de Home/autoinicio |

## Qué es propio y qué sigue siendo de sus autores

El motor `firelibre/`, los comandos, la documentación en español, las pruebas y la identidad
de FireLibre pertenecen a este proyecto bajo MIT. Las listas de paquetes y ajustes se basan
en las dos guías de código abierto y en la configuración de referencia documentada.

El código Java del launcher es **dumbtv**, con modificaciones locales para recursos en español.
Mantiene el paquete `tv.dumbtv.home`, la estructura y la licencia originales. Su autoría no se
reemplaza por el nombre FireLibre. Las modificaciones están descritas en
[`UPSTREAM.json`](../integrations/dumbtv/UPSTREAM.json).

No se ha copiado el texto completo ni un script del gist como código propio. Se enlaza como
referencia conceptual. Tampoco se redistribuyen binarios ni código de Projectivy, NetGuard,
personalDNSfilter, FLauncher o Leanback on Fire.

## Decisiones que cambian el flujo

- Actualizaciones, Alexa, duplicación y apps personales se conservan.
- No hay borrado de cachés/datos, desinstalaciones masivas, root ni cambios en `/system`.
- No hay un filtro DNS automático que bloquee OTA como efecto secundario.
- Los paquetes protegidos no reciben una política de red por UID que se presente como
  bloqueo completo; esas restricciones tienen límites y posibles UID compartidos.
- La restauración recupera estados previos por sesión. No activa indiscriminadamente todos
  los paquetes de una lista, que podrían venir apagados de fábrica.
- Una clave ADB no demuestra un ajuste de cuenta, y un servicio habilitado no demuestra
  que Home funcione. Las verificaciones explicitan su alcance.
- El catálogo fija versión y checksum. No descarga silenciosamente el último APK disponible.

## Revisiones de origen

| Proyecto | Revisión usada como referencia |
|---|---|
| CleanYourTV | `572ce2cbe98b53654cea3d262ee8558a5872dfd1` |
| dumbtv | `755991b17a66e753e82f7252368c8850c08fdc71`, launcher 1.6 |
| Guía JLCareglio | Consulta del enlace público el 2 de noviembre de 2026; sin copiar su contenido íntegro |

Los proyectos originales evolucionan de forma independiente. FireLibre no se presenta como
versión oficial, sucesor autorizado ni soporte de Amazon, OpenAI o esos proyectos.
