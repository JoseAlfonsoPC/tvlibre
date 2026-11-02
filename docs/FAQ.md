# Preguntas frecuentes

[Índice](../README.md)

## ¿Esto instala otra versión de Android o desbloquea el bootloader?

No. Usa ADB sobre el sistema existente. No modifica `/system` ni cambia de sistema operativo.

## ¿Se puede volver atrás?

Los cambios de paquetes y ajustes registrados se restauran desde su copia si el dispositivo
y firmware coinciden y no hay conflictos posteriores. La instalación de apps, cambios de
cuenta y operaciones realizadas fuera del motor tienen otro alcance. Lee [Restauración](RESTAURACION.md).

## ¿Elimina toda la telemetría o todos los anuncios?

No se ha demostrado eso. Reduce componentes y preferencias concretos. Servicios protegidos,
contenido de apps y recomendaciones del inicio de Amazon pueden seguir teniendo publicidad.
Un launcher limpio no elimina anuncios dentro de una app de streaming.

## ¿Deja de funcionar Prime Video, Alexa o duplicación?

Se conservan sus paquetes y no se bloquea su red por defecto. Eso no sustituye una prueba
funcional de reproducción, voz y duplicación en cada firmware. Si una función falla, restaura
la sesión y registra el comportamiento sin añadir deshabilitaciones al azar.

## ¿Por qué vuelve al inicio de Amazon con Home?

Instalar un launcher no garantiza capturar Home. Comprueba que Guard esté vinculado y usa
`launcher verify --test-home`. Algunos firmwares rechazan servicios de terceros. Consulta
[Problemas](SOLUCION-DE-PROBLEMAS.md); no borres el inicio original para forzarlo.

## ¿Puedo usarlo en mi Stick nuevo si pone tercera generación?

Identifica el modelo y SDK con `doctor`. El AFTSSS Android 9 es la referencia; otros productos
con nombres parecidos pueden llevar otro Android o Vega OS. Consulta [Compatibilidad](COMPATIBILIDAD.md).

## ¿Por qué no se actualiza la traducción encima de la versión oficial?

Las firmas son distintas. Android impide ese reemplazo sin desinstalar. TVLibre se detiene
y explica la [migración](LAUNCHERS.md#migrar-desde-la-versión-oficial), incluida la pérdida del
historial privado que puede ocasionar. No borra automáticamente la instalación.

## ¿Puede Codex hacerlo todo sin que yo toque el mando?

Puede ejecutar el flujo autorizado desde un ordenador con acceso a la red local. Tú aceptas
ADB, consentimientos de VPN si decides usarlos y pruebas físicas. El prompt no puede eliminar
los permisos del ordenador ni las restricciones del firmware.

## ¿Puedo quitar Netflix, Music u otras apps?

Puedes ocultarlas en el launcher o retirar apps instaladas desde Ajustes. TVLibre no incluye
una desinstalación masiva y conserva las apps del usuario. No se deduce un paquete del nombre
sin comprobarlo en tu dispositivo.

## ¿Qué hago después de una actualización del sistema?

Nuevo diagnóstico, nuevo inventario y nuevo plan. El firmware puede restablecer ajustes o
cambiar permisos. No apliques una copia antigua a un firmware diferente.
