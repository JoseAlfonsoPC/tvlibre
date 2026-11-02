# Privacidad, telemetría y red

[Índice](../README.md) · [Paquetes](PAQUETES.md)

## Qué reduce la limpieza

Los perfiles proponen desactivar componentes identificados de métricas, ACR, diagnósticos y
promociones, y escribir indicadores de limitación publicitaria. La verificación comprueba
estados de paquetes y ajustes. **No captura tráfico ni demuestra que Amazon haya dejado de
recibir todos los datos.** Algunos servicios están protegidos, siguen en ejecución o se
sincronizan con la cuenta.

TVLibre mantiene actualizaciones, Alexa, streaming y duplicación por defecto.

## Firewalls y DNS opcionales

| Herramienta | Alcance | Comprobación necesaria |
|---|---|---|
| [NetGuard](https://github.com/M66B/NetGuard) | Firewall sin root mediante VPN local | La persona acepta la VPN y comprueba las apps permitidas y los paquetes del sistema |
| [personalDNSfilter](https://github.com/IngoZenz/personaldnsfilter) | Filtro DNS, con ruta VPN local según configuración | Probar dominios bloqueados, dominios permitidos, navegación y reproducción |
| DNS del router o resolver elegido | Filtrado fuera del Stick | Comprobar qué resolver usa realmente el dispositivo y qué servicios comparte un dominio |

Son integraciones **manuales**, no pasos del perfil. Comprueba los proyectos oficiales y sus
requisitos actuales.
NetGuard y un filtro DNS con VPN local normalmente compiten por la misma VPN de Android;
no actives ambos a la vez suponiendo que se acumulan sus protecciones.

Si mantienes OTA, revisa que la lista elegida permita los servidores de actualización.
Las listas de dumbtv pueden bloquearlos deliberadamente.

## Límites de las restricciones de segundo plano

`RUN_IN_BACKGROUND`, `RUN_ANY_IN_BACKGROUND` y las políticas de red por UID no equivalen a
un firewall universal. Una política para redes medidas puede no afectar a tu Wi-Fi. Varias
apps pueden compartir UID y resultar afectadas juntas. Por eso TVLibre 0.1 no aplica esas
restricciones a servicios protegidos ni cambia Data Saver global como supuesto bloqueo total.

## Los menús de Amazon importan

Revisa las tres preferencias de privacidad y las dos de reproducción automática con el mando.
Los valores ADB pueden no reflejar por sí solos el estado sincronizado con tu cuenta.
