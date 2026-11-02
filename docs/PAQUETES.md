# Perfiles, paquetes y ajustes

[Índice](../README.md) · [Privacidad](PRIVACIDAD.md)

## Elegir un perfil

**Conservador** propone 8 candidatos de métricas, diagnóstico e identificación de contenido,
y los indicadores de privacidad del espacio `secure`. **Equilibrado** amplía la lista a 33
candidatos y añade reproducción automática, avisos flotantes y dos escalas de animación.
El nombre de un paquete no siempre documenta su función: las descripciones expresan la
clasificación usada y señalan los casos cuya finalidad pública no está clara.

El plan filtra por instalación, estado previo y `--keep`. Esta tabla no es una lista de
órdenes para cualquier TV. Las pruebas de la lista de referencia se explican en
[Compatibilidad](COMPATIBILIDAD.md); la función de paquetes auxiliares puede variar.

## Candidatos

| Paquete | Perfil | Motivo / alcance |
|---|---|---|
| `com.amazon.ale` | Equilibrado | Componente auxiliar de experiencias de Amazon; perfil ampliado |
| `com.amazon.ceviche` | Equilibrado | Recopilación de datos de Amazon |
| `com.amazon.client.metrics.api` | Ambos | API de métricas |
| `com.amazon.connectivitydiag` | Equilibrado | Diagnóstico de conectividad |
| `com.amazon.dp.logger` | Ambos | Registro de diagnóstico |
| `com.amazon.dummy.alarmclock` | Equilibrado | App de relleno alarmclock |
| `com.amazon.dummy.calendar` | Equilibrado | App de relleno calendar |
| `com.amazon.dummy.contacts` | Equilibrado | App de relleno contacts |
| `com.amazon.dummy.gallery` | Equilibrado | App de relleno gallery |
| `com.amazon.dummy.music` | Equilibrado | App de relleno music |
| `com.amazon.dummy.settings` | Equilibrado | App de relleno settings |
| `com.amazon.hybridadidservice` | Ambos | Identificador publicitario |
| `com.amazon.katoch` | Equilibrado | Componente auxiliar de Amazon; función no documentada públicamente |
| `com.amazon.kso.blackbird` | Equilibrado | Contenido promocional |
| `com.amazon.livedeviceservice` | Equilibrado | Datos de interacción de dispositivos; validar las funciones usadas |
| `com.amazon.perfc` | Ambos | Diagnóstico de rendimiento |
| `com.amazon.perfcollection` | Ambos | Recopilación de rendimiento |
| `com.amazon.privacypassservice` | Equilibrado | Servicio de datos de privacidad del fabricante |
| `com.amazon.providers.contentsupport` | Equilibrado | Soporte de contenido recomendado |
| `com.amazon.shoptv.client` | Equilibrado | Compras desde el televisor |
| `com.amazon.shoptv.firetv.client` | Equilibrado | Compras desde Fire TV |
| `com.amazon.sneakpeek` | Equilibrado | Vista previa y recomendaciones |
| `com.amazon.storm.lightning.tutorial` | Equilibrado | Tutorial de la interfaz |
| `com.amazon.systemnotices` | Equilibrado | Avisos de Amazon |
| `com.amazon.tigris` | Equilibrado | Componente auxiliar de Amazon; función no documentada públicamente |
| `com.amazon.tmm.tutorial` | Equilibrado | Tutorial de administración de tareas |
| `com.amazon.tv.acr` | Ambos | Reconocimiento automático de contenido (ACR) |
| `com.amazon.tv.developer.dataservice` | Equilibrado | Datos y diagnóstico para desarrolladores |
| `com.amazon.tv.fw.metrics` | Ambos | Métricas del framework de TV |
| `com.amazon.tv.releasenotes` | Equilibrado | Notas de novedades del sistema |
| `com.amazon.wifilocker` | Equilibrado | Componente Wi-Fi auxiliar; validar la conexión tras el cambio |
| `com.amazon.wirelessmetrics.service` | Ambos | Métricas de conexión inalámbrica |
| `com.android.traceur` | Equilibrado | Registro de trazas del sistema |

## Ajustes propuestos

| Espacio | Clave | Valor | Perfil |
|---|---|---|---|
| `secure` | `amz_limit_ad_tracking` | `1` | Ambos |
| `secure` | `limit_ad_tracking` | `1` | Ambos |
| `secure` | `non_amz_limit_ad_tracking` | `1` | Ambos |
| `secure` | `advertisingIdApp:interestBasedAds:value` | `0` | Ambos |
| `secure` | `USAGE_METRICS_UPLOAD_ENABLED` | `0` | Ambos |
| `secure` | `usage_metrics_marketing_enabled` | `0` | Ambos |
| `secure` | `settingsApp:appUsageData:value` | `0` | Ambos |
| `secure` | `settingsApp:deviceUsageData:value` | `0` | Ambos |
| `global` | `heads_up_notifications_enabled` | `0` | Equilibrado |
| `global` | `com.amazon.tv.settings.featured_item_video_enabled` | `0` | Equilibrado |
| `global` | `com.amazon.tv.settings.featured_item_video_volume` | `0.0` | Equilibrado |
| `global` | `window_animation_scale` | `0.5` | Equilibrado |
| `global` | `transition_animation_scale` | `0.5` | Equilibrado |

Las claves de privacidad se leen después de escribirlas, pero pueden ser ignoradas o
sincronizadas por el firmware. Revisa las preferencias reales con el mando.
`animator_duration_scale` se deja tal como esté; no se establece a 0.5 para todos los modelos.

## Protecciones

La lista [protegidos.json](../profiles/protegidos.json) evita alterar el inicio, Ajustes,
servicios de entrada/mando, WebView, Appstore, Prime Video, paquetes OTA y otros componentes
que se decidió conservar. No es un inventario completo de todos los paquetes esenciales de
todos los Fire TV. Además, el motor solo permite actuar sobre los candidatos del perfil.

Los servicios protegidos por Amazon, como métricas de dispositivo o crash manager, se
excluyen de la limpieza automatizada. TVLibre no intenta conseguir root ni desinstalarlos.
Las apps personales ajenas a los perfiles se conservan aunque no estén en protegidos.json.

## Mantener las listas

Añade un paquete solo con evidencia de su presencia, función y recuperación en un modelo
concreto. Registra efectos sobre red, reproducción, mando y reinicio; no lo marques seguro
porque su nombre parezca publicidad. La CI comprueba duplicados y cruces con la lista protegida.
