# Política de seguridad

## Alcance y propósito

CredVault DBeaver recupera credenciales que **DBeaver guardó localmente** para el **usuario que
ejecuta la herramienta**, en su propia máquina. No rompe cifrado fuerte: DBeaver Community protege
su almacén con una **clave fija y pública** embebida en el propio programa. La herramienta solo lee
archivos a los que el usuario ya tiene acceso en su sistema de archivos.

## Uso responsable

- Úsala únicamente sobre equipos y cuentas **propias**, o con autorización explícita y por escrito
  del dueño del equipo.
- No la emplees para acceder a credenciales de terceros sin permiso.
- El proyecto no incluye ni debe incluir credenciales, hosts ni IPs reales de ninguna organización.
  Todos los datos de ejemplo son ficticios.

## Buenas prácticas al usarla

- Cierra DBeaver antes de ejecutarla (evita leer un archivo en uso).
- No compartas la salida: contiene contraseñas en claro.
- Si trabajas en un equipo compartido, borra cualquier exportación al terminar.

## Reporte de vulnerabilidades

Si encuentras un fallo de seguridad en el código (no un mal uso de la herramienta), repórtalo de
forma privada al mantenedor **antes** de divulgarlo públicamente. Evita abrir un issue público con
los detalles. Nos comprometemos a responder y, si procede, publicar una corrección y el crédito.
