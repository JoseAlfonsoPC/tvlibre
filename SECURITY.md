# Seguridad y datos personales

Versiones con mantenimiento inicial: rama `main` y serie `0.1.x`.

Si detectas una vulnerabilidad, utiliza la pestaña **Security → Advisories → Report a
vulnerability** cuando esté habilitada en este repositorio. Si no está disponible, contacta
al mantenedor mediante una vía privada que figure en su perfil de GitHub. No inventes una
dirección de contacto ni publiques credenciales o instrucciones de explotación en una issue.

Los fallos ordinarios pueden comunicarse con la plantilla de error, sin adjuntar datos
personales. Las copias y volcados de ajustes se consideran privados aunque algunos campos
estén resumidos con hashes.

El motor no requiere root ni modifica `/system`. ADB sigue siendo una interfaz con acceso
amplio: autoriza solo ordenadores propios y no abras su puerto a internet.

Los APK de release tienen checksum en el catálogo y `SHA256SUMS.txt`. Una compilación local
usa tu firma y debe revisarse por separado. No compartas claves ADB ni de firma.
