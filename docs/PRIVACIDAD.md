# Privacidad, telemetría y red

[Índice](../README.md) · [Paquetes](PAQUETES.md)

## Qué reduce la limpieza

Los perfiles proponen desactivar componentes identificados de métricas, ACR, diagnósticos y
promociones, y escribir indicadores de limitación publicitaria. La verificación comprueba
estados de paquetes y ajustes. **No captura tráfico ni demuestra que Amazon haya dejado de
recibir todos los datos.** Algunos servicios están protegidos, siguen en ejecución o se
sincronizan con la cuenta.

FireLibre mantiene actualizaciones, Alexa, streaming y duplicación por defecto. No confunde
reducir datos con bloquear toda la conectividad de Amazon. Tampoco anuncia una aceleración
o ahorro de RAM que no se haya medido.

## Firewalls y DNS opcionales

| Herramienta | Alcance | Comprobación necesaria |
|---|---|---|
| [NetGuard](https://github.com/M66B/NetGuard) | Firewall sin root mediante VPN local | La persona acepta la VPN y comprueba las apps permitidas y los paquetes del sistema |
| [personalDNSfilter](https://github.com/IngoZenz/personaldnsfilter) | Filtro DNS, con ruta VPN local según configuración | Probar dominios bloqueados, dominios permitidos, navegación y reproducción |
| DNS del router o resolver elegido | Filtrado fuera del Stick | Comprobar qué resolver usa realmente el dispositivo y qué servicios comparte un dominio |

Son integraciones **manuales**, no pasos del perfil. Comprueba los proyectos oficiales y sus
requisitos actuales. No se distribuyen sus binarios ni se instala un servicio de red oculto.
NetGuard y un filtro DNS con VPN local normalmente compiten por la misma VPN de Android;
no actives ambos a la vez suponiendo que se acumulan sus protecciones.

La experiencia de la guía de JLCareglio inspira esta opción, pero FireLibre no copia su bloqueo
de actualizaciones ni su borrado de datos. Si mantienes OTA, no importes sin revisar una lista
que incluya servidores de actualización. Las listas de dumbtv pueden bloquearlos deliberadamente.

## Límites de las restricciones de segundo plano

`RUN_IN_BACKGROUND`, `RUN_ANY_IN_BACKGROUND` y las políticas de red por UID no equivalen a
un firewall universal. Una política para redes medidas puede no afectar a tu Wi-Fi. Varias
apps pueden compartir UID y resultar afectadas juntas. Por eso FireLibre 0.1 no aplica esas
restricciones a servicios protegidos ni cambia Data Saver global como supuesto bloqueo total.

## Los menús de Amazon importan

Revisa las tres preferencias de privacidad y las dos de reproducción automática con el mando.
El programa no marca una preferencia de cuenta como apagada solo porque una clave ADB acepte
el valor `0`. No se realizan compras, cambios de cuenta ni aceptación de consentimientos.

## Copias y publicación

Inventarios, ajustes y capturas pueden identificar el dispositivo o tus hábitos. `state/` y
las claves se excluyen de Git. Las incidencias necesitan modelo, SDK, firmware y resultados
resumidos; no necesitan IP, MAC, número de serie, nombres de Wi-Fi, cuentas ni copias completas.

ADB da acceso amplio al televisor a los ordenadores autorizados. Úsalo en una red de confianza
y decide si lo dejas activo al terminar. FireLibre no abre puertos del router ni elimina tus
autorizaciones automáticamente.
